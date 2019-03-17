# Turbulence Suite (0.1.0)
## For Developers
### Code Walkthrough
The following text explains what the `TurbulenceSuite.py` code does, step-by-step.
\
For instructions on how to run the code, [click here](https://github.com/tzhangwps/Turbulence-Suite/blob/master/README.md).

### Adding new data to the `index_data.pkl` file (`ts.update_weekly_prices()`)
First, `ts.update_weekly_prices()` pulls in the entire adjusted weekly price series for each asset in the asset pool, using `get_weekly_prices()`. However, there is a small nuance to the way Alpha Vantage shows weekly adjusted prices. If the request is made on a weekday that is **not** the last trading day of the week (i.e. a Friday), the first data point corresponds to the current date, instead of last Friday. For example, if I run `get_weekly_prices()` on a Wednesday, the first data point will be today, whereas ideally it would be last Friday. To deal with this issue, `get_weekly_prices()` adopts a heuristic where if the `first_date` is less than 6 days after the end of the last trading week, then we disregard the first data point. This heuristic is imperfect, so `TurbulenceSuite.py`is best run on Saturdays or Sundays.
\
\
Second, `ts.update_weekly_prices()` addresses `0` values in the API pull. This problem occurs because we are pulling U.S. and international stock market indices at the same time. For example: if this Friday is a stock market holiday in Japan, but not a stock market holiday in the U.S., then the U.S. data series will pull correctly, whereas the Japanese data series will pull in a `0`. The `replace_zero_values()` function replaces any `0` values with the prior week's ending price. Ideally in this scenario, we'd like to pull in Thursday's price (the end of this trading week) instead of last Friday's price. But since `0` values don't appear often, very little accuracy is lost from using last Friday's price.
\
\
Lastly, the new data is added to the beginning of the `prices` dataframe (in reverse chronological order), and the `prices` dataframe is saved as `index_data.pkl` in the current directory.

### `ts.add_curve_slope()`
Since we pull in treasury yield data from Alpha Vantage, we need to calculate the yield curve slope measurements. We create new fields by calculating the difference between two different points on the yield curve, and storing this difference across time. These new fields are added as new columns to the `prices` dataframe.

### Creating the `returns` object using `ts.calculate_returns()`
This calculates returns (first differences) for each asset across time, using the `first_difference()` function. For most assets, the first difference is `(new price / old price) - 1`, but for yield and yield curve slope fields, the first difference is `new price - old price`. 

### Calculating Financial Turbulence `ts.calculate_turbulence()` and Systemic Risk `ts.calculate_systemic_risk()`
For background on the calculations, [click here](https://medium.com/@tzhangwps/measuring-financial-turbulence-and-systemic-risk-9d9688f6eec1).

### Mopping Up
Output for the Financial Turbulence and Systemic Risk Indicators are converted to dataframes and saved as `.csv` files in the current directory. The first row of each `.csv` file contains strings describing each data field type.

## That's it! If you have any more questions, feel free to contact me (see the README for contact info).
