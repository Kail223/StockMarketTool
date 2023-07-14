#MANUAL SCRAPING START
#importing framework/tools
import streamlit as st
from datetime import date


import streamlit as st
import pandas as pd

import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go


#timeframe of selected data
START = "2014-01-01"
TODAY = date.today().strftime("%Y-%m-%d")
#title of tool
#st.title("Stock, The Market Tool")
#selection of stocks, and their info
stocks = ("TSLA", "SOFI", "NIO", "AAPL", "MSFT", "GOOG", "GOOGL", "CCL", "AMD", "LCID",  "PLTR",  "F",  "NVDA",  "MARA",  "JOBY", "OPEN", "AMZN", "CVNA", "IONQ", "RIVN", "BAC", "NCLH", "UBER", "PFE", "INTC", "AAL", "VALE", "NU", "AMC", "COIN", "ISEE", "DNA", "APE", "SIRI", "U", "SWN", "LUMN", "T", "BBD", "MU", "ABEV", "XPEV", "SNAP", "WBA", "WBD", "ITUB", "RIG", "NOK", "ENVX", "KMI", "LYFT", "PBR", "RIOT", "GOLD", "PINS", "WMB", "KEY", "DAL", "PYPL", "FTCH", "FCX", "META", "CHPT", "PLUG", "SNOW", "BABA", "CMCSA", "GM", "HOOD", "JBLU", "RBLX", "VZ", "MRO", "GRAB", "AFRM", "HBAN", "PCG", "WFC", "C", "AGNC", "XOM", "GIS", "SHOP", "PBR-A", "S", "DISH", "ERIC", "PR", "LU", "HST", "DIS", "PTON", "ROIV", "IQ", "JD", "CSX", "ORCL", "SLB", "OXY", "ES=F", "NQ=F", "YM=F", )
selected_stock = st.sidebar.selectbox("Select dataset to predict", stocks)



#sidebar section

def stats(dataframe):
    st.header('Raw-Data')
    st.write(dataframe.describe())


n_years = st.sidebar.slider("Years of prediction:", 1, 4)
period = n_years * 365


#reformatting the script and cleaning it up
# Add a title and intro text
#for the main page
st.title('All data related to the selected stock.')
st.text('This web app provides historical stock market data.')
#create a file uploader for potential user data sets in the sidebar
st.sidebar.title('User Data')
upload_file = st.sidebar.file_uploader('Upload your file containing data.')
#if checks
#check file using pandas
if upload_file is not None:
 
#read file to df from pandas 
    df = pd.read_csv(upload_file)


#section for raw data    
    st.header('Raw Data')
    st.write(df.describe())

#section for forecasting
    
    st.header('Forecasted Data')
    st.write(df.head())


    st.sidebar.title('Sidebar')


if upload_file is not None:
    df = pd.read_csv(upload_file)










#load stock name
#yfinance import
#cache stock selection
@st.cache_data

def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data
data_load_state = st.sidebar.text("Load data...")
data = load_data(selected_stock)
data_load_state.text("Loading data...done!")


st.subheader('Raw-Data')
st.write(data.tail())
#after import then set up graph
def plot_raw_data():
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name='Stock_Open'))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='Stock_Close'))
    fig.layout.update(title_text="Time Series Data", xaxis_rangeslider_visible=True)

    st.plotly_chart(fig)
plot_raw_data()












#Forecasting formatting
#data and closing columns
df_train = data[['Date', 'Close']]
df_train = df_train.rename(columns={"Date": "ds", "Close": "y" })
#this data will layout the training and fit it
m = Prophet()
m.fit(df_train)
#next is the forecast into the future by a specific number of days
#period definition was multiplied because it needs to be in days
future = m.make_future_dataframe(periods=period)
forecast = m.predict(future)

st.subheader('Forecast Data')
st.write(forecast.tail())


#assinging to a figure
# re assigning a title to the graph
st.write('Forecast data')
fig1 = plot_plotly(m, forecast)
st.plotly_chart(fig1)

#creating another figure without plotly
st.write('forecast components')
fig2 = m.plot_components(forecast)
st.write(fig2)