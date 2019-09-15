"""
This module contains ad hoc functions not used by the main modules.
"""

def convert_date_format(date_input):
    """
    Purpose: convert a datetime.datetime object to its string equivalent,
    in YYYY-MM-DD format.
    
    Output: a string object containing the date in YYYY-MM-DD format.
    
    "date_input": datetime.datetime, the date to be converted.
    """
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
    
    
def check_single_ticker(ticker, api_key):
    """
    Purpose: summarizes the Alpha Vantage data pull for a single asset.
    
    "ticker": string, the asset ticker.
    
    "api_key": string, the api key used to access Alpha Vantage.
    """
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
#Copyright (c) 2019 Terrence Zhang
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