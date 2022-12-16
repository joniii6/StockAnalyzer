# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 15:40:04 2022

@author: joklf
"""
import mplfinance as mpf
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import yfinance as yf


def index(Ticker):
	df = yf.Ticker(Ticker).history(period = 'ytd')
	df['Index'] = ((df["Close"] - df.iloc[0]["Close"]) / df.iloc[0]["Close"]) *100  + 100
	return df


def ytd(Ticker):
	df = yf.Ticker(Ticker).history(period = 'ytd')
	index_today = df.shape[0] -1
	ytd = (df.iloc[index_today]['Close'] - df.iloc[0]['Close']) / df.iloc[0]['Close'] *100
	return ytd

st.set_page_config(
    page_title="StockAnalyzer",
    page_icon="💸",
    layout="centered")

st.title("Stock Analyzer💸")
st.header("Welcome to our Webapp Stock Analyzer")
st.subheader("Use the sidebar to navigate through the app")

SP500 = index('^GSPC')
SMI = index('^SSMI')

fig, (ax1, ax2) = plt.subplots(1,2, sharex = True)
ax1.plot(SP500['Index'])
ax1.set(title = 'S&P 500 ytd')
ax2.plot(SMI['Index'])
ax2.set(title = 'SMI ytd')

for label in ax1.xaxis.get_ticklabels()[::2]:
	label.set_visible(False)

for label in ax2.xaxis.get_ticklabels()[::2]:
	label.set_visible(False)

ytdSP500 = ytd('^GSPC')
st.write(ytdSP500)

st.pyplot(fig)

col1, col2 = st.columns(2)

Eur = yf.Ticker('CHFEUR=X')
hist = Eur.history(period = 'ytd')
index = hist.shape[0] -1
col1.metric('Exchange Rate CHF/EUR', hist.iloc[index]['Close'], (hist.iloc[index]['Close'] - hist.iloc[index -1 ]['Close'])/hist.iloc[index - 1]['Close'])

USD = yf.Ticker('CHFUSD=X')
hist2 = USD.history(period = 'ytd')
col2.metric('Exchange Rate CHF/USD', hist2.iloc[0]['Close'], (hist2.iloc[0]['Close'] - hist2.iloc[1]['Close'])/hist2.iloc[1]['Close'])


