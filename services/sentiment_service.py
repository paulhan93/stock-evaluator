import yfinance as yf
from textblob import TextBlob
from models.stock_data import SentimentData, NewsItem
from typing import List, Optional

class SentimentService:
    @staticmethod
    def fetch_news_sentiment(ticker: str) -> Optional[SentimentData]:
        try:
            stock = yf.Ticker(ticker)
            news = stock.news
            
            if not news:
                return None

            sentiments = []
            headlines = []
            
            for article in news[:5]:
                headline = article.get('title', '')
                description = article.get('description', '')
                
                if headline:
                    headlines.append(headline)
                    full_text = f"{headline} {description}".strip()
                    analysis = TextBlob(full_text)
                    sentiments.append(analysis.sentiment.polarity)

            if not sentiments:
                return None
                
            avg_sentiment = sum(sentiments) / len(sentiments)
            
            return SentimentData(
                sentiment_score=round(avg_sentiment, 2),
                recent_headlines=headlines,
                sentiment_summary=SentimentService._get_sentiment_category(avg_sentiment)
            )
            
        except Exception as e:
            print(f"Error in sentiment analysis: {e}")
            return None

    @staticmethod
    def _get_sentiment_category(score: float) -> str:
        if score > 0.2:
            return "Positive"
        elif score < -0.2:
            return "Negative"
        return "Neutral" 