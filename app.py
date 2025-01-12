import yfinance as yf

# Get the user's input for the company ticker symbol
ticker = input("Enter the company ticker symbol: ")

# Fetch the financial data for the ticker symbol using yfinance
stock = yf.Ticker(ticker)

# Calculate Financial Ratios: These ratios are used to evaluate the value of a stock 
pe_ratio = stock.info['trailingPE']
#ps_ratio = stock.info['priceToSalesTrailing12Months']
pb_ratio = stock.info['priceToBook']
earnings_yield = 1 / pe_ratio
#ev_to_ebitda = stock.info['enterpriseValue'] / stock.info['ebitda']
#fcf_ratio = stock.info['freeCashFlow'] / stock.info['marketCap']
#roe = stock.info['returnOnEquity']
#roa = stock.info['returnOnAssets']
#roce = stock.info['returnOnCapitalEmployed']

# Print Financial Ratios
print("PE ratio: ", pe_ratio)
#print("PS ratio: ", ps_ratio)
print("PB ratio: ", pb_ratio)
print("Earnings yield: ", earnings_yield)
#print("EV-to-EBITDA ratio: ", ev_to_ebitda)
#print("FCF ratio: ", fcf_ratio)
#print("ROE: ", roe)
#print("ROA: ", roa)
#print("ROCE: ", roce)
