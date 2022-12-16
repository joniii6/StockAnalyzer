import mplfinance as mpf
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import yfinance as yf

@st.cache(allow_output_mutation=True)
def index(Ticker):
	df = yf.Ticker(Ticker).history(period = 'ytd', interval = '1d')
	df['Index'] = ((df["Close"] - df.iloc[0]["Close"]) / df.iloc[0]["Close"]) *100  + 100
	return df

@st.cache(allow_output_mutation=True)
def ytd(Ticker):
	df = yf.Ticker(Ticker).history(period = 'ytd')
	index_today = df.shape[0] -1
	ytd = (df.iloc[index_today]['Close'] - df.iloc[0]['Close']) / df.iloc[0]['Close'] *100
	return ytd

st.title("Here you can analyze your stock")

Ticker = st.text_input("Enter your Ticker")


Stock1_ind = index(Ticker)
Stock1 = yf.Ticker(Ticker)

with st.expander("Show me the business description"):
    text = Stock1.info["longBusinessSummary"]
    st.write(text)

st.subheader('Some financial information')
col1, col2, col3, col4 = st.columns(4)
col1.metric("PERatio", 45, "80%")
col2.metric("Ebitda", 45000000, "25%")
col3.metric("Profit", 45)
col4.metric("Revenue", 45)



st.subheader("Benchmark")

choice = st.radio("Choose an index to benchmark", ['SP500', 'SMI'])

if choice == "SP500":
	Ticker2 = '^GSPC'

elif choice == 'SMI':
	Ticker2 = '^SSMI'                         


Stock2 = index(Ticker2)

fig, ax = plt.subplots()
ax.plot(Stock1_ind['Index'], label = Ticker)
ax.plot(Stock2['Index'], label = Ticker2)
ax.legend()
ax.set_title("Benchmark")
st.pyplot(fig)

e = Stock1.earnings
xvals = e.index
fig2, ax1 = plt.subplots()
ax1.bar(xvals -0.15, e["Earnings"], label = "Earnings", width = 0.3)
ax1.bar(xvals + 0.15, e["Revenue"], label = "Revenue", width = 0.3)
ax1.legend()
ax1.set_title("Revenue vs Earnings")
ax1.set_ylabel("Revenue/Earnings")
ax1.ticklabel_format(useOffset=False, style = 'plain')
plt.xticks(ticks = xvals)
st.pyplot(fig2)

fig3, ax  = plt.subplots()
mpf.plot(Stock1_ind, type = 'candle', ax=ax, mav = (3,6,9))
#mpf.plot(Stock2, type = 'candle', ax=ax, mav = (3,6,9))
ax.set_title('Candle Chart')
st.pyplot(fig3)



