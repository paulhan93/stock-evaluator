# Paul Han
# 1/12/2025
# Stock Evaluator AI Agent - This is a stock evaluator that uses AI to evaluate a stock

import yfinance as yf
import boto3
import json
from textblob import TextBlob
import requests
from datetime import datetime
import sys
from pathlib import Path

class StockAnalysisLogger:
    """Custom logger to write output to both file and console"""
    def __init__(self, original_stdout, file):
        self.terminal = original_stdout
        self.file = file

    def write(self, message):
        self.file.write(message)
        self.terminal.write(message)

    def flush(self):
        self.file.flush()
        self.terminal.flush()

class StockAnalyzer:
    """Main class for analyzing stocks"""
    def __init__(self):
        self.output_dir = Path("analysis_outputs")
        self.output_dir.mkdir(exist_ok=True)
        self.bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-west-2')

    def get_output_filename(self, ticker):
        """Generate output filename based on date and ticker"""
        today = datetime.now().strftime("%Y-%m-%d")
        return self.output_dir / f"{today}_{ticker}_analysis.txt"

    def analyze_single_stock(self, ticker):
        """Analyze a single stock and save results"""
        output_file = self.get_output_filename(ticker)
        
        with open(output_file, 'w') as f:
            original_stdout = sys.stdout
            sys.stdout = StockAnalysisLogger(original_stdout, f)
            
            try:
                self._perform_analysis(ticker)
            finally:
                sys.stdout = original_stdout
                print(f"\nAnalysis saved to: {output_file}")

    def _perform_analysis(self, ticker):
        """Perform the actual stock analysis"""
        today = datetime.now().strftime("%Y-%m-%d")
        print(f"\nAnalysis for {ticker} - {today}\n")
        print("=" * 50)

        # Fetch and display financial data
        print("\nFetching financial data and news sentiment...")
        stock_data = self._fetch_stock_data(ticker)
        if not stock_data:
            return

        sentiment_data = self._fetch_news_sentiment(ticker)
        self._display_analysis_results(ticker, stock_data, sentiment_data)

    def _fetch_stock_data(self, ticker):
        """Fetch financial data for a stock"""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            return {
                "current_price": info.get("currentPrice", "N/A"),
                "market_cap": info.get("marketCap", "N/A"),
                "industry": info.get("industry", "N/A"),
                "price_to_earnings": info.get("trailingPE", "N/A"),
                "dividend_yield": info.get("dividendYield", "N/A"),
                "peg_ratio": info.get("trailingPegRatio", "N/A"),
                "price_to_sales": info.get("priceToSalesTrailing12Months", "N/A"),
                "price_to_book": info.get("priceToBook", "N/A"),
                "earnings_yield": info.get("trailingPE", "N/A"),
                "ev_to_ebitda": self._safe_division(info.get("enterpriseValue"), info.get("ebitda")),
                "roe": info.get("returnOnEquity", "N/A"),
                "roa": info.get("returnOnAssets", "N/A"),
            }
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            return None

    def _fetch_news_sentiment(self, ticker):
        """Fetch and analyze news sentiment"""
        try:
            stock = yf.Ticker(ticker)
            news = stock.news
            #print("\nDEBUG - Raw news data:")
            #print(news)  # See the raw news structure
            
            if not news:
                print("DEBUG - No news found")
                return self._create_empty_sentiment_data()

            sentiments = []
            headlines = []
            
            print("\nDEBUG - Processing articles:")
            for i, article in enumerate(news[:5]):
                print(f"\nDEBUG - Article {i + 1}:")
                print(article)  # See each article's structure
                
                # Try direct access first
                headline = article.get('title', '')
                if not headline:
                    # Try nested structure
                    headline = article.get('content', {}).get('title', '')
                    
                description = article.get('description', '')
                if not description:
                    description = article.get('content', {}).get('description', '')
                
                print(f"DEBUG - Extracted headline: {headline}")
                print(f"DEBUG - Extracted description: {description}")
                
                full_text = f"{headline} {description}".strip()
                
                if full_text:
                    headlines.append(headline)
                    analysis = TextBlob(full_text)
                    sentiment = analysis.sentiment.polarity
                    print(f"DEBUG - Sentiment score: {sentiment}")
                    sentiments.append(sentiment)

            if not sentiments:
                print("DEBUG - No valid sentiments found")
                return self._create_empty_sentiment_data()
                
            avg_sentiment = sum(sentiments) / len(sentiments)
            
            result = {
                "sentiment_score": round(avg_sentiment, 2),
                "recent_headlines": headlines,
                "sentiment_summary": self._get_sentiment_category(avg_sentiment)
            }
            
            print("\nDEBUG - Final sentiment result:")
            print(result)
            
            return result
            
        except Exception as e:
            print(f"Error in sentiment analysis: {str(e)}")
            print(f"Error type: {type(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            return None

    def _process_article(self, article):
        """Process a single news article"""
        headline = article.get('title', '')
        description = article.get('description', '')
        full_text = f"{headline} {description}".strip()
        
        if not full_text:
            return None, None
            
        analysis = TextBlob(full_text)
        return headline, analysis.sentiment.polarity

    def _create_empty_sentiment_data(self):
        """Create empty sentiment data structure"""
        return {
            "sentiment_score": "N/A",
            "recent_headlines": [],
            "sentiment_summary": "No recent news found"
        }

    def _calculate_sentiment_results(self, sentiments, headlines):
        """Calculate sentiment analysis results"""
        if not sentiments:
            return self._create_empty_sentiment_data()
            
        avg_sentiment = sum(sentiments) / len(sentiments)
        
        return {
            "sentiment_score": round(avg_sentiment, 2),
            "recent_headlines": headlines,
            "sentiment_summary": self._get_sentiment_category(avg_sentiment)
        }

    def _get_sentiment_category(self, score):
        """Categorize sentiment score"""
        if score > 0.2:
            return "Positive"
        elif score < -0.2:
            return "Negative"
        return "Neutral"

    def _safe_division(self, a, b):
        """Safely perform division"""
        try:
            if a is None or b is None or b == 0:
                return "N/A"
            return a / b
        except Exception:
            return "N/A"

    def _create_analysis_prompt(self, ticker, data, sentiment_data):
        """Create the analysis prompt for the AI"""
        prompt = f"""
        Analyze {ticker} stock based on the following financial data and provide a recommendation:
        Current Price: {data['current_price']}
        Market Cap: {data['market_cap']}
        Industry: {data['industry']}
        Price-to-Earnings Ratio: {data['price_to_earnings']}
        Dividend Yield: {data['dividend_yield']}
        PEG Ratio: {data['peg_ratio']}
        Price-to-Sales Ratio: {data['price_to_sales']}
        Price-to-Book Ratio: {data['price_to_book']}
        Earnings Yield: {data['earnings_yield']}
        EV-to-EBITDA Ratio: {data['ev_to_ebitda']}
        ROE: {data['roe']}
        ROA: {data['roa']}
        """
        
        if sentiment_data:
            prompt += self._format_sentiment_data(sentiment_data)
        
        prompt += "\nBased on both financial metrics and recent news sentiment, is this a good investment at the current price? Keep it short and concise."
        return prompt

    def _format_sentiment_data(self, sentiment_data):
        """Format sentiment data for the prompt"""
        result = f"\nRecent News Sentiment: {sentiment_data['sentiment_summary']} (Score: {sentiment_data['sentiment_score']})\nRecent Headlines:\n"
        for headline in sentiment_data['recent_headlines']:
            result += f"- {headline}\n"
        return result

    def _get_ai_recommendation(self, ticker, data, sentiment_data):
        """Get AI recommendation for the stock"""
        try:
            prompt = self._create_analysis_prompt(ticker, data, sentiment_data)
            response = self.bedrock_runtime.invoke_model(
                modelId="anthropic.claude-3-5-haiku-20241022-v1:0",
                contentType="application/json",
                accept="application/json",
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 300,
                    "temperature": 0.7,
                    "top_p": 0.999,
                    "messages": [{"role": "user", "content": prompt}]
                })
            )
            return json.loads(response['body'].read().decode('utf-8'))
        except Exception as e:
            print(f"Error during AI analysis: {e}")
            return None

    def _display_analysis_results(self, ticker, stock_data, sentiment_data):
        """Display the analysis results"""
        print("\nFinancial Data:")
        for key, value in stock_data.items():
            print(f"{key}: {value}")

        if sentiment_data:
            print("\nNews Sentiment Analysis:")
            print(f"Overall Sentiment: {sentiment_data['sentiment_summary']}")
            print(f"Sentiment Score: {sentiment_data['sentiment_score']}")
            print("\nRecent Headlines:")
            for headline in sentiment_data['recent_headlines']:
                print(f"- {headline}")

        recommendation = self._get_ai_recommendation(ticker, stock_data, sentiment_data)
        if recommendation:
            print("\nAI Recommendation:")
            try:
                print(recommendation['content'][0]['text'])
            except (KeyError, IndexError) as e:
                print("Error parsing recommendation")
        print("\n" + "=" * 50 + "\n")

def main():
    analyzer = StockAnalyzer()
    while True:
        ticker = input("Enter a stock ticker (or 'quit' to exit): ").upper()
        if ticker == 'QUIT':
            break
        analyzer.analyze_single_stock(ticker)

if __name__ == "__main__":
    main()