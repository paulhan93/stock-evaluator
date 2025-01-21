# Paul Han
# 1/12/2025
# Stock Evaluator AI Agent - This is a stock evaluator that uses AI to evaluate a stock

import yfinance as yf
import boto3
import json

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

# Analyze stock data with GPT
def analyze_stock(data):
    try:
        bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-west-2')
        
        # Move prompt template to a separate constant
        prompt = create_analysis_prompt(data)

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

def create_analysis_prompt(data):
    """Create a formatted prompt for stock analysis"""
    return f"""
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
    Is this a good investment at the current price? Keep it short and concise.
    """

def main():
    while True:
        ticker = input("Enter a stock ticker (or 'quit' to exit): ").upper()
        if ticker == 'QUIT':
            break
            
        stock_data = fetch_stock_data(ticker)
        if not stock_data:
            continue

        print("\nFinancial Data:")
        for key, value in stock_data.items():
            print(f"{key}: {value}")

        recommendation = analyze_stock(stock_data)
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