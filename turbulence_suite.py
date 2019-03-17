'''
This module contains objects and functions to be used by "TurbulenceSuite.py"
'''

def convert_date_format(date_input):
    '''
    Purpose: convert a datetime.datetime object to its string equivalent,
    in YYYY-MM-DD format.
    
    Output: a string object containing the date in YYYY-MM-DD format.
    
    "date_input": datetime.datetime, the date to be converted.
    '''
    import datetime as dt
    arg_types = [dt.datetime]
    iteration = 0
    for arg in convert_date_format.__code__.co_varnames[:len(arg_types)]:
        arg_value = locals()[arg]
        if isinstance(arg_value, arg_types[iteration]) is False:
            raise TypeError('"{}" must be a {} object'.format(arg,
                            arg_types[iteration]))
        iteration += 1
    
    if (date_input.day < 10 and date_input.month < 10):
        date_output = str(date_input.year) + '-0' + str(date_input.month) + '-0' + str(date_input.day)
    elif date_input.day < 10:
        date_output = str(date_input.year) + '-' + str(date_input.month) + '-0' + str(date_input.day)
    elif date_input.month < 10:
        date_output = str(date_input.year) + '-0' + str(date_input.month) + '-' + str(date_input.day)
    elif (date_input.day >=10 and date_input.month >=10):
        date_output = str(date_input.year) + '-' + str(date_input.month) + '-' + str(date_input.day)
    else:
        raise ValueError('"date_input" value ({}) is faulty.'.format(str(date_input)))
    
    return(date_output)
    
def get_weekly_prices(api_key, count=500):
    '''
    Purpose: Get weekly adjusted closing prices (from Alpha Vantage)
    for all assets used by the Turbulence indicators. 
    
    Output: A dictionary where each item is a list containing
    (in reverse chronological order) the adjusted closing prices.

    "count": integer, how many weeks of data to read.
    
    "api_key": string, the api key used to access Alpha Vantage
    '''
    import json
    import requests as req
    import datetime as dt
    import time
    import sys
    
    api_key = str(api_key)
    count = int(count)
    tickers = ['^FTSE', '^N225', '^GDAXI', '^FCHI', '^HSI', '^BVSP',
               '^RUT', 'IXY', 'IXR', 'IXE', 'IXM', 'IXV', 'IXT',
               'IXB', 'IXU', '^IRX', '^FVX', '^TNX', '^TYX', 'VWEHX',
               'VFSTX', 'VWESX']
    
    output = {'Dates': [], 'FTSE100': [], 'Nikkei225': [], 'DAX': [], 
              'CAC40': [], 'HangSeng': [], 'Bovespa': [],
              'Russell2000': [],
              'ConsumerDisc': [], 'ConsumerStaples': [],
              'Energy': [], 'Financials': [], 'Healthcare': [],
              'Tech': [], 'Materials': [],
              'Utilities': [], '13W_UST': [], '5Y_UST': [],
              '10Y_UST': [], '30Y_UST': [], 'HY_Corp': [],
              'ShortTerm_IG_Corp': [], 'LongTerm_IG_Corp': []}
    
    for iteration in range(0, len(tickers)):
        ticker = tickers[iteration]
        name = list(output.keys())[iteration + 1]
        print('Currently pulling data for {} ({})'.format(ticker, name))
        url = str('https://www.alphavantage.co/query?'
                  + 'function=TIME_SERIES_WEEKLY_ADJUSTED'
                  + '&symbol={}'.format(ticker)
                  + '&apikey={}'.format(api_key))
        
        delay = 4
        for attempt in range(1, 6):
            try:
                weekly_data = json.loads(req.get(url).text)['Weekly Adjusted Time Series']
            except (KeyError, json.JSONDecodeError):
                if attempt != 5:
                    delay = delay * 2
                    print('\t --CONNECTION ERROR--',
                          '\n\t Sleeping for {} seconds before Attempt #{}'.format(delay, attempt + 1))
                    time.sleep(delay)
                else:
                    print('\t -- FINAL CONNECTION ERROR--',
                          '\n\t Quitting program...')
                    sys.exit()
            else:
                break
        
        dates = list(weekly_data.keys())
        first_date = dt.datetime.strptime(dates[0], '%Y-%m-%d')
        second_date = dt.datetime.strptime(dates[1], '%Y-%m-%d')
        if first_date - second_date < dt.timedelta(days=6):
            dates = dates[1 : count + 1]
        else:
            dates = dates[:count]
        
        for date in dates:
            output[name].append(float(weekly_data[date]['5. adjusted close']))
        
        if iteration == len(tickers) - 1:
            output['Dates'].extend(dates)
        
        time.sleep(1)
    
    print('Finished pulling all data!')
    return(output)

