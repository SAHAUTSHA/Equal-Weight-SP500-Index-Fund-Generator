# Equal Weight S&P500 Index Fund Generator
**Purpose:** This project uses the IEX Cloud API to receive the real-time market prices of the S&P500 stocks. Then constructs an equal-weight S&P500 portfolio with the portfolio value inputted by the user. 
<br />
<br />
**Files:**<br />
_main.py_ - Equal Weight S&P500 Index Fund Generator Program.<br />
_SP500.csv_ - .csv File containing all S&P500 Tickers and Stock Name.<br />
_personalToken.py_ - Contains IEX Cloud token. To test this code, please replace the existing token with your own.<br />
<br />
**Version Control:**
This project uses the Python module 'pandas' in version 1.4.4 as newer versions have removed the .append method for Dataframes. <br />
All other libraries can be up-to-date.<br />
<br />
**Sample Generated Pandas Dataframe (as of Aug 16, 2023):**
![pandasSCN](https://github.com/SAHAUTSHA/Equal-Weight-SP500-Index-Fund-Generator/assets/83483386/b2d09f9b-4581-4222-9be6-427eef2a0513)
<br />
****Sample Generated CSV File Output:****
![CSVsampleOutput](https://github.com/SAHAUTSHA/Equal-Weight-SP500-Index-Fund-Generator/assets/83483386/42a99c5c-945b-41b8-9509-c34bdeb7a559)



