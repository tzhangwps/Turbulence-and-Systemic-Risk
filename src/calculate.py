"""
This module calculates the Turbulence and Systemic Risk indicators.
"""

class Calculate:
    """
    Calculates the Turbulence and Systemic Risk indicators.
    """
    
    
    def __init__(self):
        self.recession_start_dates = ['2001-04-01', '2008-01-01', '2020-03-01']
        self.recession_end_dates = ['2001-11-01', '2009-06-01', '2020-04-01']
        self.turbulence = {}
        self.systemic_risk = {}
    
    
    def exponential_smoother(self, raw_data, half_life):
        """
        Purpose: performs exponential smoothing on "raw_data". Begins recursion
        with the first data item (i.e. assumes that data in "raw_data" is listed
        in chronological order).
        
        Output: a list containing the smoothed values of "raw_data".
        
        "raw_data": iterable, the data to be smoothed.
        
        "half_life": float, the half-life for the smoother. The smoothing factor
        (alpha) is calculated as alpha = 1 - exp(ln(0.5) / half_life)
        """
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
        
        
    def append_recession_series(self, current_date, dataframe):
        """
        Purpose: determine if the "current_date" is in a recessionary time period.
        Appends the result (100 if in recession, 0 if not) to the "Recession"
        series of the "dataframe".
        """
        recession_value = 0
        for recession_instance in range(0, len(self.recession_end_dates)):
            recession_start = self.recession_start_dates[recession_instance]
            recession_end = self.recession_end_dates[recession_instance]
            after_start_date = current_date >= recession_start
            before_end_date = current_date <= recession_end
            
            if after_start_date and before_end_date:
                recession_value = 100
                break
        dataframe['Recession'].append(recession_value)
        
    
    def calculate_turbulence(self, returns, initial_window_size=250):
        """
        Purpose: calculate the Turbulence of the asset pool.
        
        Output: a dictionary containing the Turbulence values and their date-stamps.
        
        "returns": dataframe, the returns of the asset pool (in reverse chronological
        order)
        
        "initial window_size": integer, the initial window size used to calculate
        the covariance matrix. This window size grows as the analysis proceeds
        across time.
        """
        import copy
        import numpy as np
        from scipy.spatial import distance
        
        window_size = copy.deepcopy(int(initial_window_size)) 
        self.turbulence = {'Dates': [], 'Raw Turbulence': [], 'Recession': []}
        chronological_returns = returns.iloc[::-1]
        while window_size < len(chronological_returns):
            historical_sample = chronological_returns.iloc[:window_size, 1:]
            historical_sample_means = historical_sample.mean()
            inverse_covariance_matrix = np.linalg.pinv(historical_sample.cov())
            current_data = chronological_returns.iloc[[window_size]]
            current_date = current_data['Dates'].values[0]
            
            mahalanobis_distance = distance.mahalanobis(u=current_data.iloc[:, 1:],
                                                        v=historical_sample_means,
                                                        VI=inverse_covariance_matrix)
            
            self.turbulence['Raw Turbulence'].append(mahalanobis_distance)
            self.turbulence['Dates'].append(current_date)
            self.append_recession_series(current_date=current_date,
                                         dataframe=self.turbulence)
            window_size += 1
            
        self.turbulence['Turbulence'] = self.exponential_smoother(raw_data=self.turbulence['Raw Turbulence'],
                                                                  half_life=12)
        return(self.turbulence)


    def gini(self, values):
        """
        Purpose: calculate the Gini coefficient for a one-dimensional set of values.
        
        Output: the Gini coefficient, as a float object.
        
        "values": iterable, the values on which to calculate the Gini coefficient.
        The data in "values" does not have to be sorted in ascending or descending order.
        """
        
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
    
    
    def calculate_systemic_risk(self, returns, window_size=250):
        """
        Purpose: calculate the Systemic Risk of the asset pool.
        
        Output: a dictionary containing the Systemic Risk values and their date-stamps.
        
        "returns": dataframe, the returns of the asset pool (in reverse chronological
        order)
        
        "window_size": integer, the window size used to calculate
        the covariance matrix. This window size shifts forward as the analysis proceeds
        across time.
        """
        
        import numpy as np
        import copy
        
        self.systemic_risk = {'Dates': [], 'Systemic Risk': [], 'Recession': []}
        chronological_returns = returns.iloc[::-1]
        
        window_endpoint = copy.deepcopy(int(window_size))
        while window_endpoint < len(chronological_returns):
            covariance_matrix = chronological_returns.iloc[window_endpoint + 1 - window_size : window_endpoint + 1].cov()
            eigenvalues = np.sort(np.linalg.eig(covariance_matrix)[0])
            current_date = chronological_returns.iloc[window_endpoint, 0]
            self.systemic_risk['Systemic Risk'].append(self.gini(values=eigenvalues))
            self.systemic_risk['Dates'].append(current_date)
            self.append_recession_series(current_date=current_date,
                                         dataframe=self.systemic_risk)
            window_endpoint += 1
            
        return(self.systemic_risk)