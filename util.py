from generalImport import *


def save_dict(dict, folder_name):
    """
    Save a dictionary of DataFrames into CSV files inside a folder.
    
    data_dict: dict like {"AAPL": df, "JPM": df2}
    folder_name: str name of folder to save files
    """
    os.makedirs(folder_name, exist_ok=True)

    for k, v in dict.items():
        if hasattr(v, "to_csv"):
            file_path = os.path.join(folder_name, f"{k}.csv")
            v.to_csv(file_path, index=False)
        else:
            print(f"Skipping {k}: value is not a DataFrame")
    print("save complete")


def load_dict(folder_name):
    """
    Loads all CSV files from a folder into a dictionary of DataFrames.
    Returns: {"filename_without_extension": dataframe}
    """

    if not os.path.isdir(folder_name):
        raise FileNotFoundError(f"Folder '{folder_name}' does not exist.")

    loaded_dict = {}

    for file in os.listdir(folder_name):
        if file.endswith(".csv"):
            key = file[:-4]  # remove ".csv"
            file_path = os.path.join(folder_name, file)
            loaded_dict[key] = pd.read_csv(file_path)

    print(f"Loaded {len(loaded_dict)} DataFrames from '{folder_name}'.")
    return loaded_dict

def extract_stocks_historical_price_from_dict(dict):
    store = pd.DataFrame({})
    isFirst = True
    for key, value in dict.items():
        if(isFirst):
            store["Date"] = value["Date"]
            isFirst = False
        store[key] = (value["High"] + value["Low"]) / 2
    return store

def price_scaling(raw_prices_df):
    scaled_prices_df = raw_prices_df.copy()
    for i in raw_prices_df.columns[1:]:
          scaled_prices_df[i] = raw_prices_df[i]/raw_prices_df[i][0]
    return scaled_prices_df

def generate_portfolio_weights(n):
    weights = []
    for i in range(n):
        weights.append(random.random())
        
    # let's make the sum of all weights add up to 1
    weights = weights/np.sum(weights)
    return weights

# generalize it
def asset_allocation(df, weights, initialInvestment):
    # copy from instruction:
    portfolio_df = df.copy()

    # Scale stock prices using the "price_scaling" function that we defined earlier (Make them all start at 1)
    scaled_df = price_scaling(df)

    for i, stock in enumerate(scaled_df.columns[1:]):
        portfolio_df[stock] = scaled_df[stock] * weights[i] * initialInvestment

    # Sum up all values and place the result in a new column titled "portfolio value [$]" 
    # Note that we excluded the date column from this calculation
    portfolio_df['Portfolio Value [$]'] = portfolio_df[portfolio_df != 'Date'].sum(axis = 1, numeric_only = True)
            
    # Calculate the portfolio percentage daily return and replace NaNs with zeros
    portfolio_df['Portfolio Daily Return [%]'] = portfolio_df['Portfolio Value [$]'].pct_change(1) * 100 
    portfolio_df.replace(np.nan, 0, inplace = True)

    return portfolio_df


def measure(assetAllocation, rf = 0.03):
    # in the course they need to input weight, and initial investment, but 
    #   initial investment and weight can be derived from assetAllocation table
    # 1 calculate weight and initial investment.
    # weight and initial investment
    initialInvestment = float(assetAllocation.iloc[0, -2])
    initialWeight = assetAllocation.iloc[0, 1:(-1-1)] / initialInvestment

    # 1: ROI
    # what we get at the end compare with intial
    ROI = (float(assetAllocation.iloc[-1, -2]) / initialInvestment  - 1 ) * 100

    # 2: SHARP
    modiAssetAllocation = assetAllocation.drop(columns=assetAllocation.columns[[0, -1, -2]]).pct_change(1)
        # using the formular provided from the course
    expected_port_return = np.sum(initialWeight * modiAssetAllocation.mean()) * 252
    covariance = modiAssetAllocation.cov() * 252
    expected_volatility = np.sqrt(np.dot(initialWeight.T, np.dot(covariance, initialWeight)))
    shareRatio = (expected_port_return - rf) / expected_volatility
    return {"expectedReturn": float(expected_port_return), "expectedVolatility": float(expected_volatility), "shareRatio": float(shareRatio), "endReturn": float(assetAllocation.iloc[-1, -2]), "returnOnInvestment": ROI} 

def measurev2(assetAllocation, rf = 0.03):
    # in the course they need to input weight, and initial investment, but 
    #   initial investment and weight can be derived from assetAllocation table
    # 1 calculate weight and initial investment.
    # weight and initial investment
    initialInvestment = float(assetAllocation.iloc[0, -2])
    initialWeight = assetAllocation.iloc[0, 1:(-1-1)] / initialInvestment

    # 1: ROI
    # what we get at the end compare with intial
    ROI = (float(assetAllocation.iloc[-1, -2]) / initialInvestment  - 1 ) * 100

    # 2: SHARP
    modiAssetAllocation = assetAllocation.drop(columns=assetAllocation.columns[[0, -1, -2]]).pct_change(1)
        # using the formular provided from the course
    expected_port_return = np.sum(initialWeight * modiAssetAllocation.mean()) * 252
    covariance = modiAssetAllocation.cov() * 252
    expected_volatility = np.sqrt(np.dot(initialWeight.T, np.dot(covariance, initialWeight)))
    shareRatio = (expected_port_return - rf) / expected_volatility
    return float(expected_port_return), float(expected_volatility), float(shareRatio), float(assetAllocation.iloc[-1, -2]), ROI


def asset_allocation_from_scratch_version(fileLoc, weights, initialInvestment):
    df = load_dict(fileLoc)
    return asset_allocation(df, weights, initialInvestment)

def monteCarlosSimulator(priceDicLocation, sim_runs = 100, initialInvestment = 1000, riskFreeRate = 0.03):
    PriceDict = load_dict(priceDicLocation)
    priceMovement = extract_stocks_historical_price_from_dict(PriceDict)
    scaledPriceMovement = price_scaling(priceMovement)
    n = len(scaledPriceMovement.columns) - 1 # first one is the date

    weights_runs = np.zeros((sim_runs, n))
    sharpe_ratio_runs = np.zeros(sim_runs)
    expected_portfolio_returns_runs = np.zeros(sim_runs)
    volatility_runs = np.zeros(sim_runs)
    return_on_investment_runs = np.zeros(sim_runs)
    final_value_runs = np.zeros(sim_runs)

    for i in range(sim_runs):
        weights = generate_portfolio_weights(n)
        weights_runs[i,:] = weights
        allocationResult = asset_allocation(scaledPriceMovement, weights, initial_investment)
        expected_portfolio_returns_runs[i], volatility_runs[i], sharpe_ratio_runs[i], final_value_runs[i], return_on_investment_runs[i] = measurev2(allocationResult, 0.03)
        print("Simulation Run = {}".format(i))   
        print("Weights = {}, Final Value = ${:.2f}, Sharpe Ratio = {:.2f}".format(weights_runs[i].round(3), final_value_runs[i], sharpe_ratio_runs[i]))   
        print('\n')
    return weights_runs, sharpe_ratio_runs, expected_portfolio_returns_runs, volatility_runs, return_on_investment_runs, final_value_runs, scaledPriceMovement.columns