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

st.title("Here you can build your optimal portfolio")
st.subheader("Use the sidebar to navigate through the app")

portfolio = []

stocks = st.text_area("Enter the Tickers you want to add to your Portfolio. Seperate them with a comma and without a space!")

portfolio = stocks.split(", ")

#for i in portfolio:
	Stock = yf.Ticker(i)
	hist = Stock.history(period = "max")
	


