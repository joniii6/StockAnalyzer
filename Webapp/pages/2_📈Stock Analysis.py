import datetime as dt
import math	 	 
import matplotlib.pyplot as plt
import mplfinance as mpf
import numpy as np
import pandas as pd
from	pypfopt import EfficientFrontier
from	pypfopt import risk_models
from	pypfopt import expected_returns
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices
from	pypfopt.expected_returns import mean_historical_return
from	pypfopt.risk_models	import CovarianceShrinkage
import requests
import seaborn as sns
import sklearn 	 
import streamlit as st
from	urllib.parse import urlencode
import yfinance as yf

# Defining some functions---------------------------------------------------------------------------------

# Definition Index Function-------------------------------

@st.cache(allow_output_mutation=True)
def index(ticker_string, ticker_list):

	df = yf.download(ticker_string, period = 'ytd')['Close']
	df = pd.DataFrame(df)

	if len(ticker_list) == 1:
		df = df.rename(columns = {"Close" : Ticker})

	for i in ticker_list:
		x = 0
		while math.isnan(df.iloc[x][i]) == True:
			x += 1
		else:
			df[f'Index {i}'] = ((df[i] - df.iloc[x][i]) / df.iloc[x][i]) *100  + 100
	df.drop(ticker_list, axis = 1, inplace = True)
	df.fillna(method = 'ffill', inplace = True)
	df.fillna(method = 'bfill', inplace = True)
	return df

## Talk about how to deal with NAS!!!


# Definition year to date function------------------------

@st.cache(allow_output_mutation=True)
def ytd(ticker_string, ticker_list):

	df = index(ticker_string, ticker_list)

	ticker_list_ind = list(df.columns)
	
	ytd = pd.DataFrame(columns = ['ytd_return'], index = ticker_list_ind )

	last_index = df.shape[0] -1

	for i in ticker_list_ind:
		
		ytd.at[i, 'ytd_return'] = round(df.iloc[last_index][i] - df.iloc[0][i],2)
		
	return ytd
	

# Definition value today function--------------------------

@st.cache(allow_output_mutation=True)
def value_today(ticker_string, ticker_list, r):

	df = yf.download(ticker_string, period = 'ytd')['Close']

	table_today = pd.DataFrame(columns = ['value_today'], index = ticker_list)
	
	for i in ticker_list:
		index_today = df.shape[0] -1
	
		while math.isnan(df.iloc[index_today][i]) == True:
			index_today -= 1
		else:
			table_today.at[i, 'value_today'] = round(df[i].iloc[index_today], r)

	return table_today

# Definition Return on Equity function ---------------------

#def getROE(Ticker):

	#stock = yf.Ticker(Ticker)
	
	#IS = stock.income_stmt
	#BS = stock.balance_sheet
	
	#net_inc_common1 = IS.loc['Net Income'][0]
	#tot_equity_now = BS.loc['Stockholders Equity'][0]
	#tot_equity_previous = BS.loc['Stockholders Equity'][1]

	#Average_equity = (tot_equity_now + tot_equity_previous)/2

	#ROE = round(net_inc_common1/Average_equity *100, 2)

	#return f'{ROE}%' #return on equity

#st.write(getROE('MSFT'))


# Definition get info function------------------------------

def get_info(Ticker):
	Stock = yf.Ticker(Ticker)
	Name = Stock.info["longName"]
	trailing_PE = round(Stock.info['trailingPE'],2)
	ebitda = str(round(Stock.info['ebitda'] /1000000, 2))
	rec = Stock.recommendations
	div = Stock.dividends
	ISIN = Stock.isin
	BS = Stock.info['longBusinessSummary']
	mh = Stock.major_holders
	ih = Stock.institutional_holders
	sust = Stock.sustainability
	price = Stock.info['currentPrice']
	div = Stock.dividends
	
	return trailing_PE, ebitda, Stock, rec, div, ISIN, BS, mh, ih, sust, price, div, Name


# Page configuration------------------------------------------------------------------------------

st.set_page_config(
    page_title="StockAnalyzer",
    page_icon="💸",
    layout="centered")


