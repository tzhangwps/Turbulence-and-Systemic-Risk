"""
Drops rows from the index_data.pkl dataframe.
"""
import pandas as pd

import TurbulenceSuite_paths as path


class DropRecent:
    """
    The manager class for this module.
    """
    
    
    def drop(self, rows_to_drop):
        """
        Drop rows from the index_data.pkl dataframe.
        """
        prices = pd.read_pickle(path.prices_path_current)
        prices = prices.iloc[rows_to_drop:,]
        prices.reset_index(inplace=True)
        prices = prices.drop('index', axis=1)
        prices.to_pickle(path.prices_path_current)
        
        print('\nRemoved {} rows from "prices" dataframe'.format(rows_to_drop),
              'and saved to {}'.format(path.prices_path_current))


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