def replace_zero_values(input_dictionary):
    '''
    Purpose: Replace 0 values in each item in the "input_dictionary". Replaces
    with the value of the next element.
    
    "input_dictionary": dictionary.
    '''
    for key in input_dictionary.keys():
        for index in range(len(input_dictionary[key]) - 1, -1, -1):
            if input_dictionary[key][index] == 0:
                input_dictionary[key][index] = input_dictionary[key][index + 1]
                
    return(input_dictionary)
    
def update_weekly_prices(prices, api_key):
    '''
    Purpose: update the "prices" with more recent prices.
    
    Output: the updated "prices".
    
    "prices": dataframe, the dataframe to be updated.
    
    "api_key": string, the api key used to access Alpha Vantage
    '''
    import pandas as pd
    import datetime as dt
    
    api_key = str(api_key)
    new_pull = get_weekly_prices(api_key)
    new_pull = pd.DataFrame(replace_zero_values(new_pull))
    previous_date = dt.datetime.strptime(prices['Dates'][0], '%Y-%m-%d')
    data_to_add_indices = []
    for index in range(0, len(new_pull)):
        date = dt.datetime.strptime(new_pull.loc[index, 'Dates'], '%Y-%m-%d')
        if date > previous_date:
            data_to_add_indices.append(index)
        elif date == previous_date:
            break
    
    data_to_add = new_pull.loc[data_to_add_indices,]
    prices = data_to_add.append(prices)
    prices.reset_index(inplace=True)
    prices.drop('index', axis=1, inplace=True)
    
    return(prices)

def add_curve_slope(prices):
    '''
    Purpose: calculates yield curve slope data from data that is already in
    "prices", and appends yield curve slope data to "prices".
    
    Output: "prices" with yield curve slope data added.
    '''
    
    prices['CurveSlope_10Y-5Y'] = prices['10Y_UST'] - prices['5Y_UST']
    prices['CurveSlope_10Y-13W'] = prices['10Y_UST'] - prices['13W_UST']
    
    return(prices)
    
def first_difference(price_t1, price_t0, percent_change=True):
    '''
    Purpose: calculate either the percent change or absolute change between
    two prices.
    
    Output: the percent change or absolute change, as a float object.
    '''
    price_t1 = float(price_t1)
    price_t0 = float(price_t0)
    
    if percent_change == True:
        return(float((price_t1/price_t0) - 1))
    else:
        return(float(price_t1 - price_t0))
        
def calculate_returns(prices):
    '''
    Purpose: calculate single-period returns from the "prices".
    
    Output: a dataframe containing the returns.
    
    "prices": dataframe, contains prices.
    '''
    import pandas as pd
    output = {'Dates': prices['Dates'][:len(prices) - 1],
              'FTSE100': [], 'Nikkei225': [], 'DAX': [], 
              'CAC40': [], 'HangSeng': [], 'Bovespa': [],
              'Russell2000': [],
              'ConsumerDisc': [], 'ConsumerStaples': [],
              'Energy': [], 'Financials': [], 'Healthcare': [],
              'Tech': [], 'Materials': [],
              'Utilities': [], '10Y_UST': [], '30Y_UST': [],
              'CurveSlope_10Y-5Y': [], 'CurveSlope_10Y-13W': [], 
              'HY_Corp': [],
              'ShortTerm_IG_Corp': [], 'LongTerm_IG_Corp': []}
    
    yield_assets = ['10Y_UST', '30Y_UST', 'CurveSlope_10Y-5Y',
                    'CurveSlope_10Y-13W']
    
    for asset in list(output.keys())[1:]:
        returns = []
        for date in range(0, len(prices) - 1):
            if asset in yield_assets:
                returns.append(first_difference(price_t1=prices.loc[date, asset],
                                                price_t0=prices.loc[date + 1, asset],
                                                percent_change=False))
            else:
                returns.append(first_difference(price_t1=prices.loc[date, asset],
                                                price_t0=prices.loc[date + 1, asset]))
        output[asset] = returns
        
    return(pd.DataFrame(output))

def exponential_smoother(raw_data, half_life):
    '''
    Purpose: performs exponential smoothing on "raw_data". Begins recursion
    with the first data item (i.e. assumes that data in "raw_data" is listed
    in chronological order).
    
    Output: a list containing the smoothed values of "raw_data".
    
    "raw_data": iterable, the data to be smoothed.
    
    "half_life": float, the half-life for the smoother. The smoothing factor
    (alpha) is calculated as alpha = 1 - exp(ln(0.5) / half_life)
    '''
    import math
    
    raw_data = list(raw_data)
    half_life = float(half_life)
    
    smoothing_factor = 1 - math.exp(math.log(0.5) / half_life)
    smoothed_values = [raw_data[0]]
    for index in range(1, len(raw_data)):
        previous_smooth_value = smoothed_values[-1]
        new_unsmooth_value = raw_data[index]
        new_smooth_value = ((smoothing_factor * new_unsmooth_value)
            + ((1 - smoothing_factor) * previous_smooth_value))
        smoothed_values.append(new_smooth_value)
    
    return(smoothed_values)
        
