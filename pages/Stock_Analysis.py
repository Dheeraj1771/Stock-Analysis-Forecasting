# Import the Required Modules
import streamlit as st
import pandas as pd
import yfinance as yf
# import plotly.graph_objects as go
import datetime
# import ta
from pages.utils.plotly_figure import plotly_table, close_chart, candlestick, RSI, moving_average, MACD


# Setting the Page Config
st.set_page_config(
    page_title="Stock Analysis",
    page_icon=":page_with_curl:",
    layout='wide'
)

st.title("Stock Analysis")

# Creating Three Columns for Text Input and Date
col1, col2, col3 = st.columns(3)

# Today's Date
today = datetime.date.today()

# Create the Three Columns
with col1:
    # Select the Ticker, Choose Defualt value as Tesla - TSLA
    ticker = st.text_input("Stock Ticker", "TSLA")
with col2:
    # Select the Start Date, Choose default value as 1 year before from today's date
    start_date = st.date_input("Choose Start Date", today - datetime.timedelta(days=365))
    
with col3:
    # Select the End Date, Choose default value as todays date
    end_date = st.date_input("Choose End Date", datetime.date(today.year, today.month, today.day))
    
st.subheader(ticker)

stock = yf.Ticker(ticker)

st.write(stock.info['longBusinessSummary'])
st.write("**The Sector of the Company is:**", stock.info['sector'])
st.write("**The Number of Full Time Employess in the Company is:** ", str(stock.info['fullTimeEmployees']))
st.write("**The Link to the Company Website is:** ", stock.info['website'])


# To Show other Metrics in a DF (Data Frame) like Market Cap, Beta, EPS, PE Ratio
col1, col2 = st.columns(2)

with col1:
    # Create a DataFrame 
    df = pd.DataFrame(index=['Market Cap', 'Beta', 'EPS', 'PE Ratio'])
    df[''] = [stock.info["marketCap"], stock.info['beta'], stock.info['trailingEps'], stock.info['trailingPE']]
    # Pass the DataFrame into the plotly_table
    fig_df = plotly_table(df)
    st.plotly_chart(fig_df, use_container_width=True)
    
with col2:
    df = pd.DataFrame(index=['Quick Ratio', 'Revenue per share', 'Profit Margins',
                             'Debt to Equity', 'Return on Equity'])
    
    df[''] = [stock.info["quickRatio"], stock.info["revenuePerShare"], stock.info["profitMargins"], stock.info["debtToEquity"], stock.info["returnOnEquity"]]
    
    fig_df = plotly_table(df)
    st.plotly_chart(fig_df, use_container_width=True)
   
# Dowload the Data using yfinance   
# 1. Create a cached function for downloading
@st.cache_data
def fetch_historical_data(ticker, start, end):
    return yf.download(ticker, start=start, end=end)

# 2. Call the new cached function
data = fetch_historical_data(ticker, start=start_date, end=end_date)

col1, col2, col3 = st.columns(3)

# Daily Change (today - yesterday)
current_price = data['Close'].iloc[-1].item()
previous_price = data['Close'].iloc[-2].item()
daily_change =  current_price - previous_price
col1.metric(label="Daily Change", 
            value=str(round(current_price, 2)), 
            delta=str(round(daily_change, 2))
)

# Historical Trend
last_10_df = data.tail(10).sort_index(ascending=False).round(3)
fig_df = plotly_table(last_10_df)
st.write("##### Historical Data (Last 10 Days)")
st.plotly_chart(fig_df, use_container_width=True)

# Create Buttons
col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12 = st.columns([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

num_period=''
with col1:
    if st.button('5D'):
        num_period='5d'
with col2:
    if st.button('1M'):
        num_period='1mo'
with col3:
    if st.button('6M'):
        num_period='6mo'
with col4:
    if st.button('YTD'):
        num_period='ytd'
with col5:
    if st.button('1Y'):
        num_period='1y'
with col6:
    if st.button('5Y'):
        num_period='5y'
with col7:
    if st.button('MAX'):
        num_period='max'
        
col1, col2, col3 = st.columns([1, 1, 4])
with col1:
    chart_type = st.selectbox('', ('Candle', 'Line'))
with col2:
    if chart_type == 'Candle':
        indicators = st.selectbox('', ('RSI', 'MACD'))
    else:
        indicators = st.selectbox('', ('RSI', 'Moving Average', 'MACD'))
        
ticker_ = yf.Ticker(ticker)
new_df1 = ticker_.history(period='max')
data1 = ticker_.history(period='max')

# If Button is not selected
if num_period == '':
    if chart_type=='Candle' and indicators=='RSI':
        st.plotly_chart(candlestick(data1, '1y'), use_container_width=True)
        st.plotly_chart(RSI(data1, '1y'), use_container_width=True)
    if chart_type=='Candle' and indicators=='MACD':
        st.plotly_chart(candlestick(data1, '1y'), use_container_width=True)
        st.plotly_chart(MACD(data1, '1y'), use_container_width=True)
    if chart_type=='Line' and indicators=='RSI':
        st.plotly_chart(close_chart(data1, '1y'), use_container_width=True)
        st.plotly_chart(RSI(data1, '1y'), use_container_width=True)
    if chart_type=='Line' and indicators=='Moving Average':
        st.plotly_chart(moving_average(data1, '1y'), use_container_width=True)
    if chart_type=='Line' and indicators=='MACD':
        st.plotly_chart(close_chart(data1, '1y'), use_container_width=True)
        st.plotly_chart(MACD(data1, '1y'), use_container_width=True)
else:
    if chart_type=='Candle' and indicators=='RSI':
        st.plotly_chart(candlestick(new_df1, num_period), use_container_width=True)
        st.plotly_chart(RSI(new_df1, num_period), use_container_width=True)
    if chart_type=='Candle' and indicators=='MACD':
        st.plotly_chart(candlestick(new_df1, num_period), use_container_width=True)
        st.plotly_chart(MACD(new_df1, num_period), use_container_width=True)
    if chart_type=='Line' and indicators=='RSI':
        st.plotly_chart(close_chart(new_df1, num_period), use_container_width=True)
        st.plotly_chart(RSI(new_df1, num_period), use_container_width=True)
    if chart_type=='Line' and indicators=='Moving Average':
        st.plotly_chart(moving_average(new_df1, num_period), use_container_width=True)
    if chart_type=='Line' and indicators=='MACD':
        st.plotly_chart(close_chart(new_df1, num_period), use_container_width=True)
        st.plotly_chart(MACD(new_df1, num_period), use_container_width=True)