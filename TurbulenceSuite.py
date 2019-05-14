'''
/# ######################################################################### #/
/# ##################### T U R B U L E N C E    S U I T E ################## #/
/# ######################################################################### #/
/#                                                                           #/
/# Name: TurbulenceSuite.py                                                  #/
/#                                                                           #/
/# Date: March 2019                                                          #/
/#                                                                           #/
/# Contact: Terrence Zhang (tzhangwps@gmail.com)                             #/
/#                                                                           #/
/# ######################################################################### #/
/# ######################### G O  G A T O R S ! ! ! ######################## #/
/# ######################################################################### #/
'''

import os
import pandas as pd
import argparse

import turbulence_suite as ts

###############################################################################
###################### Set the Input and Output Filepaths #####################
###############################################################################

os.chdir(os.path.dirname(os.path.abspath(__file__)))
parser = argparse.ArgumentParser()
parser.add_argument('api_key', type=str,
                    help=
                    '''
                    The api key used to pull data from Alpha Vantage.
                    
                    Get your api key here: https://www.alphavantage.co/support/#api-key
                    ''')
args = parser.parse_args()
api_key = args.api_key

prices_path = os.path.join(os.getcwd(), 'index_data.pkl')
turbulence_chart_path = os.path.join(os.getcwd(), 'turbulence_chart.csv')
systemic_risk_chart_path = os.path.join(os.getcwd(), 'systemic_risk_chart.csv')

###############################################################################
################################ Begin Analyzing ##############################
###############################################################################

prices = pd.read_pickle(prices_path)
print('\nRequesting data from Alpha Vantage API...')
prices = ts.MainProcess().update_weekly_prices(prices, api_key=api_key)
prices.to_pickle(prices_path)

prices = ts.MainProcess().add_curve_slope(prices)
returns = ts.MainProcess().calculate_returns(prices)

print('\nBuilding Turbulence Index...')
turbulence = pd.DataFrame(ts.MainProcess().calculate_turbulence(returns))
print('Turbulence Index completed!')
print('\nBuilding Systemic Risk Index...')
systemic_risk = pd.DataFrame(ts.MainProcess().calculate_systemic_risk(returns))
print('Systemic Risk Index completed!')

turbulence_chart = pd.DataFrame({
                                 'Dates': ['date'] + list(turbulence['Dates']),
                                 'Raw Turbulence': ['number'] + list(turbulence['Raw Turbulence']),
                                 'Turbulence': ['number'] + list(turbulence['Turbulence']),
                                })
systemic_risk_chart = pd.DataFrame({
                                    'Dates': ['date'] + list(systemic_risk['Dates']),
                                    'Systemic Risk': ['number'] + list(systemic_risk['Systemic Risk'])
                                   })

turbulence_chart.to_csv(turbulence_chart_path, index=False)
systemic_risk_chart.to_csv(systemic_risk_chart_path, index=False)

print('\nTurbulence and Systemic Risk data written as .csv files and saved to',
      str(os.getcwd()))
print('\n{}'.format(turbulence.iloc[-5:,]))
input('Press [ENTER] to close the program.')
        
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