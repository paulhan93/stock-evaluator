# Paul Han
# 1/12/2025
# Stock Evaluator - Stock Price Calculator 

import yfinance as yf
import json

# Prompt user for ticker symbol
ticker = input("Ticker: ")
print("\n")

# Fetch the financial data for the ticker symbol using yfinance
stock = yf.Ticker(ticker)
info = stock.info

# Save the info dictionary to a file
file_name = f"{ticker}_info.json"
with open(file_name, "w") as file:
    json.dump(info, file, indent=4)

# print stock info
#print(stock.info)

#print(stock.history(period="1mo"))

#print(stock.financials)

#print(stock.balance_sheet)

#print(stock.cashflow)


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
print("\n")
print("PE ratio: ", pe_ratio)
print("PS ratio: ", ps_ratio)
print("PB ratio: ", pb_ratio)
print("Earnings yield: ", earnings_yield)
print("EV-to-EBITDA ratio: ", ev_to_ebitda)
#print("FCF ratio: ", fcf_ratio)
print("ROE: ", roe)
print("ROA: ", roa)
#print("ROCE: ", roce)
