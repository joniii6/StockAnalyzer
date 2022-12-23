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

# Defining some general functions---------------------------------------------------------------------------------

# Definition Index Function-------------------------------

@st.cache(allow_output_mutation=True)
def index(ticker_string, ticker_list):

	df = yf.download(ticker_string, period = 'ytd')['Close']
	df = pd.DataFrame(df)

	if len(ticker_list) == 1:
		df = df.rename(columns = {'Close' : Ticker})

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

# Definition get news function-----------------------------

@st.cache(allow_output_mutation=True)
def get_a_page_of_headlines():
	API_TOKEN = 'XHEogdmXrGkHzMmW5uEA6fG4wohYfj4ZHR6bKI4D'
	params = urlencode(
		{'api_token': API_TOKEN, 'language': 'en', 'page': 'page'}
	)
	url = 'https://api.marketaux.com/v1/news/all?{}&language=en&api_token=XHEogdmXrGkHzMmW5uEA6fG4wohYfj4ZHR6bKI4D'
	r = requests.get(url)
	r.raise_for_status()
	json = r.json()
	titles = [x.get('title') for x in json['data']]
	description = [x.get('description') for x in json['data']]
	images = [x.get('image_url') for x in json['data']]
	url = [x.get('url') for x in json['data']]

	data = {'Title': titles, 
		'URL' : url, 'images':images, 'description':description}

	return (pd.DataFrame(data))

# Definition daily return function-----------------------------

@st.cache(allow_output_mutation = True)
def daily_return(ticker_string, ticker_list):

	df = index(ticker_string, ticker_list)
	last_value = df[df.shape[0]-1][0]
	prev_value = df[df.shape[0] -2][0]
	
	daily_return = (last_value-prev_value)/prev_value

	return prev_value
	
# Page configuration--------------------------------------------------------------------------------------

st.set_page_config(
    page_title='StockAnalyzer',
    page_icon='💸',
    layout='centered')

st.title('Welcome to Stock Analyzer💸')
st.markdown('Use the sidebar to navigate through the app')

# Section World Market Overview---------------------------------------------------------------------------

st.subheader('World Market Overview (Year to date)')

indices_tickers = '^GSPC ^SSMI ^IXIC ^N225 ^GDAXI ^FTSE'
indices_ticker_list = indices_tickers.split(' ')
indices_names = ['SP500', 'SMI', 'NASDAQ', 'NIKKEI', 'DAX', 'FTSE 100']

df = index(indices_tickers, indices_ticker_list)

df2 = ytd(indices_tickers, indices_ticker_list)

df3 = value_today(indices_tickers, indices_ticker_list,1)
df3['Name'] = indices_names
df3['YTD'] = df2['ytd_return'].values


fig, ax1 = plt.subplots()
ax1.plot(df)
ax1.legend(indices_names)
ax1.set_title('Returns of most common indices')
fig.set_size_inches(7, 5)

col1, col2, col3 = st.columns([3, 1. ,1.1])

col1.pyplot(fig)

for i in range (df3.shape[0]):
	if i < 3:
		col2.metric(df3.iloc[i]['Name'], df3.iloc[i]['value_today'],str(df3.iloc[i]['YTD']) + ' % ytd')
	else:
		col3.metric(df3.iloc[i]['Name'], df3.iloc[i]['value_today'],str(df3.iloc[i]['YTD']) + ' % ytd')


# Section Exchange Rates--------------------------------------------------------------------------------

st.subheader('Exchange rates')

ER_tickers = 'CHFEUR=X CHFUSD=X CHFJPY=X CHFGBP=X'
ER_tickers_list = ER_tickers.split(' ')
ER_names = ['CHF/EUR', 'CHF/USD','CHF/JPY','CHF/GBP']

df4 = value_today(ER_tickers, ER_tickers_list,3)
df4['Name'] = ER_names

df5 = ytd(ER_tickers, ER_tickers_list)
df4['YTD'] = df5.values

col1, col2, col3, col4 = st.columns(4)

for i in range(df4.shape[0]):
	if i == 0:
		col1.metric(df4.iloc[i]['Name'], df4.iloc[i]['value_today'], str(df4.iloc[i]['YTD']) + ' % ytd')
	if i == 1:
		col2.metric(df4.iloc[i]['Name'], df4.iloc[i]['value_today'], str(df4.iloc[i]['YTD']) + ' % ytd')
	if i == 2:
		col3.metric(df4.iloc[i]['Name'], df4.iloc[i]['value_today'], str(df4.iloc[i]['YTD']) + ' % ytd')
	if i == 3:
		col4.metric(df4.iloc[i]['Name'], df4.iloc[i]['value_today'], str(df4.iloc[i]['YTD']) + ' % ytd')

