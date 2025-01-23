import yfinance as yf
from models.stock_data import FinancialData
from utils.helpers import safe_division

class StockService:
    @staticmethod
    def fetch_stock_data(ticker: str) -> FinancialData:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            return FinancialData(
                current_price=info.get("currentPrice", "N/A"),
                market_cap=info.get("marketCap", "N/A"),
                industry=info.get("industry", "N/A"),
                price_to_earnings=info.get("trailingPE", "N/A"),
                dividend_yield=info.get("dividendYield", "N/A"),
                peg_ratio=info.get("trailingPegRatio", "N/A"),
                price_to_sales=info.get("priceToSalesTrailing12Months", "N/A"),
                price_to_book=info.get("priceToBook", "N/A"),
                earnings_yield=info.get("trailingPE", "N/A"),
                ev_to_ebitda=safe_division(info.get("enterpriseValue"), info.get("ebitda")),
                roe=info.get("returnOnEquity", "N/A"),
                roa=info.get("returnOnAssets", "N/A")
            )
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            return None 