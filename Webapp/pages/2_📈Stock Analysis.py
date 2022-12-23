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
		df = df.rename(columns = {'Close' : ticker_list[0]})

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

def getROE(Ticker):

	stock = yf.Ticker(Ticker)
	
	IS = stock.income_stmt
	BS = stock.balance_sheet
	
	net_inc_common1 = IS.loc['Net Income'][0]
	tot_equity_now = BS.loc['Stockholders Equity'][0]
	tot_equity_previous = BS.loc['Stockholders Equity'][1]

	Average_equity = (tot_equity_now + tot_equity_previous)/2

	ROE = round(net_inc_common1/Average_equity *100, 2)

	return f'{ROE}%' 

# Definition get info function------------------------------

def get_info(Ticker):
	Stock = yf.Ticker(Ticker)
	Name = Stock.info["longName"]
	trailing_PE = round(Stock.info['trailingPE'],2)
	ebitda = round(Stock.info['ebitda'] /1000000, 2)
	rec = Stock.recommendations
	div = Stock.dividends
	ISIN = Stock.isin
	BS = Stock.info['longBusinessSummary']
	mh = Stock.major_holders
	ih = Stock.institutional_holders
	sust = Stock.sustainability
	price = Stock.info['currentPrice']
	div = Stock.dividends
	rev = round(Stock.financials.loc['Total Revenue'][0] / 1000000,2)
	
	return trailing_PE, ebitda, Stock, rec, div, ISIN, BS, mh, ih, sust, price, div, Name, rev

# Definition getCAGR function------------------------------

def getCAGR(start, end, periods):
	cagr = round(((end/start)**(1/periods)-1)*100,2)

	return f'{cagr} %'

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
	error = False

except:
	if Ticker == '':
		st.error("Please enter a valid ticker!")
		error = True
	else:
		st.error(f'{Ticker} is not a valid ticker. Please enter a valid ticker!')
		error = True

st.subheader('Financial information')

col1, col2, col3 = st.columns([3, 1, 1.1])

if error == True:
	st.write('Define a valid ticker')
else:
	try:
		trailing_PE, ebitda, Stock, rec, div, ISIN, BS, mh, ih, sust, price, div, Name, rev = get_info(Ticker)

		roe = getROE(Ticker)

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
		col3.write(f' {Stock.info["longName"]}')
		col3.metric("Revenue in Million", rev)
		col3.metric("Ebitda in Million", ebitda)
		col3.metric("Return on Equity", roe)
		
	except:
		pass

if error == True:
	st.write('Define a valid ticker')
else:
	try:
		earnings = Stock.earnings
		xvals = earnings.index
		fig2, ax1 = plt.subplots()
		ax1.bar(xvals -0.15, earnings["Earnings"] / 1000000, label = "Earnings", width = 0.3)
		ax1.bar(xvals + 0.15, earnings["Revenue"] / 1000000, label = "Revenue", width = 0.3)
		ax1.legend()
		ax1.set_title("Revenue vs Earnings ")
		ax1.set_ylabel("Revenue/Earnings in Millions")
		ax1.ticklabel_format(useOffset=False, style = 'plain')
		plt.xticks(ticks = xvals)

		periods = len(earnings.index)

		start_revenue = earnings.iloc[0]['Revenue']
		start_earnings = earnings.iloc[0]['Earnings']

		end_revenue = earnings.iloc[-1]['Revenue']
		end_earnings = earnings.iloc[-1]['Earnings']

		revenue_cagr = getCAGR(start_revenue,end_revenue,periods)
		earnings_cagr = getCAGR(start_earnings, end_earnings, periods)

		col1,col2 = st.columns(2)
		col1.pyplot(fig2)
		col2.metric("CAGR Revenue", revenue_cagr)
		col2.metric('CAGR Earnings', earnings_cagr)

	except:
		st.write('There are no information on the earnings available for this ticker')

# General Company Information--------------------------------------------------------------------------------------
try:
	st.subheader(f'General company information for {Name}')
except:
	st.subheader('General company information')



if error == True:
	st.write('Define a valid ticker')
