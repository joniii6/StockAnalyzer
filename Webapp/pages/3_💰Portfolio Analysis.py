import datetime as dt
import math	 	 
import matplotlib.pyplot as plt
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
		df = df.rename(columns = {'Close' : ticker_list[0]})

		x = 0
		while math.isnan(df.iloc[x]) == True:
			x += 1
		else:
			df[f'Index {Ticker}'] = ((df - df.iloc[x]) / df.iloc[x]) *100  + 100

	else:
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

	if len(ticker_list) == 1:
		
		index_today = df.shape[0] -1
	
		while math.isnan(df.iloc[index_today]) == True:
			index_today -= 1
		else:
			table_today.at[ticker_list[0], 'value_today'] = round(df.iloc[index_today], r)
	
	else:
		for i in ticker_list:
			index_today = df.shape[0] -1
	
			while math.isnan(df.iloc[index_today][i]) == True:
				index_today -= 1
			else:
				table_today.at[i, 'value_today'] = round(df[i].iloc[index_today], r)

	return table_today


st.set_page_config(
    page_title='StockAnalyzer',
    page_icon='💸',
    layout='centered')


st.title('Portfolio Analysis')
st.markdown('Use the sidebar to navigate through the app')

st.subheader("Portfolio Overview")

stocks_tickers = st.text_input('Enter your tickers seperated with a **space**!')
stocks_ticker_list = stocks_tickers.split(' ')

stocks_names = []

try:
	for i in stocks_ticker_list:
		stocks_names.append(yf.Ticker(i).info["longName"])
except:
	if stocks_tickers == '':
		st.error("Enter at least two valid tickers")
	else:
		st.error("At least one of the Tickers is not valid")
try:
	df = index(stocks_tickers, stocks_ticker_list)

	df2 = ytd(stocks_tickers, stocks_ticker_list)

	df3 = value_today(stocks_tickers, stocks_ticker_list,2)
	df3['Name'] = stocks_names
	df3['YTD'] = df2['ytd_return'].values


	fig, ax1 = plt.subplots()
	ax1.plot(df)
	ax1.legend(stocks_names, loc = 3)
	ax1.set_title('Returns of your portfolio indexed')
	fig.set_size_inches(7, 5)

	col1, col2, col3 = st.columns([3, 1. ,1.1])

	col1.pyplot(fig)

	for i in range(df3.shape[0]):
		if i <= (df3.shape[0] /2 ):
			col2.metric(df3.iloc[i]['Name'], df3.iloc[i]['value_today'],str(df3.iloc[i]['YTD']) + ' % ytd')
		else:
			col3.metric(df3.iloc[i]['Name'], df3.iloc[i]['value_today'],str(df3.iloc[i]['YTD']) + ' % ytd')

except:
	st.write("No overview for your portfolio available")


st.subheader("Build your optimal portfolio")
st.caption("Add explanation of the process of building the optimal portfolio")

Investment_Amount = st.number_input("Select how much money you want to invest in your portfolio", min_value = 1000, step = 1000)

try:
	portfolio = yf.download(stocks_tickers, period = '10y')['Close']

	mu = mean_historical_return(portfolio)

	S = CovarianceShrinkage(portfolio).ledoit_wolf()

	ef = EfficientFrontier(mu, S)

	raw_weights = ef.max_sharpe()

	cleaned_weights = ef.clean_weights()


	latest_prices = get_latest_prices(portfolio)

	da = DiscreteAllocation(cleaned_weights, latest_prices, total_portfolio_value= Investment_Amount)

	allocation, leftover = da.greedy_portfolio()

	alloc = pd.DataFrame.from_dict(allocation, orient = 'index')
	alloc['Last price'] = round(latest_prices,2)
	alloc['Investment'] = round(alloc[0] * alloc['Last price'],2)


	alloc.rename(columns = { 0: '# shares' }, inplace = True)
	new_row = ['-','-',leftover]
	alloc.loc['Cash'] = new_row


	labels = alloc.index.tolist()
	sizes = alloc['Investment']

	col1, col2 = st.columns(2)

	fig1, ax1 = plt.subplots()
	ax1.pie(sizes,  autopct = '%1.1f%%')
	ax1.axis('Equal')
	ax1.set_title('Your optimal Portfolio')
	ax1.legend(labels)
	col1.pyplot(fig1)

	col2.dataframe(alloc)

except:
	st.write("Unfortunately we were not able to calculate the optimal portfolio for you")

