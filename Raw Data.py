import streamlit as st
from datetime import date



import yfinance as yf


from plotly import graph_objs as go





#timeframe of selected data
START = "2014-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

#title of tool
st.title('The raw company data along a time series display.')

#selection of stocks, and their info
stocks = ("TSLA", "SOFI", "NIO", "AAPL", "MSFT", "GOOG", "GOOGL", "CCL", "AMD", "LCID",  "PLTR",  "F",  "NVDA",  "MARA",  "JOBY",  "OPEN",  "AMZN", "CVNA", "IONQ", "RIVN", "BAC", "NCLH", "UBER", "PFE", "INTC", "AAL", "VALE", "NU", "AMC", "COIN", "ISEE", "DNA", "APE", "SIRI", "U", "SWN", "LUMN", "T", "BBD", "MU", "ABEV", "XPEV", "SNAP", "WBA", "WBD", "ITUB", "RIG", "NOK", "ENVX", "KMI", "LYFT", "PBR", "RIOT", "GOLD", "PINS", "WMB", "KEY", "DAL", "PYPL", "FTCH", "FCX", "META", "CHPT", "PLUG", "SNOW", "BABA", "CMCSA", "GM", "HOOD", "JBLU", "RBLX", "VZ", "MRO", "GRAB", "AFRM", "HBAN", "PCG", "WFC", "C", "AGNC", "XOM", "GIS", "SHOP", "PBR-A", "S", "DISH", "ERIC", "PR", "LU", "HST", "DIS", "PTON", "ROIV", "IQ", "JD", "CSX", "ORCL", "SLB", "OXY", "ES=F", "NQ=F", "YM=F", )
selected_stock = st.sidebar.selectbox("Select dataset to predict", stocks)





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

