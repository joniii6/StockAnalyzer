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

In order to show and analyze the data, we have created a Webapp with different funcionalities and features across four different pages, which are being described in the following sections.

### Markets Today

The Markets Today page is the first page the user is confronted with. Since graphs appear to catch the users attention, we wanted to create a graphical homepage. In order to do so we displayed a world market overview with six indexes of our choice: SP500, SMI, NASDAQ, NIKKEI, DAX and FTSE 100. Surrounding this graph you can find current and their year-to-date (YTD) volatility. In addition we decided to show US treasury bond rates and added commodities since we thought they were just as important.Last but not least, scrolling down the page you will find the latest news.   

How do the codes on the page run and work: 
The code imports several libraries, including yfinance, streamlit, and pandas. In a first step we defined some functions that perform various tasks related to stock analysis and financial news: 

The `Index` function takes a ticker string and a list of tickers as input, and returns a Pandas DataFrame containing the performance of each ticker in the list relative to its starting value (expressed as a percentage change). 

The `ytd` function takes a ticker string and a list of tickers as input, and returns a Pandas DataFrame containing the YTD return for each ticker in the list (also expressed as a percentage change). 
     
The `value_today` function takes a ticker string, a list of tickers, and a rounding value as input, and returns a Pandas DataFrame containing the current value of each ticker in the list, rounded to the specified number of decimal places.
     
And lastly the `get_a_page_of_headlines` function retrieves a page of headlines from a financial news API and returns the list of headlines.
     
As a next step we build functions to create each individual section: market overview, bonds, commodities, exchange rates and news. 
    
The Section Bond obtains data about US Treasury bond rates using the value_today function and displays the data in the Streamlit app. The data is displayed in four columns, with each column showing the name and current value of a different bond rate. The bond rate data is obtained from a DataFrame. 
     
The commodity section gathers data about the YTD performance and current values of various commodities using the `value_today` and `ytd` functions. The data is then displayed in a Streamlit app in four columns, with each column showing the name, current value, and YTD performance of a different commodity. The commodity data is retrieved from two DataFrames.
      
For both the section: bond and the commodity section metric functions are used to display the data in the Streamlit app. 
        
The data in the exchange rate section is displayed in four columns, with each column showing the name, current value, and YTD performance of a different exchange rate. The corresponding data is retrieved from two DataFrames and the metric function is used to display the data in the Streamlit app. The code also calculates the daily returns for each exchange rate using the index function and displays this data in the Streamlit app using the metric function. 
        
For the news section we used the `get_a_page_of_headlines` function. The code creates three columns in the Streamlit app and populates each column with the image, title, description, and URL for a different news headline. If an error occurs during the execution of the code, an error message is displayed in the Streamlit app.   
        
In all five codes a subheading was added to the app using the st.subheader function.

### Stock Analysis

The “stock analysis” section was created to sustain current or potential investors whilst making an investment decision. The page displays a variety of data both numerical and alphabetical which should help decide whether or not a company is worth investing in.    
There are four figures shown within the numerical section. All related to financial benefits for investors: dividends, return on equity, earnings per share and price-to-earnings (P/E) ratio.    

The non-numerical data consists of internally processed data as well as externally provided data. Internally processed data, reflects data provided by the company herself, such as sustainability related data and tables of the major holders of the company or the major institutional holders. External data however consists of data provided by external parties who are either shareholders themselves who are keen on giving a recommendation on whether or not to execute a purchase or sale, or are interested in the company for other reasons, such as i.e. publishing a great storyline (journalists).   

How do the codes on the page run and work: 
This code is a script that uses several libraries to perform various tasks related to financial data analysis. The script starts by importing a number of libraries and defining some functions.   
The first three functions: `Index` function, `ytd` function and `value_today` function fetch and process financial data for a specified set of tickers.   
      
The next function calculates the return on equity (ROE) for a given ticker (e.g MSFT-microsoft) by using financial data from Yahoo Finance: getROE. Since the ROE was not directly extractable from the balance sheet or income statement we had to code the function ourselves. However the function does retrieve data from the income statement and balance sheet for the ticker, in order to then calculate the average equity over the past two periods, and return the ROE as a percentage.  
      
