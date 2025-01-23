from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class FinancialData:
    current_price: float
    market_cap: float
    industry: str
    price_to_earnings: float
    dividend_yield: float
    peg_ratio: float
    price_to_sales: float
    price_to_book: float
    earnings_yield: float
    ev_to_ebitda: float
    roe: float
    roa: float

@dataclass
class NewsItem:
    title: str
    description: str
    sentiment_score: float

@dataclass
class SentimentData:
    sentiment_score: float
    recent_headlines: List[str]
    sentiment_summary: str

@dataclass
class StockAnalysis:
    ticker: str
    financial_data: FinancialData
    sentiment_data: Optional[SentimentData]
    recommendation: Optional[str]
    analysis_date: datetime 