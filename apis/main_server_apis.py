"""

Contains apis for website
"""

import json
from flask import Flask, jsonify

app = Flask(__name__)


def load_GetLastQuoteArray_file():
    with open('GetLastQuoteArray_realtime_file.json') as file:
        data = json.load(file)
    return data


def load_straddle_data_file():
    with open('lastquoteoptiongreekschain_realtime.json') as file:
        data = json.load(file)
    return data


def load_iv_data_file():
    with open("lastquoteoptiongreeks_realtime.json") as file:
        data = json.load(file)
    return data


def load_data_from_file(file_path):
    """
    Loads data from a JSON file.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def calculate_standard_deviation(values):
    """
    Calculates the standard deviation of a list of values.
    """
    # Calculate the mean
    mean = sum(values) / len(values)

    # Calculate the sum of squared differences from the mean
    squared_diff_sum = sum((val - mean) ** 2 for val in values)

    # Calculate the variance
    variance = squared_diff_sum / len(values)

    # Calculate the standard deviation
    standard_deviation = variance ** 0.5

    return standard_deviation


@app.route('/getlastquotearray', methods=['GET'])
def get_last_quote_array():
    data = load_GetLastQuoteArray_file()
    quote = data[0]

    liquidity = quote["TotalQtyTraded"]
    symbol = quote["InstrumentIdentifier"]
    ltp = quote["LastTradePrice"]
    change_percentage = quote["PriceChangePercentage"]

    result = {
        "liquidity": liquidity,
        "symbol": symbol,
        "ltp": ltp,
        "change_percentage": change_percentage
    }
    return jsonify(result)


# GetLastQuoteOptionGreeksChain
@app.route('/straddle', methods=['GET'])
def get_straddle_data():
    data = load_straddle_data_file()

    # Assuming data is a list of dictionaries
    if len(data) > 0:
        quote = data[0]  # Retrieve the first element from the list

        call_option_price = quote["BuyPrice"]
        put_option_price = quote["BuyPrice"]
        print(call_option_price, put_option_price)

        straddle_value = call_option_price + put_option_price

        result = {
            "straddle": {
                "call_option_price": call_option_price,
                "put_option_price": put_option_price,
                "straddle_value": straddle_value
            }
        }
    else:
        result = {
            "straddle": {},
        }

    return jsonify(result)


# GetLastQuoteArrayOptionGreeks
@app.route('/iv_data', methods=['GET'])
def get_iv_data():
    data = load_iv_data_file()
    iv_values = []
    ivr_values = []
    ivp_values = []
    iv_change_values = []

    for quote in data:
        iv = quote["IV"]
        iv_values.append(iv)

    if len(iv_values) > 1:
        for i in range(1, len(iv_values)):
            iv_change = ((iv_values[i] - iv_values[i - 1]) / iv_values[i - 1]) * 100
            iv_change_values.append(iv_change)

        min_iv = min(iv_values)
        max_iv = max(iv_values)

        for iv in iv_values:
            ivr = (iv - min_iv) / (max_iv - min_iv) * 100
            ivr_values.append(ivr)

        lower_iv_count = sum(iv < min_iv for iv in iv_values)
        total_days = len(iv_values)

        ivp = (lower_iv_count / total_days) * 100
        ivp_values.append(ivp)

    result = {
        "IV_Change": iv_change_values,
        "IV": iv_values,
        "IVR": ivr_values,
        "IVP": ivp_values
    }

    return jsonify(result)


################################################################


@app.route('/eod_iv_charts', methods=['GET'])
def get_eod_iv_charts():
    """
    Generates EOD IV charts.
    """
    # Load data from GetLastQuoteArray.json
    quote_array_data = load_data_from_file('GetLastQuoteArray_historic_file.json')

    # Load data from GetLastQuoteOptionArrayGreeks.json
    option_array_greeks_data = load_data_from_file('lastquoteoptiongreekschain_historic.json')

    # Extract relevant values for EOD IV charts
    future_prices = [quote["Close"] for quote in quote_array_data]
    iv_values = [greeks["IV"] for greeks in option_array_greeks_data]

    # Calculate RV 30D (Standard Deviation of last 30 days)
    rv_30d = calculate_standard_deviation(iv_values[-30:])

    # Calculate RV 10D (Standard Deviation of last 10 days)
    rv_10d = calculate_standard_deviation(iv_values[-10:])

    # Calculate IV-RV Spread (Implied Volatility - RV 30D)
    iv_rv_spread = [iv - rv_30d for iv in iv_values]

    # Prepare the response
    eod_iv_charts = {
        "FuturePrices": future_prices,
        "IV": iv_values,
        "RV30D": rv_30d,
        "RV10D": rv_10d,
        "IVRVSpread": iv_rv_spread
    }

    return jsonify(eod_iv_charts)


if __name__ == '__main__':
    app.run()