else:
	with st.expander(f"Show me the business description for {Name}"):
		try:
			st.caption(BS)
		except:
			st.write('Unfortunately no data has been found to display a business description')

col1, col2 = st.columns(2)

col1.write("Sustainability")
col2.write("Major Holders")

try:
	col1.caption(f' {Name} has an overall ESG-Score of {sust.loc["totalEsg"]["Value"]}')
		
except:
	col1.caption(f'There are no sustainability information available for {Name}.')


## Which more information??

if error == True:
	st.write('Define a valid ticker')

else:
	try:
		top5 = ', '.join(ih[:5]['Holder'])
		col2.caption(f' {mh.iloc[0][0]} of the shares are held by insiders.')
		col2.caption(f' {mh.iloc[1][0]} of the shares are held by institutions.')
		col2.caption(f' The top five institutional holders are {top5}')
		
	except:
		st.write("No information on major holders available")

st.write("Analyst recommendations of the last six months")

try:
	col1, col2 = st.columns(2)

	rec6m = rec[(rec.index.month >= (rec.index.month[-1] -6)) & (rec.index.year == (rec.index.year[-1]))]

	col1.dataframe(rec6m["To Grade"].value_counts())
	
except:
	st.write("No analyst recomemendations available")
# Benchmarking--------------------------------------------------------------------------------------

st.subheader("Benchmark")

indices_tickers = '^GSPC ^SSMI ^IXIC ^N225 ^GDAXI ^FTSE'
indices_ticker_list = indices_tickers.split(' ')
indices_names = ['SP500', 'SMI', 'NASDAQ', 'NIKKEI', 'DAX', 'FTSE 100']

dict_ind = dict(zip(indices_names,indices_ticker_list))

choice = st.multiselect("Choose some indices to benchmark against your stock", indices_names, default = 'SMI')

Tickers_used_str = ''

try:
	for i in choice[:-1]:
		Tickers_used_str += dict_ind.get(i) + ' '
	Tickers_used_str += dict_ind.get(choice[-1])

	Tickers_used = Tickers_used_str.split(' ')
	Tickers_used = list(filter(None, Tickers_used))

	Indices_used = index(Tickers_used_str, Tickers_used)

	try:
		Stock_used = index(Ticker, Ticker_list)
	except:
		st.write("Enter a valid ticker")

	if len(choice) == 1:
		choice = choice[0]

	fig, ax = plt.subplots()
	try:
		ax.plot(Stock_used, label = Ticker)
	except:
		pass


	ax.plot(Indices_used, label = choice)
	ax.legend()
	ax.set_title('Benchmark your Stock against some Indices')
except:
	st.write("No Data for Benchmark available")

try:
	Tickers_used_str += ' ' + Ticker
	Tickers_used.append(Ticker)

	ytd_benchmarks = ytd(Tickers_used_str, Tickers_used)

	choice = list(choice)

	Names = []

	for i in choice:
		Names.append(i)

	Names.append(Name)


	ytd_benchmarks['Name'] = Names

	col1,col2,col3 = st.columns([3,1,1.1])

	col1.pyplot(fig)

	for i in range(len(ytd_benchmarks.index)):
		if i <= 3:
			col2.metric(f'YtD {ytd_benchmarks.iloc[i]["Name"]}', f' {ytd_benchmarks.iloc[i]["ytd_return"]} %')
		else:
			col3.metric(f'YtD {ytd_benchmarks.iloc[i]["Name"]} ',  f' {ytd_benchmarks.iloc[i]["ytd_return"]} %')
except:
	st.write("No YtD Data for Benchmarks available")


## News --------------------------------------------------------------------------------------
try:
	st.subheader(f' Latest news on {Name}')
except:
	st.subheader('Latest news')

if error == True:
	st.write('Define a valid Ticker')
else:
	try:
		titles = ([x.get('title') for x in Stock.news])

		urls = ([x.get('link') for x in Stock.news])

		col1, col2, col3 = st.columns(3)

		col1.write(titles[0])
		col1.write(urls[0])

		col2.write(titles[1])
		col2.write(urls[1])

		col3.write(titles[2])
		col3.write(urls[2])
	except: 
		st.write('No News are available for this Ticker')


	