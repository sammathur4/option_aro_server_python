import json
from flask import Flask, jsonify

app = Flask(__name__)


import json
from flask import jsonify

def load_GetLastQuoteArray_file():
    with open('get_last_quote.json') as file:
        data = json.load(file)
    return data

# @app.route('/option_dashboard', methods=['GET'])
# def option_dashboard():
#     last_quote_data = load_GetLastQuoteArray_file()
#     print(type(last_quote_data))
#
#     result = {
#         "data": last_quote_data['Result'],
#         "calculated_data": calculate_data(last_quote_data['Result']),
#     }
#     return jsonify(result)



@app.route('/option_dashboard', methods=['GET'])
def option_dashboard():
    last_quote_data = load_GetLastQuoteArray_file()

    result = {
        "data": last_quote_data['Result'],
        "calculated_data": calculate_data(last_quote_data['Result']),
    }

    last_quote_data['calculated_data'] = result['calculated_data']

    return jsonify(last_quote_data)



def calculate_data(data):
    calculated_data = []
    for elem in data:
        liquidity = elem["TotalQtyTraded"]
        symbol = elem["InstrumentIdentifier"]
        ltp = elem["LastTradePrice"]
        change_percentage = elem["PriceChangePercentage"]

        # Perform calculations on the data
        # Example calculation: multiply ltp by 2
        calculated_value = ltp * 2

        calculated_data.append({
            "liquidity": liquidity,
            "symbol": symbol,
            "ltp": ltp,
            "change_percentage": change_percentage,
            "calculated_value": calculated_value
        })

    return calculated_data



if __name__ == '__main__':
    app.run()

# print(option_dashboard())
