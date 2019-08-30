"""
Read stock data from Alpha Venture API
"""

import requests
import csv
import pprint


class APIRequest:
    def __init__(self, base_url: str, params: [str], tag: str):
        self.base_url = base_url
        self.params = params
        self.tag = tag

    @staticmethod
    def _url(base_url, params):
        param_str: str = "&".join(params)
        return "&".join([base_url, param_str])

    def get_json(self):
        response = requests.get(self.base_url, self.params)
        print(f"Request json from: {self}")
        print(f"Request parameters: {self.params}")
        if response.ok:
            return response.json()
        else:
            raise Exception(f"Fail to request from {response.url}")

    def get_meta_data(self, json: dict):
        print(type(json))
        return json['Meta Data']

    @staticmethod
    def get_time_series(json: dict):
        time_series_key = None
        for key in json.keys():
            if key.startswith("Time Series"):
                time_series_key = key
        if not time_series_key:
            raise KeyError("Unable to find the key of time series in dictionary")
        return json[time_series_key]

    def write_csv(self):
        json = self.get_json()
        print("Json requested")
        pprint.pprint(json["Meta Data"])
        time_series = self.get_time_series(json)
        title: str = f"{self.tag}_{self.params['symbol']}.csv"
        print(f"Open csv file: {title}")
        with open(title, "w") as csvfile:
            fieldnames = ["timestamp", "1. open", "2. high", "3. low", "4. close", "5. volume"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for timestamp in time_series:
                data: dict = time_series[timestamp]
                data.update({"timestamp": timestamp})
                writer.writerow(data)
        print(f"Finish writing")


"""
❚ Required: function

The time series of your choice. In this case, function=TIME_SERIES_INTRADAY

❚ Required: symbol

The name of the equity of your choice. For example: symbol=MSFT

❚ Required: interval

Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min

❚ Optional: outputsize

By default, outputsize=compact. Strings compact and full are accepted with the following specifications: compact returns only the latest 100 data points in the intraday time series; full returns the full-length intraday time series. The "compact" option is recommended if you would like to reduce the data size of each API call.

❚ Optional: datatype

By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the intraday time series in JSON format; csv returns the time series as a CSV (comma separated value) file.

❚ Required: apikey

Your API key. Claim your free API key here.

Examples (click for JSON output)

https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=MSFT&interval=5min&apikey=demo

https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=MSFT&interval=5min&outputsize=full&apikey=demo
"""


class TimeSeriesIntradayRequest(APIRequest):
    def __init__(self, symbol: str, interval: str, outputsize:str = "compact", datatype: str = "json"):
        function = "TIME_SERIES_INTRADAY"
        apikey = "X33OF6EG83E35R8A"
        self.params = {
            "function": function,
            "symbol": symbol,
            "interval": interval,
            "outputsize": outputsize,
            "datatype": datatype,
            "apikey": apikey
        }
        tag = f"intraday_{interval}"
        APIRequest.__init__(self, "https://www.alphavantage.co/query", self.params, tag=tag)


class TimeSeriesDailyRequest(APIRequest):
    """
    This API returns daily time series (date, daily open, daily high, daily low, daily close, daily volume) of the
     global equity specified, covering 20+ years of historical data.

    Required: symbol

    The name of the equity of your choice. For example: symbol=MSFT

    Optional: outputsize

    By default, outputsize=compact. Strings compact and full are accepted with the following specifications: compact returns
    only the latest 100 data points; full returns the full-length time series of 20+ years of historical data. The "compact"
    option is recommended if you would like to reduce the data size of each API call.

    Optional: datatype

    By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily
    time series in JSON format; csv returns the time series as a CSV (comma separated value) file.
    """
    def __init__(self, symbol: str, outputsize: str = "compact", datatype: str = "json"):
        function = "TIME_SERIES_DAILY"
        apikey = "X33OF6EG83E35R8A"
        self.params = {
            "function": function,
            "symbol": symbol,
            "outputsize": outputsize,
            "datatype": datatype,
            "apikey": apikey
        }
        tag = f"daily"
        APIRequest.__init__(self, "https://www.alphavantage.co/query", self.params, tag=tag)


class TimeSeriesWeeklyRequest(APIRequest):
    """
    This API returns weekly time series (last trading day of each week, weekly open, weekly high, weekly low, weekly close, weekly volume) of the global equity specified, covering 20+ years of historical data.

    The latest data point is the prices and volume information for the week (or partial week) that contains the current trading day, updated realtime.

    API Parameters:

    ❚ Required: symbol

    The name of the equity of your choice. For example: symbol=MSFT

    ❚ Optional: datatype

    By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the
    weekly time series in JSON format; csv returns the time series as a CSV (comma separated value) file.
    """
    def __init__(self, symbol: str, datatype: str = "json"):
        function = "TIME_SERIES_WEEKLY"
        apikey = "X33OF6EG83E35R8A"
        self.params = {
            "function": function,
            "symbol": symbol,
            "datatype": datatype,
            "apikey": apikey
        }
        tag = f"daily"
        APIRequest.__init__(self, "https://www.alphavantage.co/query", self.params, tag=tag)


class TimeSeriesMonthly(APIRequest):
    def __init__(self, symbol: str, datatype: str = "json"):
        function = "TIME_SERIES_WEEKLY"
        apikey = "X33OF6EG83E35R8A"
        self.params = {
            "function": function,
            "symbol": symbol,
            "datatype": datatype,
            "apikey": apikey
        }
        tag = f"daily"
        APIRequest.__init__(self, "https://www.alphavantage.co/query", self.params, tag=tag)
