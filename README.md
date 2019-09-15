# Turbulence and Systemic Risk (0.1.0)
## Intro
- [What does this code do?](https://medium.com/@tzhangwps/measuring-financial-turbulence-and-systemic-risk-9d9688f6eec1)
- [Charts](https://terrencez.com/financial-turbulence-and-systemic-risk-charts/) for Financial Turbulence and Systemic Risk
- [Link to code](https://github.com/tzhangwps/Turbulence-and-Systemic-Risk/blob/master/TurbulenceSuite_master.py)

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

### How to Use the Code
1. Download all folders and files in the repository. Maintain the file organization structure.
2. Run `TurbulenceSuite.py` via the command line. It takes one optional argument.
- `-d (--drop_recent)`
  - Invoke this argument when you want to remove rows from the `index_data.pkl` dataframe, in reverse-chronological order. This is the number of rows to remove from the `index_data.pkl` dataframe. 

#### DO NOT RUN `TurbulenceSuite.py` ON WEEKDAYS
While the code can run just fine most weekdays, some weekdays (that coincide with stock market holidays) can cause the `index_data.pkl` dataframe to record dates incorrectly. Therefore, it is better to run the script on Saturday or Sunday.

## For Developers
License: MIT
\
For a step-by-step explanation of the code, [click here](https://github.com/tzhangwps/Turbulence-Suite/blob/master/DeveloperGuide.md).