def calculate_turbulence(returns, initial_window_size=250):
    '''
    Purpose: calculate the Turbulence of the asset pool.
    
    Output: a dictionary containing the Turbulence values and their date-stamps.
    
    "returns": dataframe, the returns of the asset pool (in reverse chronological
    order)
    
    "initial window_size": integer, the initial window size used to calculate
    the covariance matrix. This window size grows as the analysis proceeds
    across time.
    '''
    import copy
    import numpy as np
    from scipy.spatial import distance
    
    window_size = copy.deepcopy(int(initial_window_size)) 
    turbulence = {'Dates': [], 'Raw Turbulence': []}
    chronological_returns = returns.iloc[::-1]
    while window_size < len(chronological_returns):
        historical_sample = chronological_returns.iloc[:window_size, 1:]
        historical_sample_means = historical_sample.mean()
        inverse_covariance_matrix = np.linalg.pinv(historical_sample.cov())
        current_data = chronological_returns.iloc[[window_size]]
        
        mahalanobis_distance = distance.mahalanobis(u=current_data.iloc[:, 1:],
                                                    v=historical_sample_means,
                                                    VI=inverse_covariance_matrix)
        
        turbulence['Raw Turbulence'].append(mahalanobis_distance)
        turbulence['Dates'].append(current_data['Dates'].values[0])
        window_size += 1
        
    turbulence['Turbulence'] = exponential_smoother(raw_data=turbulence['Raw Turbulence'],
                                                    half_life=12)
        
    return(turbulence)

def gini(values):
    '''
    Purpose: calculate the Gini coefficient for a one-dimensional set of values.
    
    Output: the Gini coefficient, as a float object.
    
    "values": iterable, the values on which to calculate the Gini coefficient.
    The data in "values" does not have to be sorted in ascending or descending order.
    '''
    
    values = list(values)
    values.sort()
    
    minimum_value = values[0]
    lorenz_curve_value = minimum_value
    average_input = sum(values)/len(values)
    line_of_equality = [average_input]
    gap_area = [line_of_equality[0] - lorenz_curve_value]
    
    for index in range(1, len(values)):
        lorenz_curve_value += values[index]
        line_of_equality.append(line_of_equality[index - 1] + average_input)
        gap_area.append(line_of_equality[index - 1] + average_input
                        - lorenz_curve_value)
    
    return(sum(gap_area)/sum(line_of_equality))
    
def calculate_systemic_risk(returns, window_size=250):
    '''
    Purpose: calculate the Systemic Risk of the asset pool.
    
    Output: a dictionary containing the Systemic Risk values and their date-stamps.
    
    "returns": dataframe, the returns of the asset pool (in reverse chronological
    order)
    
    "window_size": integer, the window size used to calculate
    the covariance matrix. This window size shifts forward as the analysis proceeds
    across time.
    '''
    
    import numpy as np
    import copy
    
    systemic_risk = {'Dates': [], 'Systemic Risk': []}
    chronological_returns = returns.iloc[::-1]
    
    window_endpoint = copy.deepcopy(window_size)
    while window_endpoint < len(chronological_returns):
        covariance_matrix = chronological_returns.iloc[window_endpoint + 1 - window_size : window_endpoint + 1].cov()
        eigenvalues = np.sort(np.linalg.eig(covariance_matrix)[0])
        systemic_risk['Systemic Risk'].append(gini(values=eigenvalues))
        systemic_risk['Dates'].append(chronological_returns.iloc[window_endpoint, 0])
        window_endpoint += 1
        
    return(systemic_risk)

def check_single_ticker(ticker, api_key):
    '''
    Purpose: summarizes the Alpha Vantage data pull for a single asset.
    
    "ticker": string, the asset ticker.
    
    "api_key": string, the api key used to access Alpha Vantage.
    '''
    import requests as req
    import json
    
    ticker = str(ticker)
    api_key = str(api_key)
    url = str('https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED'
              + '&symbol={}'.format(ticker)
              + '&apikey={}'.format(api_key))
    json_data = json.loads(req.get(url).text)
    print(json_data['Meta Data'])
    
    return(json_data['Weekly Adjusted Time Series'])

#MIT License
#
#Copyright (c) 2019 Terrence Y. Zhang
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.