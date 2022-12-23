# StockAnalyzer

“Stock Analyzer” was created within the framework of the course: “Introduction to Programming” by Mario Sillic at the University of St.Gallen. The aim of “Stock Analyzer” was to build a web application on which market data and stock information were more accessible for interested parties.

![image](https://user-images.githubusercontent.com/121302353/209364952-75124495-527d-4968-b34a-dd2b199955e8.png)


### Table of Contents  
[1.) Introduction](#headers)  
[2.) Running the Project](#headers)  
[3.) Navigating the Webapp](#headers)  
[4.) Appendix](#headers)  
<a name="headers"/>


## 1.) Introduction

Have you ever felt like some investment platforms just are not user friendly enough?   

Most of the time all kinds of information are displayed for various financial instruments, however not all of them provide useful data to derive efficient investment decisions. This somewhat lack of overview led us to create “Stock Analyzer'' : A summarised web application with key numbers and company information we feel crucial to have access to from an investors perspective. By gathering information on historic data, company information and key financial ratios, the idea of the application was to provide potential investors with the toolkit to make data-backed investment decisions.

This Project was developped by:
- Jonas Kleubler
- Flavia Lopreno
- Laurin Tröhler

## 2.) Running the project

Jonas da muesch nomal ran

## 3.) Navigating the Webapp

To show gathered and manipulated data in a user friendly way. app has different features across its four pages


### Markets Today


### Stock Analysis



### Portfolio Analysis

The portfolio building section of the Webapp, allows the user to build an optimal portfolio allocation, given a certain combination of stocks. The tool requires two different inputs. Firstly, the user needs to add the tickers of stocks, which he would like to have in his portfolio. As a second input, one must select the available financial ressources. This allows for the creation of an optimal allocation, given a certain financial allowance.

After the selection of the preferred stocks, the user wants to have in its portfolio, the code gatheres historic financial stock data from the last ten years. To find an optimal weighting, we compute the covariance matrix of the selected stocks and their average returns. Using the principles of the efficient frontier, the webapp computes various portfolios with different weights composed of the selected stocks, which give the highest possible return, given a certain level of risk, which is measured in standard deviation. Ultimately we want to find the one portfolio lying on the efficient frontier, which maximises the sharpe ratio, as this indicates better portfolio performance. By doing these calculations, we end up with an optimal portfolio allocation, which tells us how much of each stock to buy given a certain resource allowance. 






### About us

The last page of our Webapp, shows some basic information on the three creators of this Project. It provides information on the team's previous endeavours and it's reasonings behind the overlapping interests of finance and programming. 

## 4.) Appendix
















