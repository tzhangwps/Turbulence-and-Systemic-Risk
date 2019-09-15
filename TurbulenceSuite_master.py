"""
This is the main script that runs all modules.
"""

import os
import argparse

import src.drop_recent as drp
import src.main as main
import TurbulenceSuite_paths as path

os.chdir(os.path.dirname(os.path.abspath(__file__)))
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--drop_recent', type=int,
                    help=
                    """
                    How many rows (reverse-chronological) do you want to
                    remove from the "index_data.pkl" dataframe?
                    """)
args = parser.parse_args()
rows_to_drop = args.drop_recent

if rows_to_drop is not None:
    drp.DropRecent().drop(rows_to_drop=rows_to_drop)
    
else:
    main_process = main.MainProcess()
    main_process.append_prices_and_returns()
    main_process.calculate_turbulence_and_systemic_risk()
    main_process.save_chart_data()
    
            
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