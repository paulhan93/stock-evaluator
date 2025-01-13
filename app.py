# Paul Han
# 1/12/2025
# Stock Evaluator - Stock Price Calculator 

import yfinance as yf
import json

def main():
    # Prompt user for ticker symbol
    ticker = input("Ticker: ")

    # Fetch the financial data for the ticker symbol using yfinance
    stock = yf.Ticker(ticker)
    info = stock.info

    # Save the info dictionary to a file
    file_name = f"{'ticker'}_info.json"
    with open(file_name, "w") as file:
        json.dump(info, file, indent=4)

    # print company info
    print(stock.info['website'])
    print(stock.info['address1'])
    print(stock.info['city'], stock.info['state'])
    print(stock.info['zip'])
    print(stock.info['country'])
    print()
    print(stock.info['industry'])
    print(stock.info['sector'])
    print()
    print(stock.info['longBusinessSummary'])
    print()

    # print current stock price
    print("Current Stock Price: ", stock.info['currentPrice'])
    print()
    
    # print financial ratios


    # Calculate Financial Ratios: These ratios are used to evaluate the value of a stock 
    pe_ratio = stock.info['trailingPE']
    ps_ratio = stock.info['priceToSalesTrailing12Months']
    pb_ratio = stock.info['priceToBook']
    earnings_yield = 1 / pe_ratio
    ev_to_ebitda = stock.info['enterpriseValue'] / stock.info['ebitda']
    #fcf_ratio = stock.info['freeCashFlow'] / stock.info['marketCap']
    roe = stock.info['returnOnEquity']
    roa = stock.info['returnOnAssets']
    #roce = stock.info['returnOnCapitalEmployed']

    # Print Financial Ratios
    print("PE ratio: ", pe_ratio)
    print("PS ratio: ", ps_ratio)
    print("PB ratio: ", pb_ratio)
    print("Earnings yield: ", earnings_yield)
    print("EV-to-EBITDA ratio: ", ev_to_ebitda)
    #print("FCF ratio: ", fcf_ratio)
    print("ROE: ", roe)
    print("ROA: ", roa)
    #print("ROCE: ", roce)

    return 0

# main
if __name__ == "__main__":
    main()