The fifth function, `get_info` function, fetches information about a stock with a given ticker symbol. It uses the Ticker function of the yfinance library to gather information about the stock, including the stock's name, P/E ratio, EBITDA, recommendations, dividends, ISIN number, business summary, major and institutional holders, sustainability data, current price, dividends, and total revenue. The function then returns all of these information as a tuple.   
       
The sixth function used, is a Streamlit app function that allows users to input a stock ticker (e.g AAPL), retrieve financial information and plot graphs related to the stock. The app first takes in a ticker as user input and stores it in the Ticker variable. It then attempts to collect data for the ticker using the index() function, and if the ticker is not valid, an error message is displayed to the user. The function then retrieves further financial information for the ticker using the get_info() function, which uses the yfinance library to obtain information about the stock. The app then allows users to choose a period for which to plot a graph of the stock's closing price, and plots the graph using matplotlib. Finally, the function plots a bar chart showing the company's revenue and earnings over time, and calculates and displays the compound annual growth rate (CAGR) for both revenue and earnings. 
The seventh function General Company Information was used to obtain company information.  
          
Furthermore we created a code Benchmarking which enabled our webapp users to compare different tickers to each other. The code first obtains the tickers for various indices and their corresponding names. It then allows users to select some indices from a list of names using a multi-select widget.
The code then plots the stock and selected indices on the same graph to compare their performance. It also calculates the YTD return for the stock and selected indices and displays the values in separate metrics widgets. If there is an error in obtaining the data for the stock or indices (e.g. if the ticker is invalid), an error message is displayed.   
         
Since news articles have a big impact on investors decision making we decided to include a function retrieving articles too. This code tries to display the latest news articles related to a specific stock, represented by the variable Ticker. It first redeems the news articles and their associated URLs using the Stock.news attribute of the yfinance library. Then it displays the titles and URLs of the latest three news articles in three separate columns. In case there are no news articles available or if there is an error in retrieving the news articles, it will display a message saying "No News are available for this Ticker".  
      
### Portfolio Analysis

The portfolio building section of the Webapp, allows the user to build an optimal portfolio allocation, given a certain combination of stocks. The tool requires two different inputs. Firstly, the user needs to add the tickers of stocks, which he would like to have in his portfolio. As a second input, one must select the available financial ressources. This allows for the creation of an optimal allocation, given a certain financial allowance. On a technical side, we have reused previous defined functions, as well as creating new ones.   

After the selection of the preferred stocks, the user wants to have in its portfolio, the code gatheres historic financial stock data from the last ten years. To find an optimal weighting, we compute the covariance matrix of the selected stocks and their average returns.   
For this we have used the following two codes from the `Pypfopt` library: `mu = mean_historical_return(portfolio)` calculates average returns and `S = CovarianceShrinkage(portfolio).ledoit_wolf()` creates the covariance matrices.   

Using the principles of the efficient frontier, the webapp computes various portfolios with different weightings, which give the highest possible return, given a certain level of risk (measured in standard deviation). To create this frontier, we use `ef = EfficientFrontier(mu, S)` with the previously calculated return and covariance as the two input elements.   

Ultimately with the following code `raw_weights = ef.max_sharpe()` we are able to find the one portfolio lying on the efficient frontier, which maximises the sharpe ratio, as this indicates better portfolio performance. By doing these calculations, we end up with an optimal portfolio allocation, which tells us how much of each stock to buy given a certain resource allowance. 






### About us

The last page of our Webapp, shows some basic information on the three creators of this Project. It provides information on the team's previous endeavours and it's reasonings behind the overlapping interests of finance and programming. 

## 4.) Appendix

`Numpy` Is used for scientific computing and data analysis. It provides a large set of functions and tools that enable you to perform various mathematical and scientific operations on arrays and matrices of data. One of the main features of NumPy is its support for multidimensional arrays, which are used to represent data in a more organised and efficient way. NumPy also includes a variety of functions for performing operations on these arrays, such as mathematical functions, statistical functions, and linear algebra operations.