# Financials--------------------------------------------------------------------------------------

st.title("Here you can analyze your stock")
st.subheader("Use the sidebar to navigate through the app")

Ticker = st.text_input("Enter your Ticker")
Ticker_list = [Ticker]

try:
	df = index(Ticker, Ticker_list)

except:
	if Ticker == '':
		st.error("Please enter a valid ticker!")
	else:
		st.error(f'{Ticker} is not a valid ticker. Please enter a valid ticker!')

st.subheader('Some financial information')

col1, col2, col3 = st.columns([3, 1, 1.1])

try:
	trailing_PE, ebitda, Stock, rec, div, ISIN, BS, mh, ih, sust, price, div, Name = get_info(Ticker)

	choice = st.radio('Choose your period', options = ["Year to date", "1 year", "5 years", "10 years", "Max"], horizontal = True)

	dictionary = {"Year to date" : "ytd", "1 year" : "1y", "5 years" : "5y", "10 years" : "10y", "Max" : "max"}

	period = dictionary.get(choice)

	df = yf.Ticker(Ticker).history(period = period)

	fig, ax1 = plt.subplots()
	ax1.plot(df["Close"])
	ax1.set_title(f' {Name} {choice}')

	col1.pyplot(fig)

	col2.image(Stock.info['logo_url'])
	col2.metric("Current Price", price)
	col2.metric("Trailing PE", trailing_PE)
	col3.metric("Ebitda in Million", ebitda)
	col3.metric("Return on Equity", 'ROE')
	col3.metric("Revenue", 45)
	col3.dataframe(div)

except:
	st.write("No Ticker selcted")

# General Company Information--------------------------------------------------------------------------------------
try:
	st.subheader(f'General company information for {Name}')
except:
	st.subheader('General company information')

col1, col2 = st.columns(2)



with st.expander(f"Show me the business description for {Name}"):
	try:
		st.caption(BS)
	except:
		st.write('Unfortunately no data has been found to display a business description')

col1.write("Sustainability")

try:
	col1.caption(f' {Name} has an overall ESG-Score of {sust.loc["totalEsg"]["Value"]}')
except:
	col1.caption(f'There are no sustainability information available for {Name}.')


## Which more information??

try:
	col2.write("Major Holders")
	col2.caption(f' {mh.iloc[0][0]} of the shares are held by insiders.')
	col2.caption(f' {mh.iloc[1][0]} of the shares are held by institutions.')
	col2.caption(f' The top five institutional holders are { ih.iloc[:5]["Holder"] }')
	st.dataframe(mh)
	st.dataframe(ih)
	st.dataframe(sust)
	st.write(rec['To Grade'].value_counts())

except:
	st.write("No Ticker selected")

st.write("Analyst recommendations")
col1, col2 = st.columns(2)

col1.dataframe(rec["To Grade"].value_counts().loc[['Buy', 'Hold', 'Sell']])
col2.dataframe(rec)


# Benchmarking--------------------------------------------------------------------------------------

st.subheader("Benchmark")

indices_tickers = '^GSPC ^SSMI ^IXIC ^N225 ^GDAXI ^FTSE'
indices_ticker_list = indices_tickers.split(' ')
indices_names = ['SP500', 'SMI', 'NASDAQ', 'NIKKEI', 'DAX', 'FTSE 100']

dict_ind = dict(zip(indices_ticker_list, indices_names))

st.write(dict_ind)

choice = st.multiselect("Choose some indices to benchmark", indices_names)

st.write(choice)

Tickers_used = []

for i in choice:
	Tickers_used.append(dict_ind.get(i))

st.write(Tickers_used)


Tickers_used_str = ''	                      
for i in Tickers_used:
	Tickers_used_str += i


Stock2 = index(Tickers_used_str, Tickers_used)
st.dataframe(Stock2)

fig, ax = plt.subplots()
#ax.plot(Stock1_ind['Index'], label = Ticker)
ax.plot(Stock2, label = Ticker2)
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


# News --------------------------------------------------------------------------------------

st.subheader("News")

titles = []
titles.append([x.get('title') for x in Stock.news])

st.write(titles)
