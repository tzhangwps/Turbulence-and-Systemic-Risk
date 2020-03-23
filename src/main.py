"""
The main module to output the Turbulence and Systemic Risk indicators.
"""
import pandas as pd
import os

import TurbulenceSuite_paths as path
import src.get_data as get
import src.calculate as calc


class MainProcess:
    """
    Contains the main processes to run the Turbulence and Systemic Risk
    indicators.
    """
    
    
    def __init__(self):
        self.prices = pd.DataFrame()
        self.returns = pd.DataFrame()
        self.turbulence = pd.DataFrame()
        self.systemic_risk = pd.DataFrame()
    
    
    def append_prices_and_returns(self):
        """
        Appends new data to the prices dataset and the returns dataset.
        """
        print('\nRequesting data from Yahoo Finance...')
        self.prices = pd.read_pickle(path.prices_path_historical)
        self.prices = get.GetPrices().update_weekly_prices(self.prices)
        self.prices.to_pickle(path.prices_path_current)
        self.prices = get.CalculateReturns().add_curve_slope(self.prices)
        self.returns = get.CalculateReturns().calculate_returns(self.prices)
        
        
    def calculate_turbulence_and_systemic_risk(self):
        """
        Calculates Turbulence and Systemic Risk.
        """
        print('\nBuilding Turbulence Index...')
        self.turbulence = pd.DataFrame(calc.Calculate().calculate_turbulence(self.returns))
        print('Turbulence Index completed!')
        
        print('\nBuilding Systemic Risk Index...')
        self.systemic_risk = pd.DataFrame(calc.Calculate().calculate_systemic_risk(self.returns))
        print('Systemic Risk Index completed!')
        
        
    def save_chart_data(self):
        """
        Reformats data so that it can be uploaded to Visualizer (Wordpress library).
        """
        turbulence_chart = pd.DataFrame({
                                         'Dates': ['date'] + list(self.turbulence['Dates']),
                                         'Raw Turbulence': ['number'] + list(self.turbulence['Raw Turbulence']),
                                         'Turbulence': ['number'] + list(self.turbulence['Turbulence']),
                                         'Recession': ['number'] + list(self.turbulence['Recession'])
                                        })
        systemic_risk_chart = pd.DataFrame({
                                            'Dates': ['date'] + list(self.systemic_risk['Dates']),
                                            'Systemic Risk': ['number'] + list(self.systemic_risk['Systemic Risk']),
                                            'Recession': ['number'] + list(self.systemic_risk['Recession'])
                                           })
        
        turbulence_chart.to_csv(path.turbulence_chart_path, index=False)
        systemic_risk_chart.to_csv(path.systemic_risk_chart_path, index=False)
        
        print('\nTurbulence and Systemic Risk data written as .csv files and saved to',
              str(os.getcwd() + '\\data'))
        print('\n{}'.format(self.turbulence.iloc[-5:,]))
        input('Press [ENTER] to close the program.')