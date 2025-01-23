import boto3
import json
from typing import Optional, Dict
from models.stock_data import FinancialData, SentimentData

class AIService:
    def __init__(self):
        self.bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-west-2')

    def get_recommendation(self, ticker: str, financial_data: FinancialData, 
                         sentiment_data: Optional[SentimentData]) -> Optional[str]:
        try:
            prompt = self._create_analysis_prompt(ticker, financial_data, sentiment_data)
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
            result = json.loads(response['body'].read().decode('utf-8'))
            return result['content'][0]['text'] if result else None
        except Exception as e:
            print(f"Error during AI analysis: {e}")
            return None

    def _create_analysis_prompt(self, ticker: str, data: FinancialData, 
                              sentiment_data: Optional[SentimentData]) -> str:
        prompt = f"""
        Analyze {ticker} stock based on the following financial data and provide a recommendation:
        Current Price: {data.current_price}
        Market Cap: {data.market_cap}
        Industry: {data.industry}
        Price-to-Earnings Ratio: {data.price_to_earnings}
        Dividend Yield: {data.dividend_yield}
        PEG Ratio: {data.peg_ratio}
        Price-to-Sales Ratio: {data.price_to_sales}
        Price-to-Book Ratio: {data.price_to_book}
        Earnings Yield: {data.earnings_yield}
        EV-to-EBITDA Ratio: {data.ev_to_ebitda}
        ROE: {data.roe}
        ROA: {data.roa}
        """
        
        if sentiment_data:
            prompt += f"""
            Recent News Sentiment: {sentiment_data.sentiment_summary} (Score: {sentiment_data.sentiment_score})
            Recent Headlines:
            """
            for headline in sentiment_data.recent_headlines:
                prompt += f"- {headline}\n"
        
        prompt += "\nBased on both financial metrics and recent news sentiment, is this a good investment at the current price? Keep it short and concise. Be sure to add a risk level, target price range, and recommendation."
        return prompt 