import streamlit as st
from datetime import date



import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly




START = "2014-01-01"
TODAY = date.today().strftime("%Y-%m-%d")


st.title('Forecasted Data and the projection charts.')

stocks = ("TSLA", "SOFI", "NIO", "AAPL", "MSFT", "GOOG", "GOOGL", "CCL", "AMD", "LCID",  "PLTR",  "F",  "NVDA",  "MARA",  "JOBY", "OPEN", "AMZN", "CVNA", "IONQ", "RIVN", "BAC", "NCLH", "UBER", "PFE", "INTC", "AAL", "VALE", "NU", "AMC", "COIN", "ISEE", "DNA", "APE", "SIRI", "U", "SWN", "LUMN", "T", "BBD", "MU", "ABEV", "XPEV", "SNAP", "WBA", "WBD", "ITUB", "RIG", "NOK", "ENVX", "KMI", "LYFT", "PBR", "RIOT", "GOLD", "PINS", "WMB", "KEY", "DAL", "PYPL", "FTCH", "FCX", "META", "CHPT", "PLUG", "SNOW", "BABA", "CMCSA", "GM", "HOOD", "JBLU", "RBLX", "VZ", "MRO", "GRAB", "AFRM", "HBAN", "PCG", "WFC", "C", "AGNC", "XOM", "GIS", "SHOP", "PBR-A", "S", "DISH", "ERIC", "PR", "LU", "HST", "DIS", "PTON", "ROIV", "IQ", "JD", "CSX", "ORCL", "SLB", "OXY", "ES=F", "NQ=F", "YM=F", )
selected_stock = st.sidebar.selectbox("Select company to forecast", stocks)
n_years = st.sidebar.slider("Years of prediction:", 1, 4)
period = n_years * 365






def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data

data_load_state = st.sidebar.text("Load data...")
data = load_data(selected_stock)
data_load_state.text("Loading data...done!")


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
st.write('Forecast Components')
fig2 = m.plot_components(forecast)
st.write(fig2)