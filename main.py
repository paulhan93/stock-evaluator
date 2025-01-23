import sys
from datetime import datetime
from pathlib import Path
from services.stock_service import StockService
from services.sentiment_service import SentimentService
from services.ai_service import AIService
from utils.logger import StockAnalysisLogger
from models.stock_data import StockAnalysis
from config import OUTPUT_DIR

class StockAnalyzer:
    def __init__(self):
        self.stock_service = StockService()
        self.sentiment_service = SentimentService()
        self.ai_service = AIService()

    def analyze_single_stock(self, ticker: str) -> None:
        output_file = self._get_output_filename(ticker)
        
        with open(output_file, 'w') as f:
            original_stdout = sys.stdout
            sys.stdout = StockAnalysisLogger(original_stdout, f)
            
            try:
                self._perform_analysis(ticker)
            finally:
                sys.stdout = original_stdout
                print(f"\nAnalysis saved to: {output_file}")

    def _get_output_filename(self, ticker: str) -> Path:
        today = datetime.now().strftime("%Y-%m-%d")
        return OUTPUT_DIR / f"{today}_{ticker}_analysis.txt"

    def _perform_analysis(self, ticker: str) -> None:
        today = datetime.now().strftime("%Y-%m-%d")
        print(f"\nAnalysis for {ticker} - {today}\n")
        print("=" * 50)

        print("\nFetching financial data and news sentiment...")
        financial_data = self.stock_service.fetch_stock_data(ticker)
        if not financial_data:
            return

        sentiment_data = self.sentiment_service.fetch_news_sentiment(ticker)
        recommendation = self.ai_service.get_recommendation(
            ticker, financial_data, sentiment_data
        )

        analysis = StockAnalysis(
            ticker=ticker,
            financial_data=financial_data,
            sentiment_data=sentiment_data,
            recommendation=recommendation,
            analysis_date=datetime.now()
        )

        self._display_analysis_results(analysis)

    def _display_analysis_results(self, analysis: StockAnalysis) -> None:
        print("\nFinancial Data:")
        for key, value in vars(analysis.financial_data).items():
            print(f"{key}: {value}")

        if analysis.sentiment_data:
            print("\nNews Sentiment Analysis:")
            print(f"Overall Sentiment: {analysis.sentiment_data.sentiment_summary}")
            print(f"Sentiment Score: {analysis.sentiment_data.sentiment_score}")
            print("\nRecent Headlines:")
            for headline in analysis.sentiment_data.recent_headlines:
                print(f"- {headline}")

        if analysis.recommendation:
            print("\nAI Recommendation:")
            print(analysis.recommendation)
        
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
