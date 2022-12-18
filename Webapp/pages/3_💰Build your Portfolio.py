import mplfinance as mpf
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import yfinance as yf
from datetime import datetime as dt
from pypfopt import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt.expected_returns import mean_historical_return
from pypfopt.risk_models import CovarianceShrinkage
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices
import sklearn


def index(Ticker):
	df = yf.Ticker(Ticker).history(period = 'ytd')
	df['Index'] = ((df['Close'] - df.iloc[0]['Close']) / df.iloc[0]['Close']) *100  + 100
	return df

def ytd(Ticker):
	df = yf.Ticker(Ticker).history(period = 'ytd')
	index_today = df.shape[0] -1
	ytd = (df.iloc[index_today]['Close'] - df.iloc[0]['Close']) / df.iloc[0]['Close'] *100
	return ytd

def value_today(Stock):
	index_today = Stock.shape[0] -1
	today = Stock.iloc[index_today]['Close']
	return round(today,2)

st.set_page_config(
    page_title='StockAnalyzer',
    page_icon='💸',
    layout='centered')


st.title('Here you can build your optimal portfolio')
st.markdown('Use the sidebar to navigate through the app')

String = st.text_input('Enter your tickers seperated with a space!')
Investment_Amount = st.slider("Select the amount you want to invest", 1000, 1000000, value = 100000, step = 1000)

Tickers = String.split(' ')

# Add Something to deal with empty data
try:
	portfolio = yf.download(String, period = '10y')['Close']

	mu = mean_historical_return(portfolio)

	S = CovarianceShrinkage(portfolio).ledoit_wolf()

	ef = EfficientFrontier(mu, S)

	raw_weights = ef.max_sharpe()

	cleaned_weights = ef.clean_weights()


	latest_prices = get_latest_prices(portfolio)

	da = DiscreteAllocation(cleaned_weights, latest_prices, total_portfolio_value= Investment_Amount)

	allocation, leftover = da.greedy_portfolio()

	alloc = pd.DataFrame.from_dict(allocation, orient = 'index')
	alloc['Last price'] = latest_prices
	alloc['Investment'] = alloc[0] * alloc['Last price']
	new_row = ['-','-',leftover]
	alloc.loc['Cash'] = new_row


	labels = alloc.index.tolist()
	sizes = alloc['Investment']

	fig1, ax1 = plt.subplots()
	ax1.pie(sizes,  autopct = '%1.1f%%')
	ax1.axis('Equal')
	ax1.set_title('Your optimal Portfolio')
	ax1.legend(labels)
	st.pyplot(fig1)

except:
	st.error("Please enter at least two valid tickers")