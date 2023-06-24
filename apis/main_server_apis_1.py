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


#
# @app.route('/getlastquotearray', methods=['GET'])
# def get_last_quote_array():
#     data = load_GetLastQuoteArray_file()
#     quote = data[0]
#
#     liquidity = quote["TotalQtyTraded"]
#     symbol = quote["InstrumentIdentifier"]
#     ltp = quote["LastTradePrice"]
#     change_percentage = quote["PriceChangePercentage"]
#
#     result = {
#         "liquidity": liquidity,
#         "symbol": symbol,
#         "ltp": ltp,
#         "change_percentage": change_percentage
#     }
#     return jsonify(result)
#
#
# # GetLastQuoteOptionGreeksChain
# @app.route('/straddle', methods=['GET'])
# def get_straddle_data():
#     data = load_straddle_data_file()
#
#     # Assuming data is a list of dictionaries
#     if len(data) > 0:
#         quote = data[0]  # Retrieve the first element from the list
#
#         call_option_price = quote["BuyPrice"]
#         put_option_price = quote["BuyPrice"]
#         print(call_option_price, put_option_price)
#
#         straddle_value = call_option_price + put_option_price
#
#         result = {
#             "straddle": {
#                 "call_option_price": call_option_price,
#                 "put_option_price": put_option_price,
#                 "straddle_value": straddle_value
#             }
#         }
#     else:
#         result = {
#             "straddle": {},
#         }
#
#     return jsonify(result)
#
#
# # GetLastQuoteArrayOptionGreeks
# @app.route('/iv_data', methods=['GET'])
# def get_iv_data():
#     data = load_iv_data_file()
#     iv_values = []
#     ivr_values = []
#     ivp_values = []
#     iv_change_values = []
#
#     for quote in data:
#         iv = quote["IV"]
#         iv_values.append(iv)
#
#     if len(iv_values) > 1:
#         for i in range(1, len(iv_values)):
#             iv_change = ((iv_values[i] - iv_values[i - 1]) / iv_values[i - 1]) * 100
#             iv_change_values.append(iv_change)
#
#         min_iv = min(iv_values)
#         max_iv = max(iv_values)
#
#         for iv in iv_values:
#             ivr = (iv - min_iv) / (max_iv - min_iv) * 100
#             ivr_values.append(ivr)
#
#         lower_iv_count = sum(iv < min_iv for iv in iv_values)
#         total_days = len(iv_values)
#
#         ivp = (lower_iv_count / total_days) * 100
#         ivp_values.append(ivp)
#
#     result = {
#         "IV_Change": iv_change_values,
#         "IV": iv_values,
#         "IVR": ivr_values,
#         "IVP": ivp_values
#     }
#
#     return jsonify(result)


@app.route('/option_dashboard', methods=['GET'])
def option_dashboard():
    last_quote_data = load_GetLastQuoteArray_file()
    straddle_data = load_straddle_data_file()
    iv_data = load_iv_data_file()
    #


    liquidity = ''
    symbol = ''
    ltp = ''
    change_percentage = ''
    call_option_price = ''
    put_option_price = ''
    straddle_value = ''
    change_percentage = ''

    # Get Last Quote Array
    if len(last_quote_data) > 0:
        last_quote = last_quote_data[0]

        liquidity = last_quote["TotalQtyTraded"]
        symbol = last_quote["InstrumentIdentifier"]
        ltp = last_quote["LastTradePrice"]
        change_percentage = last_quote["PriceChangePercentage"]

        last_quote_result = {
            "liquidity": liquidity,
            "symbol": symbol,
            "ltp": ltp,
            "change_percentage": change_percentage
        }
    else:
        last_quote_result = {}

    # Get Straddle Data
    if len(straddle_data) > 0:
        straddle_quote = straddle_data[0]

        call_option_price = straddle_quote["BuyPrice"]
        put_option_price = straddle_quote["BuyPrice"]

        straddle_value = call_option_price + put_option_price

        straddle_result = {
            "call_option_price": call_option_price,
            "put_option_price": put_option_price,
            "straddle_value": straddle_value
        }
    else:
        straddle_result = {}

    # Get IV Data
    iv_values = []
    ivr_values = []
    ivp_values = []
    iv_change_values = []

    for quote in iv_data:
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
        "last_quote_liquidity": liquidity,
        "last_quote_symbol": symbol,
        "last_quote_ltp": ltp,
        "last_quote_change_percentage": change_percentage,
        "straddle_call_option_price": call_option_price,
        "straddle_put_option_price": put_option_price,
        "straddle_value": straddle_value,
        "iv_change_values": iv_change_values,
        "iv_values": iv_values,
        "ivr_values": ivr_values,
        "ivp_values": ivp_values
    }

    return jsonify(result)


if __name__ == '__main__':
    app.run()
