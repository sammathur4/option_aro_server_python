"""

Option Dashboard API

"""

"""
Save only this in database
get last option greek chain historic data
"""

# GetLastQuoteArray(ws)
# #GFDL : Returns LastTradePrice of multiple Symbols – max 25 in single call (detailed)

from import_files import *


"""
Liquidity
Symbol
LTP
% Change

"""
def GetLastQuoteArray_db():
    last_quote_Array = gw.lastquotearray.get(con, 'NFO', '[{"Value":"NIFTY-I"}, {"Value":"BANKNIFTY-I"}]', 'false')
    last_quote_Array_response_str = json.loads(last_quote_Array)

    # if last_quote_Array_response_str['Result'] and last_quote_Array_response_str['Result'] != {"MessageType": "Echo"}:
    #     return last_quote_Array_response_str


# GetLastQuoteArray_db()






def lastquoteoptiongreekschain_store():
    while True:
        response = gw.lastquoteoptiongreekschain.get(con, 'NFO', 'NIFTY')
        response_str = json.loads(response)
        if response_str['Result']:
            return response_str


# lastquoteoptiongreekschain_store()
gw.lastquoteoptiongreekschain.get(con,'NFO','NIFTY')


# # @app.route('/option_dashboard', methods=['GET'])
# def option_dashboard():
#     last_quote_Array = gw.lastquotearray.get(con, 'NFO', '[{"Value":"NIFTY-I"}, {"Value":"BANKNIFTY-I"}]', 'false')
#     last_quote_data = json.loads(last_quote_Array)
#
#
#
#
#     # last_quote_data = load_GetLastQuoteArray_file()
#     # straddle_data = load_straddle_data_file()
#     # iv_data = load_iv_data_file()
#     #
#
#     liquidity = ''
#     symbol = ''
#     ltp = ''
#     change_percentage = ''
#     call_option_price = ''
#     put_option_price = ''
#     straddle_value = ''
#     change_percentage = ''
#
#     # Get Last Quote Array
#     if len(last_quote_data) > 0:
#         last_quote = last_quote_data[0]
#
#         liquidity = last_quote["TotalQtyTraded"]
#         symbol = last_quote["InstrumentIdentifier"]
#         ltp = last_quote["LastTradePrice"]
#         change_percentage = last_quote["PriceChangePercentage"]
#
#         last_quote_result = {
#             "liquidity": liquidity,
#             "symbol": symbol,
#             "ltp": ltp,
#             "change_percentage": change_percentage
#         }
#     else:
#         last_quote_result = {}
#
#     # Get Straddle Data
#     if len(straddle_data) > 0:
#         straddle_quote = straddle_data[0]
#
#         call_option_price = straddle_quote["BuyPrice"]
#         put_option_price = straddle_quote["BuyPrice"]
#
#         straddle_value = call_option_price + put_option_price
#
#         straddle_result = {
#             "call_option_price": call_option_price,
#             "put_option_price": put_option_price,
#             "straddle_value": straddle_value
#         }
#     else:
#         straddle_result = {}
#
#     # Get IV Data
#     iv_values = []
#     ivr_values = []
#     ivp_values = []
#     iv_change_values = []
#
#     for quote in iv_data:
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
#         "last_quote_liquidity": liquidity,
#         "last_quote_symbol": symbol,
#         "last_quote_ltp": ltp,
#         "last_quote_change_percentage": change_percentage,
#         "straddle_call_option_price": call_option_price,
#         "straddle_put_option_price": put_option_price,
#         "straddle_value": straddle_value,
#         "iv_change_values": iv_change_values,
#         "iv_values": iv_values,
#         "ivr_values": ivr_values,
#         "ivp_values": ivp_values
#     }
#
#     return jsonify(result)
