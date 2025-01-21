# Paul Han
# 1/12/2025
# Stock Evaluator AI Agent - This is a stock evaluator that uses AI to evaluate a stock

import yfinance as yf
import boto3
import json
from textblob import TextBlob  # For basic sentiment analysis
import requests
from datetime import datetime, timedelta

# Fetch stock data
def fetch_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        # Extract relevant financial data
        data = {
            "current_price": info.get("currentPrice", "N/A"),
            "market_cap": info.get("marketCap", "N/A"),
            "industry": info.get("industry", "N/A"),
            "price_to_earnings": info.get("trailingPE", "N/A"),
            "dividend_yield": info.get("dividendYield", "N/A"),
            "peg_ratio": info.get("trailingPegRatio", "N/A"),
            "price_to_sales": info.get("priceToSalesTrailing12Months", "N/A"),
            "price_to_book": info.get("priceToBook", "N/A"),
            "earnings_yield": info.get("trailingPE", "N/A"),
            "ev_to_ebitda": safe_division(info.get("enterpriseValue"), info.get("ebitda")),
            "roe": info.get("returnOnEquity", "N/A"),
            "roa": info.get("returnOnAssets", "N/A"),
        }
        return data
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

def safe_division(a, b):
    """Safely perform division, returning 'N/A' if invalid"""
    try:
        if a is None or b is None or b == 0:
            return "N/A"
        return a / b
    except Exception:
        return "N/A"

def fetch_news_sentiment(ticker):
    """Fetch and analyze news sentiment for a given stock ticker"""
    try:
        # Get news from Yahoo Finance
        stock = yf.Ticker(ticker)
        news = stock.news
        
        if not news:
            return {
                "sentiment_score": "N/A",
                "recent_headlines": [],
                "sentiment_summary": "No recent news found"
            }

        # Analyze sentiment for each news item
        sentiments = []
        headlines = []
        
        for article in news[:5]:  # Analyze last 5 news items
            # Extract title from the correct location in the structure
            headline = article.get('content', {}).get('title', '')
            if not headline:  # Fallback to direct title if content structure doesn't exist
                headline = article.get('title', '')
                
            # Extract description for better sentiment analysis
            description = article.get('content', {}).get('description', '')
            if not description:
                description = article.get('description', '')
                
            # Combine title and description for better sentiment analysis
            full_text = f"{headline} {description}".strip()
            
            if headline:  # Only append if we actually got a headline
                headlines.append(headline)
                analysis = TextBlob(full_text)
                sentiments.append(analysis.sentiment.polarity)
        
        avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0
        
        # Categorize overall sentiment
        if avg_sentiment > 0.2:
            sentiment_summary = "Positive"
        elif avg_sentiment < -0.2:
            sentiment_summary = "Negative"
        else:
            sentiment_summary = "Neutral"
            
        return {
            "sentiment_score": round(avg_sentiment, 2),
            "recent_headlines": headlines,
            "sentiment_summary": sentiment_summary
        }
    except Exception as e:
        print(f"Error fetching news sentiment: {e}")
        return None

# Analyze stock data with GPT
def analyze_stock(data, sentiment_data=None):
    try:
        bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-west-2')
        
        # Include sentiment data in the analysis prompt
        prompt = create_analysis_prompt(data, sentiment_data)

        kwargs = {
            "modelId": "anthropic.claude-3-5-haiku-20241022-v1:0",
            "contentType": "application/json",
            "accept": "application/json",
            "body": json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 300,
                "temperature": 0.7,
                "top_p": 0.999,
                "messages": [{"role": "user", "content": prompt}]
            })
        }

        response = bedrock_runtime.invoke_model(**kwargs)
        response_body = json.loads(response['body'].read().decode('utf-8'))
        return response_body
    except Exception as e:
        print(f"Error during analysis: {e}")
        return None

def create_analysis_prompt(data, sentiment_data=None):
    """Create a formatted prompt for stock analysis including sentiment"""
    base_prompt = f"""
    Analyze the following financial data and provide a recommendation:
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
        base_prompt += f"""
    Recent News Sentiment: {sentiment_data['sentiment_summary']} (Score: {sentiment_data['sentiment_score']})
    Recent Headlines:
    """
        for headline in sentiment_data['recent_headlines']:
            base_prompt += f"- {headline}\n"
    
    base_prompt += "\nBased on both financial metrics and recent news sentiment, is this a good investment at the current price? Keep it short and concise."
    return base_prompt

def main():
    while True:
        ticker = input("Enter a stock ticker (or 'quit' to exit): ").upper()
        if ticker == 'QUIT':
            break
            
        print("\nFetching financial data and news sentiment...")
        stock_data = fetch_stock_data(ticker)
        if not stock_data:
            continue
        sentiment_data = fetch_news_sentiment(ticker)

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

        recommendation = analyze_stock(stock_data, sentiment_data)
        if recommendation:
           print("\nAI Recommendation:")
           try:
               print(recommendation['content'][0]['text'])
           except (KeyError, IndexError) as e:
               print("Error parsing recommendation")
        print("\n" + "-"*50 + "\n")

# main
if __name__ == "__main__":
    main()