# Stock Reader

This is a script to read stock  json data from API [Alpha Vantage](https://www.alphavantage.co/) and write the data to
a csv file.

## Getting Started
1. Make sure you install [requests](https://2.python-requests.org/en/master/). For example, you can install the package from PIP
```shell
pip install requests
```
2. Using it!
```python
intraday_request = TimeSeriesIntradayRequest("MSFT", "5min")
intraday_request.write_csv()
```