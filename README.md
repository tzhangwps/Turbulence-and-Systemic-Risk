# Turbulence Suite (0.1.0)
## Intro
- [What does this code do?](https://medium.com/@tzhangwps/measuring-financial-turbulence-and-systemic-risk-9d9688f6eec1)
- [Charts](https://terrencez.com/financial-turbulence-and-systemic-risk-charts/) for Financial Turbulence and Systemic Risk
- [Link to code](https://github.com/tzhangwps/Turbulence-Suite/blob/master/TurbulenceSuite.py)

## Credits
Author: Terrence Zhang
- [Email me](https://terrencez.com/get-in-touch/)
- [LinkedIn](https://www.linkedin.com/in/terrencezhang/)
- [My blog](https://medium.com/@tzhangwps)
- [Facebook](https://www.facebook.com/terrence.zhang.39)

## For Users
### Dependencies
Python (3.6.4)
\
Modules: [requirements.txt](https://github.com/tzhangwps/Turbulence-Suite/blob/master/requirements.txt)
\
Other dependencies needed to run the `TurbulenceSuite.py` script:
- [`turbulence_suite.py`](https://github.com/tzhangwps/Turbulence-Suite/blob/master/turbulence_suite.py) - this local module contains objects and functions to be used by the main `TurbulenceSuite.py` script.
- [`index_data.pkl`](https://github.com/tzhangwps/Turbulence-Suite/blob/master/index_data.pkl) - a pickled dataframe containing historical prices for the asset pool used to calculate Financial Turbulence and Systemic Risk.

### How to Use the Code
1. Place the main script `TurbulenceSuite.py`, the local module `turbulence_suite.py`, and the `index_data.pkl` dataframe into the same directory.
2. Run `TurbulenceSuite.py` via the command line. It takes two optional arguments. NOTE: only run one of these optional arguments at a time.
- `-a (--api_key)`
  - Invoke this argument if you want to update the Turbulence and Systemic Risk indices. This is the api key used to pull data from Alpha Vantage. You can get a free api key [here](https://www.alphavantage.co/support/#api-key).
- `-d (--drop_recent)`
  - Invoke this argument when you want to remove rows from the `index_data.pkl` dataframe, in reverse-chronological order. This is the number of rows to remove from the `index_data.pkl` dataframe. 

#### DO NOT RUN `TurbulenceSuite.py` ON WEEKDAYS
While the code can run just fine most weekdays, some weekdays (that coincide with stock market holidays) can cause the `prices` dataframe to record dates incorrectly. Therefore, it is better to run the script on Saturday or Sunday.

## For Developers
License: MIT
\
For a step-by-step explanation of the code, [click here](https://github.com/tzhangwps/Turbulence-Suite/blob/master/DeveloperGuide.md).