`Pandas` Is an open-source machine learning library that is essential for data scientists. It offers a range of high-level data structures and analysis tools, making it easier to perform tasks such as data manipulation, cleaning, and analysis. Some of the operations supported by Pandas include sorting, re-indexing, iteration, concatenation (concatenation refers to the creation of a new string by combining two or more existing strings), data conversion, visualisation, and aggregation.

`YFinance` Allows you to retrieve financial data from Yahoo Finance, a popular financial data provider. It provides a convenient and easy-to-use interface for accessing financial data, including stock prices, market data, and company information.
Using yfinance, you can retrieve a wide range of financial data, including historical stock prices, current market data, and information about specific companies. You can also use the library to perform various types of analysis on the data, such as calculating returns, correlations, and moving averages. We used it because it is easy to use and provides a large amount of data. It is also regularly updated to ensure that the data it provides is current and accurate.

`Seaborn` Is a data visualisation library. It is built on top of Matplotlib and provides a high-level interface for creating attractive and informative statistical graphics. It is particularly useful for exploring and visualising multivariate data, and it is often used in conjunction with Pandas.

`Matplotlib.pyplot` Is a sub-library of the Matplotlib library in Python and provides functions for creating visualisations of data. It is a powerful and flexible library that is widely used in scientific and technical computing to produce a variety of plots and charts. It is often used in combination with other libraries, such as NumPy and Pandas, to create sophisticated visualisations of data.

`Request` Is a library for making HTTP requests. It provides a simple and easy-to-use interface for sending HTTP requests and receiving responses from web servers.
Using requests, you can send various types of HTTP requests, including GET (which was frequently used for this project), and you can specify the parameters and payload of the request as needed. The library also provides functions for processing the response from the server, such as accessing the status code, headers, and content of the response.
HTTP: HTTP stands for Hypertext Transfer Protocol and is a protocol for transmitting data over the internet. It is the foundation of the modern web, and it is used by web browsers and web servers to communicate with each other.
When you visit a website in your web browser, your browser sends an HTTP request to the web server that hosts the site. The server then responds with an HTTP response, which includes the content of the website and other information about the response, such as the status code and headers.

`Json` Works with JSON (JavaScript Object Notation) data. JSON is a data interchange format that is used to transmit data between systems and is often used to represent data in a structured and organised way. It provides functions for encoding and decoding JSON data. It can be used to convert Python data structures, such as dictionaries and lists, into JSON-formatted strings, and to convert JSON-formatted strings into Python data structures. This allows you to easily exchange data with systems that use JSON as their data interchange format. Moreover it helps reading and writing configuration files, and storing data in a structured format. 

`Pypfopt` Is a library used for portfolio optimization, which is the process of selecting a portfolio of assets that optimises some objective, such as maximising return or minimising risk. Pypfopt provides tools and functions for constructing and analysing portfolios using various optimization techniques.

`Math` Provides mathematical functions and tools. It includes a wide range of functions for tasks such as arithmetic, algebra, geometry, and trigonometry.

`Datetime` Is a useful tool for working with dates and times. It provides a range of functions and classes for storing, manipulating, and formatting date and time values and is often used in applications that need to store or manipulate date and time data, such as scheduling systems and financial software.

`Sklearn` Provides a wide range of algorithms and tools for tasks such as classification, regression, clustering, dimensionality reduction, and model selection.

`Streamlit` Is used to create interactive web-based data applications. It allows users to build simple, lightweight, and efficient user interfaces for data applications without the need to write HTML, CSS, or JavaScript. Furthermore it provides a range of functions and widgets for building user interfaces, including buttons, text input fields, dropdown menus, and charts. It also includes features for organising and styling the user interface, such as layout management and custom themes.

`Urlencode` Is used to encode data that will be sent as part of a URL. It converts a dictionary, list of tuples, or a sequence of two-element tuples into a URL query string. 














