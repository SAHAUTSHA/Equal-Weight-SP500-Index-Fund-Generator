# Utsha K. Saha
# Equal-Weight S&P500 Index Fund Generator

# Import Libraries
import numpy as np
import pandas as pd # We are using Pandas 1.4.4, the latest version of pandas does not have append for Dataframes.
import requests
import xlsxwriter
import math

# Import Stock Tickers
# A S&P500 csv is attached to this Git Repository (updated Aug. 2023)
# If desired, a user could change the csv to have different stocks than S&P500
stocks = pd.read_csv('SP500.csv')

# Import IEX Cloud API Token
# In order for this code to work, a valid subscription / token to IEX Cloud is necessary.
# The token used for this project was a 7-day free trial token that has expired.
# To test this code, you can create a free IEX Cloud account and get a 7-day free trial token.
from personalToken import IEX_CLOUD_API_TOKEN

# Batch API Calls to IEX Cloud
# We will take our S&P500 list and divide them into 'chunks' of 100 stocks since
# IEX Cloud can handle up to 100 stocks per Batch request
def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

# This array lists the information we want to recieve and document.
my_columns = [ 'Ticker', 'Stock Price', 'Market Capitalization', 'Number of Shares to Buy']

# Loop through chunks to get Stock Ticker, Stock Price, and Stock Market Cap
symbol_groups = list(chunks(stocks['Symbol'], 100))
symbol_strings = []
for i in range(0, len(symbol_groups)):
    symbol_strings.append(','.join(symbol_groups[i]))
    # print(symbol_strings[i])
final_dataframe = pd.DataFrame(columns = my_columns)

for symbol_string in symbol_strings:
    batch_api_call_url = f'https://cloud.iexapis.com/stable/stock/market/batch?symbols={symbol_string}&types=quote&token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(batch_api_call_url).json()
    for symbol in symbol_string.split(','):
        final_dataframe = final_dataframe.append(
            pd.Series(
            [
                symbol,
                data[symbol]['quote']['latestPrice'],
                data[symbol]['quote']['marketCap'],
                'N/A'
            ],
            index = my_columns),
            ignore_index=True
        )

# Calculate the Number of Shares to Buy to achieve a Equal-Weight Portfolio
# This following input asks the user to enter the value of their portfolio
portfolio_size = input('Enter the value of your portfolio:')

try:
    val = float(portfolio_size)
    print(val)
except ValueError:
    print("Error: Invalid Portfolio Value! \nPlease try again:")
    portfolio_size = input('Enter the value of your portfolio:')
    val = float(portfolio_size)

# The following calculates the Number of Shares to Buy to achieve a Equal-Weight Portfolio
position_size = val/len(final_dataframe.index)
for i in range(0, len(final_dataframe.index)):
    final_dataframe.loc[i, 'Number of Shares to Buy'] = math.floor(position_size/final_dataframe.loc[i, 'Stock Price'])

# Excel Output File
# Initializing XlsxWriter - Generate a Excel file with the Equal Weight S&P500 Index Fund Generator
writer = pd.ExcelWriter('Recommended Trades.xlsx', engine = 'xlsxwriter')
final_dataframe.to_excel(writer, 'Recommended Trades', index = False)

# Format Excel Sheet (Background and Font Color and Symbols '$')
background_color = '#D1FFBD'
font_color = '#000000'

string_format = writer.book.add_format(
    {
        'font_color': font_color,
        'bg_color': background_color,
        'border': 1
    }
)

dollar_format = writer.book.add_format(
    {
        'num_format': '$0.00',
        'font_color': font_color,
        'bg_color': background_color,
        'border': 1
    }
)

integer_format = writer.book.add_format(
    {
        'num_format': '0',
        'font_color': font_color,
        'bg_color': background_color,
        'border': 1
    }
)

# Formats Columns for the Excel Sheet
column_formats = {
    'A': ['Ticker', string_format],
    'B': ['Stock Price', dollar_format],
    'C': ['Market Capitalization', dollar_format],
    'D': ['Number of Shares to Buy', integer_format]
}

# Loop to format Columns Headers
for column in column_formats.keys():
    writer.sheets['Recommended Trades'].set_column(f'{column}:{column}', 18, column_formats[column][1])
    writer.sheets['Recommended Trades'].write(f'{column}1', column_formats[column][0], column_formats[column][1])

# Save the Excel Output
writer.save()