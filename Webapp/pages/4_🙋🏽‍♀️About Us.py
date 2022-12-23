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

st.title("About us")
st.subheader("Get to know our developper team")

st.image('https://miro.medium.com/max/1187/1*0FqDC0_r1f5xFz3IywLYRA.jpeg')



st.write("##### Hey - I'm Jonas.")
st.write("I was born and raised in Basel and am now studying business administration at the University of St.Gallen. I have always seen a great potential in learning a programming language, due to its growing importance in nowadays society. When I saw that HSG offered different courses within the programming field, I decided to apply for the Data Science Fundamentals course. There I was introduced to R for the first time. Being fascinated by its potentials I then chose to register for two other compulsory elective subjects which were related to programming: “Business analytics and Data Science applications” and “Data Handling”. I am a firm believer that you can never learn enough about coding which is why I saw this project as a great opportunity to dive into a topic that interests me and parallelly learn more about Python. ")

st.write("##### Hey - I'm Laurin.")
st.write("I was born and raised in Zurich and am now studying economics at the University of St.Gallen. I have always been intrigued by financial markets and their investment opportunities. Which is why next to uni I work 60% at LGT Capital in the private equity and venture capitalist sector. Seeing the fast growing pace of companies based on fintech I see it as a necessity to understand the core basics of technologies such as Python or R. The university of St.Gallen offers a variety of courses which fulfil my wish to learn how to code. So far I have attended both the Data Science Fundamental course and the Data Handling lecture. ")

st.write("##### Hey - I'm Flavia.")
st.write("I was born and raised in Zurich where I graduated in 2019. Instead of travelling around the world during my gap year, I attended the assessment year in the field of mechanical engineering at the technical university (ETH) in Zurich. There I took part in the compulsory lecture: Introduction into programming - C++. Although it only lasted for a semester, I found the pleasure in coding (although on a very basic level of course). At HSG I am currently studying business administration.")

