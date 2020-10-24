import yfinance as yf
import streamlit as st
import datetime
import pandas_ta
import pandas as pd
import requests
yf.pdr_override()

st.write("""
# Technical Analysis Web Application
Shown below are the **Moving Average Crossovers**, **Bollinger Bands**, **MACD's**, **Commodity Channel Indexes**, and **Relative Strength Indexes** of any stock!
""")

st.sidebar.header('User Input Parameters')

today = datetime.date.today()
def user_input_features():
    ticker = st.sidebar.text_input("Ticker", 'IP.CN')
    start_date = st.sidebar.text_input("Start Date", '2019-01-01')
    end_date = st.sidebar.text_input("End Date", f'{today}')
    return ticker, start_date, end_date

symbol, start, end = user_input_features()

def get_symbol(symbol):
    url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(symbol)
    result = requests.get(url).json()
    for x in result['ResultSet']['Result']:
        if x['symbol'] == symbol:
            return x['name']
company_name = get_symbol(symbol.upper())

start = pd.to_datetime(start)
end = pd.to_datetime(end)

# Read data 
data = yf.download(symbol,start,end)
st.write(data)
# Adjusted Close Price
st.header(f"Adjusted Close Price\n {company_name}")
st.line_chart(data["Close"])

# ## SMA and EMA
#Simple Moving Average
data.ta.sma(length=20, append=True)

# Exponential Moving Average
data.ta.ema(length=20, append=True)
st.write(data)
# Plot
st.header(f"Simple Moving Average vs. Exponential Moving Average\n {company_name}")
st.line_chart(data[['adj_close','SMA_20','EMA_20']])

# Bollinger Bands
data.ta.bbands(length=20, append=True)
# data['upper_band'], data['middle_band'], data['lower_band'] = talib.BBANDS(data['Adj Close'], timeperiod =20)
# Plot
st.header(f"Bollinger Bands\n {company_name}")
st.line_chart(data[['adj_close','BBL_20_2.0','BBM_20_2.0','BBU_20_2.0']])

# ## RSI (Relative Strength Index)
# RSI
data.ta.rsi(length=20, append=True)
st.write(data)
# Plot
st.header(f"Relative Strength Index\n {company_name}")
st.line_chart(data['RSI_20', 'adj_close'])

# ## OBV (On Balance Volume)
# OBV
# data['OBV'] = talib.OBV(data['Adj Close'], data['Volume'])/10**6
data.ta.pvol(length=20, append=True)
# Plot
st.header(f"Price-Volume\n {company_name}")
st.line_chart(data['PVOL_20', 'adj_close'])
st.write(data)
