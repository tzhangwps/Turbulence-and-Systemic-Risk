"""
This module gets data from Yahoo Finance.
"""
import re
from io import StringIO
import requests as req
import datetime as dt
import time
import pandas as pd


class YahooData:
    """
    Retrieves data from Yahoo Finance.
    
    Original code source: https://stackoverflow.com/questions/44225771/scraping-historical-data-from-yahoo-finance-with-python
    """
    timeout = 2
    crumb_link = 'https://finance.yahoo.com/quote/{0}/history?p={0}'
    crumble_regex = r'CrumbStore":{"crumb":"(.*?)"}'
    quote_link = 'https://query1.finance.yahoo.com/v7/finance/download/{quote}?period1={dfrom}&period2={dto}&interval=1wk&events=history&crumb={crumb}'


    def __init__(self, symbol, days_back=7):
        """
        symbol: ticker symbol for the asset to be pulled.
        """
        self.symbol = str(symbol)
        self.session = req.Session()
        self.dt = dt.timedelta(days=days_back)


    def get_crumb(self):
        """
        Original code source: https://stackoverflow.com/questions/44225771/scraping-historical-data-from-yahoo-finance-with-python
        """
        response = self.session.get(self.crumb_link.format(self.symbol), timeout=self.timeout)
        response.raise_for_status()
        match = re.search(self.crumble_regex, response.text)
        if not match:
            raise ValueError('Could not get crumb from Yahoo Finance')
        else:
            self.crumb = match.group(1)


    def get_quote(self):
        """
        Original code source: https://stackoverflow.com/questions/44225771/scraping-historical-data-from-yahoo-finance-with-python
        """
        if not hasattr(self, 'crumb') or len(self.session.cookies) == 0:
            self.get_crumb()
        now = dt.datetime.utcnow()
        dateto = int(now.timestamp())
        datefrom = -630961200
#       line in original code: datefrom = int((now - self.dt).timestamp())
        url = self.quote_link.format(quote=self.symbol, dfrom=datefrom, dto=dateto, crumb=self.crumb)
        response = self.session.get(url)
        response.raise_for_status()
        return pd.read_csv(StringIO(response.text), parse_dates=['Date'])


class GetPrices:
    """
    Gets price data from Yahoo Finance.
    """
    
    
    def __init__(self):
        self.dates = []
        self.values = []
    

    def yahoo_response(self, series_id):
        """
        Retrieves data from Yahoo Finance, and performs timestamp adjustments.
        
        series_id: ticker symbol for the asset to be pulled.
        """
        series_id = str(series_id)
        series_dataframe = YahooData(series_id).get_quote()[::-1]
        series_dataframe.reset_index(inplace=True)
        series_dataframe.drop('index', axis=1, inplace=True)
                                               
        first_date = dt.datetime.strptime(str(series_dataframe['Date'][0])[:10],
                                          '%Y-%m-%d')
        second_date = dt.datetime.strptime(str(series_dataframe['Date'][1])[:10],
                                           '%Y-%m-%d')                      
                                               
        if first_date - second_date < dt.timedelta(days=6):
            series_dataframe = series_dataframe[1:]
            series_dataframe.reset_index(inplace=True)
            series_dataframe.drop('index', axis=1, inplace=True)
            
        self.dates.extend([str(series_dataframe['Date'][index])[:10]
            for index in range(0, len(series_dataframe))])
        self.values.extend([float(series_dataframe['Adj Close'][index])
            for index in range(0, len(series_dataframe))])
    
    
    def get_weekly_prices(self):
        """
        Purpose: Get weekly adjusted closing prices (from Yahoo Finance)
        for all assets used by the Turbulence indicators. 
        
        Output: A dictionary where each item is a list containing
        (in reverse chronological order) the adjusted closing prices.
        """
        
        
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
            self.dates = []
            self.values = []
            name = list(output.keys())[iteration + 1]
            print('Currently pulling data for {} ({})'.format(ticker, name))
            
            success = False
            while success == False:
                try:
                    self.yahoo_response(series_id=ticker)
                except (req.HTTPError, req.exceptions.ReadTimeout):
                    delay = 5
                    print('\t --CONNECTION ERROR--',
                          '\n\t Sleeping for {} seconds.'.format(delay))
                    time.sleep(delay)
                else:
                    success = True
                    
            output[name].extend(self.values)
            
            if iteration == 1:
                output['Dates'].extend(self.dates)
            
            time.sleep(1)
        
        print('Finished pulling all data!')
        return(output)
        
        
    def replace_zero_values(self, input_dictionary):
        """
        Purpose: Replace 0 values in each item in the "input_dictionary". Replaces
        with the value of the next element.
        
        "input_dictionary": dictionary.
        """
        for key in input_dictionary.keys():
            for index in range(len(input_dictionary[key]) - 1, -1, -1):
                is_zero = input_dictionary[key][index] == 0
                is_nan = str(input_dictionary[key][index]) == 'nan'
                if is_zero or is_nan:
                    input_dictionary[key][index] = input_dictionary[key][index + 1]
                    
        return(input_dictionary)
    
    
    def update_weekly_prices(self, prices):
        """
        Purpose: update the "prices" with more recent prices.
        
        Output: the updated "prices".
        
        "prices": dataframe, the dataframe to be updated.
        """
        
        new_pull = self.get_weekly_prices()
        new_pull = self.replace_zero_values(input_dictionary=new_pull)
        new_pull = pd.DataFrame(dict([(k,pd.Series(v)) for k,v in new_pull.items()]))
        previous_date = dt.datetime.strptime(prices['Dates'][0], '%Y-%m-%d')
        data_to_add_indices = []
        for index in range(0, len(new_pull)):
            date = dt.datetime.strptime(new_pull.loc[index, 'Dates'], '%Y-%m-%d')
            if date > previous_date:
                data_to_add_indices.append(index)
            elif date <= previous_date:
                break
        
        data_to_add = new_pull.loc[data_to_add_indices,]
        prices = data_to_add.append(prices)
        prices.reset_index(inplace=True)
        prices.drop('index', axis=1, inplace=True)
        
        return(prices)
        

class CalculateReturns:
    """
    Creates the returns dataset from the prices dataset.
    """


    def add_curve_slope(self, prices):
        """
        Purpose: calculates yield curve slope data from data that is already in
        "prices", and appends yield curve slope data to "prices".
        
        Output: "prices" with yield curve slope data added.
        """
        
        prices['CurveSlope_10Y-5Y'] = prices['10Y_UST'] - prices['5Y_UST']
        prices['CurveSlope_10Y-13W'] = prices['10Y_UST'] - prices['13W_UST']
        
        return(prices)


    def first_difference(self, price_t1, price_t0, percent_change=True):
        """
        Purpose: calculate either the percent change or absolute change between
        two prices.
        
        Output: the percent change or absolute change, as a float object.
        """
        price_t1 = float(price_t1)
        price_t0 = float(price_t0)
        
        if percent_change == True:
            return(float((price_t1/price_t0) - 1))
        else:
            return(float(price_t1 - price_t0))

        
    def calculate_returns(self, prices):
        """
        Purpose: calculate single-period returns from the "prices".
        
        Output: a dataframe containing the returns.
        
        "prices": dataframe, contains prices.
        """
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
                    returns.append(self.first_difference(price_t1=prices.loc[date, asset],
                                                         price_t0=prices.loc[date + 1, asset],
                                                         percent_change=False))
                else:
                    returns.append(self.first_difference(price_t1=prices.loc[date, asset],
                                                         price_t0=prices.loc[date + 1, asset]))
            output[asset] = returns
            
        return(pd.DataFrame(output))