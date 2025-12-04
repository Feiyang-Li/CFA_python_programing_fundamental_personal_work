# Python programming fundamental

# purpose:
To learn how to use python to extract stock information, to clean and transform data, to analysis data, and to present data. It is also required by CFA institute as one of the courses required to get the final CFA level 1 grade.

# Package used:
- pandas
- matplotlib
- yfinance
- pandas
- numpy
- json
- plotly
- random
- datetime

# instruction
1.1 - 5.10 are the work sheet for each course sections, the util.py is the specialize functionality I created to improvize what I learned from the course.
What I did here is:
1. Allowing for saving the stock information obtained as the csv file into a specific folder. Detail look into: save_dict(dict, folder_name)
In addition, loading dictionary is also possible with load_dict(folder_name)

2. The function extract_stocks_historical_price_from_dict(dict) is specifically using the same dict as mentioned in 1, to get the average stock price of each stock throughout history and group up to a pandas dataframe

3. price_scaling(raw_prices_df), generate_portfolio_weights(n) is same as cfa instructor provided, first one scale down share price so in first year start with one, and year after multiply one by a growth factor. Second one is just use random to generate a weight.

4. asset_allocation, is using weights and initialInvestment to get what would each date individual stock value be, and porfolio value be. It is a simulation of a investment, using the historical data.

5. measure(assetAllocation, rf = 0.03), measure the result of your simulation in step 4, it give you the expectedReturn, expectedVolativlity, sharpRatio, endReturn, and returnOnInvestment

6. measurev2 is just a return method different than measure

7. monteCarlosSimulator(priceDicLocation, sim_runs = 100, initialInvestment = 1000, riskFreeRate = 0.03), performing monteCarlosSimulation on the stocks reside in the priceDicLocation.

Notice 4 - 7, used the different method as CFA instructors taught, I found it more clearer to understand, since I can make each function seperate as compare as CFA instruction method which must reside within a ipynb file. 

# my comment:
- yfinance is very useful, I hope I learn it earlier
- monteCarlosSimulation is interesting, but I think you could just use some formular to get the weight and that take less time.
- I will work on creating my own index in my future project, using the historical information extract from yfinance. 

# what I learn:
- python is what this course teach, it future consolidate my understanding in python (especially on data analysis part) (although I am already very familar with it)
- yfinance (yahoo finance api) to extract stock information
- numpy, pandas, matplot, pyplot. (which I also have a great amount of experience before)
- monte Carlos Simulation for stock price analysis.
- Portfolio construction, and portfolio price analysis.
- Graphical display of the portfolio return.