df6 = index(ER_tickers, ER_tickers_list)

daily_return = pd.DataFrame(columns = ['Daily_return'])

for i in df6.columns:
	daily_return.loc[i] = str(round(((df6.iloc[df6.shape[0]-1][i] - df6.iloc[df6.shape[0]-2][i]) / df6.iloc[df6.shape[0]-2][i]) *100,3)) + '% daily'

daily_return['Names'] = ER_names

for i in range(daily_return.shape[0]):
	if i == 0:
		col1.metric(daily_return.iloc[i]['Names'], value = '', delta = daily_return.iloc[i]['Daily_return'], label_visibility = 'collapsed')
	if i == 1:
		col2.metric(daily_return.iloc[i]['Names'], value = '', delta = daily_return.iloc[i]['Daily_return'], label_visibility = 'collapsed' )
	if i == 2:
		col3.metric(daily_return.iloc[i]['Names'], value = '', delta = daily_return.iloc[i]['Daily_return'], label_visibility = 'collapsed')
	if i == 3:
		col4.metric(daily_return.iloc[i]['Names'], value = '', delta = daily_return.iloc[i]['Daily_return'], label_visibility = 'collapsed')


# Section Commodities-----------------------------------------------------------------------------------

st.subheader('Commodities (Year to date)')

Comm_tickers = 'GC=F CL=F NG=F ZW=F'
Comm_tickers_list = Comm_tickers.split(' ')
Comm_names = ['Gold Feb 23', 'Crude Oil Jan 23', 'Natural Gas Jan 23', 'Wheat Jan 23']

df6 = value_today(Comm_tickers, Comm_tickers_list, 2)
df6['Name'] = Comm_names


df7 = ytd(Comm_tickers, Comm_tickers_list)
df6['YTD'] = df7.values

col1, col2, col3, col4 = st.columns(4)

for i in range(df6.shape[0]):
	if i == 0:
		col1.metric(df6.iloc[i]['Name'], df6.iloc[i]['value_today'], str(df6.iloc[i]['YTD']) + ' % ytd')
	if i == 1:
		col2.metric(df6.iloc[i]['Name'], df6.iloc[i]['value_today'], str(df6.iloc[i]['YTD']) + ' % ytd')
	if i == 2:
		col3.metric(df6.iloc[i]['Name'], df6.iloc[i]['value_today'], str(df6.iloc[i]['YTD']) + ' % ytd')
	if i == 3:
		col4.metric(df6.iloc[i]['Name'], df6.iloc[i]['value_today'], str(df6.iloc[i]['YTD']) + ' % ytd')



# Section Bonds-----------------------------------------------------------------------------------

st.subheader('US Treasury Bond Rates')

Bo_tickers = '^IRX ^FVX ^TNX ^TYX'
Bo_tickers_list = Bo_tickers.split(' ')
Bo_names = ['13 week Treasury Bill', 'Treasury Yield 5 Years', 'Treasury Yield 10 Years', 'Treasury Yield 30 Years',]

df6 = value_today(Bo_tickers, Bo_tickers_list, 2)
df6['Name'] = Bo_names

col1, col2, col3, col4 = st.columns(4)

for i in range(df6.shape[0]):
	if i == 0:
		col1.metric(df6.iloc[i]['Name'], str(df6.iloc[i]['value_today']) + ' %')
	if i == 1:
		col2.metric(df6.iloc[i]['Name'], str(df6.iloc[i]['value_today']) + ' %')
	if i == 2:
		col3.metric(df6.iloc[i]['Name'], str(df6.iloc[i]['value_today']) + ' %')
	if i == 3:
		col4.metric(df6.iloc[i]['Name'], str(df6.iloc[i]['value_today']) + ' %')


# Section News-------------------------------------------------------------------------------------------

st.subheader('Latest News')

try:
	a = get_a_page_of_headlines()

	col1, col2, col3 = st.columns(3)

	
	col1.image(a.iloc[0]['images'], use_column_width = True, caption = a.iloc[0]['Title'])
	col1.caption(a.iloc[0]['description'])
	col1.caption(a.iloc[0]['URL'])
	col2.image(a.iloc[1]['images'], use_column_width = True, caption = a.iloc[1]['Title'])
	col2.caption(a.iloc[1]['description'])
	col2.caption(a.iloc[1]['URL'])
	col3.image(a.iloc[2]['images'], use_column_width = True, caption = a.iloc[2]['Title'])
	col3.caption(a.iloc[2]['description'])
	col3.caption(a.iloc[2]['URL'])
except:
	st.error('The website has reached 100 news requests today which is the limit of our API license :(  \n''Try again tomorrow!')
	



