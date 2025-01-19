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
            "current_price": info.get("currentPrice"),
            "market_cap": info.get("marketCap"),
            "industry": info.get("industry"),
            "price_to_earnings": info.get("trailingPE"),
            "dividend_yield": info.get("dividendYield"),
            "peg_ratio": info.get("trailingPegRatio"),
            "price_to_sales": info.get("priceToSalesTrailing12Months"),
            "price_to_book": info.get("priceToBook"),
            "earnings_yield": info.get("trailingPE"),
            "ev_to_ebitda": info.get("enterpriseValue") / info.get("ebitda"),
            "roe": info.get("returnOnEquity"),
            "roa": info.get("returnOnAssets"),
        }
        return data
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

# Analyze stock data with GPT
def analyze_stock(data):
    # Initialize the Bedrock client
    bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-west-2')

    prompt = f"""
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
    Is this a good investment at the current price?
    """

    kwargs = {
        "modelId": "anthropic.claude-3-5-haiku-20241022-v1:0",  # Ensure this is the correct model ID
        "contentType": "application/json",
        "accept": "application/json",
        "body": json.dumps({  # Serialize the body to a JSON string
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 200,
            "temperature": 1,
            "top_p": 0.999,
            "messages": [
                {
                    "role": "user",
                    "content": prompt  # Directly pass the prompt as a string
                }
            ]
        })
    }

    response = bedrock_runtime.invoke_model(**kwargs)
    response_body = response['body'].read().decode('utf-8')  # Decode the response body
    return response_body




def main():
    # Display data
    ticker = input("Enter a stock ticker: ").upper()
    stock_data = fetch_stock_data(ticker)

    if stock_data:
        print("\nFinancial Data:")
        for key, value in stock_data.items():
            print(f"{key}: {value}")

        recommendation = analyze_stock(stock_data)
        print("\nAI Recommendation:")
        print(recommendation)
    else:
        print("Could not fetch stock data.")
    return 0

# main
if __name__ == "__main__":
    main()