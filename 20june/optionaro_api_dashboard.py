import json
from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
client = MongoClient('mongodb+srv://sammathur4:wo7kdLODmeaFG7wL@optionaro.gpzp2ko.mongodb.net/')
db = client['OPTIONARO']

get_last_quote_arrays_realtime = db['get_last_quote_arrays_realtime']
get_last_quote_arrays_historic = db['get_last_quote_arrays_historic']

lastquoteoptiongreeks_realtime_db = db["last_quote_option_greeks_realtime"]
lastquoteoptiongreeks_historic_db = db["last_quote_option_greeks_historic"]

lastquoteoptiongreekschain_realtime_db = db["lastquoteoptiongreekschain_realtime"]
lastquoteoptiongreekschain_historic_db = db["lastquoteoptiongreekschain_historic"]

database = "GetLastQuoteArray_realtime_file.json"
data = json.loads(open(database).read())

database = "lastquoteoptiongreekschain_realtime.json"
data2 = json.loads(open(database).read())

# GetLastQuoteArray
"""
ATM check

1. ek new collection- 
    KEY: Strike value, coming from name of instrument
    Ce_IV
    PE_IV
    Last Trade Time
    
2. Create a function, that Call this db using strike value, fetch ce pe values. 
   
3. This function returns straddle value. Store straddle value in new collection with strike value
"""

def get_last_quote_array():
    collection = db['get_last_quote_arrays_realtime']
    quotes = collection.find()

    results = []
    for quote in quotes:
        liquidity = quote["TotalQtyTraded"]
        symbol = quote["InstrumentIdentifier"]
        ltp = quote["LastTradePrice"]
        change_percentage = quote["PriceChangePercentage"]

        # Check if the change_percentage is a dictionary with "$numberDouble" key
        if isinstance(change_percentage, dict) and "$numberDouble" in change_percentage:
            change_percentage = change_percentage["$numberDouble"]

        # straddle_value = get_straddle_datas()
        # stradele_data = get_new_straddle_data().json

        # call_id = symbol
        # iv = iv_values.get(call_id)
        #
        # if iv is None:
        #     iv = giv()
        #     iv_values[call_id] = iv

        # print(symbol)
        # cached_data = data_cache.get(symbol)
        # pe_iv, ce_iv = 0, 0
        #
        # if cached_data is None:
        #     IV = giv()
        #     # IV = (call_iv + pe_iv)/2
        #     straddle_value = get_new_straddle_data()
        #     print(straddle_value)
        #     cached_data = {
        #         "iv": IV,
        #         "straddle_value": straddle_value
        #     }
        #     data_cache[symbol] = cached_data
        # else:
        #     IV = cached_data['iv']
        #     straddle_value = cached_data['straddle_value']
        #     print(straddle_value, cached_data['straddle_value'])

        # IV = giv()
        """
                    if CE in symbol
                    ce_iv = quote["iv]

                    if PE in symbol
                    pe_iv = quote['iv
                    """
        # if 'PE' in symbol:
        #     pe_iv = quote['IV']
        #
        # if 'CE' in symbol:
        #     ce_iv = quote['IV']

        # IV = (pe_iv + ce_iv) / 2

        result = {
            "liquidity": liquidity,
            "symbol": symbol,
            "ltp": ltp,
            "change_percentage": change_percentage,
            # "straddle_value": straddle_value,
            # "ce_iv": ce_iv,
            # "pe_iv": pe_iv,
            # "IV": IV,
        }
        print(result)
        results.append(result)

    return jsonify(results)


# Straddle Data

"""
ATM check
"""

"""
Strike price : 19500 
OPTIDX_NIFTY_06JUL2023_CE_19500

AT the money check
CALL: lastquoteoptiongreekschain will give us LTP, IV, find strike by using the last quote option
PUT: lastquoteoptiongreekschain will give us LTP, IV, find strike by using the last quote option

Every index--- 5sec
every stock -- 30 sec

NITFY ltp : lets lay 18892 - strike prices of Nitfy (19500 from name) = which val closer to 0
take that, we need only thats value ltp, call iv, put iv
for both CE and PE

"""



# IV Data


# def get_new_straddle_data():
#     get_last_quote_arrays = data
#     lastquoteoptiongreekschain_realtime = data2
#
#     closest_difference = float('inf')
#     closest_value = 0
#     IV = 0
#     straddle_value = 0
#     results = []
#
#     for quote in get_last_quote_arrays:
#         Name = quote["InstrumentIdentifier"]
#         LastTradePrice = quote["LastTradePrice"]
#
#         ans1 = [val for val in lastquoteoptiongreekschain_realtime if
#                 ((val["InstrumentIdentifier"].split("_")[1]) + '-I') == Name]
#
#         for v in ans1:
#             InstrumentIdentifier = v["InstrumentIdentifier"]
#             strike_price = float(InstrumentIdentifier.split("_")[-1])
#             difference = abs(LastTradePrice - strike_price)
#
#             if 'CE' in InstrumentIdentifier:
#                 call_ltp = v['LastTradePrice']
#             else:
#                 new_identifier = InstrumentIdentifier.replace("CE", "PE")
#                 ans2 = [vals for vals in lastquoteoptiongreekschain_realtime if
#                         vals["InstrumentIdentifier"] == new_identifier]
#                 for vals in ans2:
#                     pe_ltp = vals['LastTradePrice']
#
#             if 'PE' in InstrumentIdentifier:
#                 pe_ltp = v['LastTradePrice']
#             else:
#                 new_identifier = InstrumentIdentifier.replace("PE", "CE")
#                 ans3 = [vals for vals in lastquoteoptiongreekschain_realtime if
#                         vals["InstrumentIdentifier"] == new_identifier]
#             for vals in ans3:
#                 pe_ltp = vals['LastTradePrice']
#
#             if LastTradePrice == 0 or LastTradePrice == '':
#                 LastTradePrice = 1
#             if call_ltp == 0 or call_ltp == '':
#                 call_ltp = pe_ltp
#             if pe_ltp == 0 or pe_ltp == '':
#                 pe_ltp = call_ltp
#
#             if difference < closest_difference:
#                 closest_difference = difference
#                 closest_value = strike_price
#                 straddle_value = ((call_ltp + pe_ltp) / strike_price) * 100
#
#         result = {
#             "InstrumentIdentifier": Name,
#             "CE_LTP": call_ltp,
#             "PE_LTP": pe_ltp,
#             "straddle_value": straddle_value
#         }
#         results.append(result)
#
#     return jsonify(results)


#
# def get_new_straddle_data():
#     get_last_quote_arrays = data
#     lastquoteoptiongreekschain_realtime = data2
#
#
#     closest_difference = float('inf')
#     closest_value = 0
#     IV = 0
#     straddle_value = 0
#     results = []
#
#     for quote in get_last_quote_arrays:
#         Name = quote["InstrumentIdentifier"]
#         LastTradePrice = quote["LastTradePrice"]
#
#         ans1 = [val for val in lastquoteoptiongreekschain_realtime if
#                 ((val["InstrumentIdentifier"].split("_")[1]) + '-I') == Name]
#
#         for v in ans1:
#             InstrumentIdentifier = v["InstrumentIdentifier"]
#             strike_price = float(InstrumentIdentifier.split("_")[-1])
#
#             difference = abs(LastTradePrice - strike_price)
#
#
#             if 'CE' in InstrumentIdentifier:
#                 call_ltp = quote['LastTradePrice']
#             else:
#                 new_identifier = InstrumentIdentifier.replace("CE", "PE")
#                 ans2 = [vals for vals in lastquoteoptiongreekschain_realtime if
#                         vals["InstrumentIdentifier"] == new_identifier]
#             for vals in ans2:
#                 pe_ltp = vals['LastTradePrice']
#
#             if 'PE' in InstrumentIdentifier:
#                 pe_ltp = quote['LastTradePrice']
#             else:
#                 new_identifier = InstrumentIdentifier.replace("PE", "CE")
#                 ans3 = [vals for vals in lastquoteoptiongreekschain_realtime if
#                         vals["InstrumentIdentifier"] == new_identifier]
#             for vals in ans3:
#                 pe_ltp = vals['LastTradePrice']
#
#             if LastTradePrice == 0 or LastTradePrice == '':
#                 LastTradePrice = 1
#             if call_ltp == 0 or call_ltp == '':
#                 call_ltp = pe_ltp
#             if pe_ltp == 0 or pe_ltp == '':
#                 pe_ltp = call_ltp
#
#             if difference < closest_difference:
#                 closest_difference = difference
#                 closest_value = strike_price
#                 straddle_value = ((call_ltp + pe_ltp) / strike_price) * 100
#
#         result = {
#             "InstrumentIdentifier": Name,
#             "CE_LTP": call_ltp,
#             "PE_LTP": pe_ltp,
#             "straddle_value": straddle_value
#         }
#         results.append(result)
#
#     return jsonify(results)




iv_values = {}
# Option Dashboard




@app.route('/future_dashboard', methods=['GET'])
def future_dashboard():
    """
    return:
        PriceChangePercentage
        0.03
        OpenInterestChange
        100750
    """

    collection = db['get_last_quote_arrays_realtime']
    quotes = collection.find()

    results = []
    for quote in quotes:
        Exchange = quote["Exchange"]
        InstrumentIdentifier = quote["InstrumentIdentifier"]
        PriceChangePercentage = quote["PriceChangePercentage"]
        OpenInterestChange = quote["OpenInterestChange"]

        result = {
            "Exchange": Exchange,
            "InstrumentIdentifier": InstrumentIdentifier,
            "PriceChangePercentage": PriceChangePercentage,
            "OpenInterestChange": OpenInterestChange,
        }
        results.append(result)

    return jsonify(results)


@app.route('/live_option_chain', methods=['GET'])
def live_option_chain():
    # collection = db["lastquoteoptiongreekschain_realtime"]
    # get_last_quote_arrays = db['get_last_quote_arrays_realtime']

    results = []
    # for quote in collection.find({}):
    for quote in data2:
        # VWAP = quote["VWAP"]
        InstrumentIdentifier = quote["InstrumentIdentifier"]
        LastTradePrice = quote["LastTradePrice"]
        BuyPrice = quote["BuyPrice"]
        BuyQty = quote["BuyQty"]
        SellPrice = quote["SellPrice"]
        SellQty = quote["SellQty"]
        OpenInterest = quote["OpenInterest"]
        Value = quote["Value"]
        PriceChange = quote["PriceChange"]
        PriceChangePercentage = quote["PriceChangePercentage"]
        OpenInterestChange = quote["OpenInterestChange"]
        IV = quote["IV"]
        Delta = quote["Delta"]
        Theta = quote["Theta"]
        Vega = quote["Vega"]
        Gamma = quote["Gamma"]
        IVVwap = quote["IVVwap"]
        Vanna = quote["Vanna"]
        Charm = quote["Charm"]
        Speed = quote["Speed"]
        Zomma = quote["Zomma"]
        Color = quote["Color"]
        Volga = quote["Volga"]
        Veta = quote["Veta"]
        ThetaGammaRatio = quote["ThetaGammaRatio"]
        ThetaVegaRatio = quote["ThetaVegaRatio"]
        DTR = quote["DTR"]

        # ans1 = [val for val in get_last_quote_arrays.find({}) if
        #         val["InstrumentIdentifier"] == (InstrumentIdentifier.split("_")[1]) + '-I']

        ans1 = [val for val in data if
                val["InstrumentIdentifier"] == (InstrumentIdentifier.split("_")[1]) + '-I']

        UnderlyingLastTradePrice = 0
        for val in ans1:
            print(val["LastTradePrice"])
            UnderlyingLastTradePrice = val["LastTradePrice"]

        result = {
            "InstrumentIdentifier": InstrumentIdentifier,
            "PriceChangePercentage": PriceChangePercentage,
            "OpenInterestChange": OpenInterestChange,
            "BuyPrice": BuyPrice,
            "PriceChange": PriceChange,
            "LastTradePrice": LastTradePrice,
            "BuyQty": BuyQty,
            "SellPrice": SellPrice,
            "SellQty": SellQty,
            "Value": Value,
            "OpenInterest": OpenInterest,
            "IV": IV,
            "Theta": Theta,
            "Delta": Delta,
            "Vega": Vega,
            "Gamma": Gamma,
            "IVVwap": IVVwap,
            "Vanna": Vanna,
            "Charm": Charm,
            "Speed": Speed,
            # "VWAP": VWAP,
            "Zomma": Zomma,
            "Color": Color,
            "DTR": DTR,
            "Veta": Veta,
            "Volga": Volga,
            "ThetaGammaRatio": ThetaGammaRatio,
            "ThetaVegaRatio": ThetaVegaRatio,
            "UnderlyingLastTradePrice": UnderlyingLastTradePrice,
        }
        results.append(result)

    return {
        "Message": "Live Option Chain",
        "data": (results),
        "status": 200
    }


def calculate_iv_chart(data):
    iv_chart = []

    for item in data:
        # Extract necessary data from the item dictionary
        close_price = item['Close']
        price_change_percentage = item['PriceChangePercentage']

        # Calculate RV 30
        rv_30 = price_change_percentage * 30 ** 0.5

        # Calculate RV 10
        rv_10 = price_change_percentage * 10 ** 0.5

        # Calculate IV-RV Spread (IV-RV30)
        iv_rv_spread = calculate_implied_volatility(rv_30)

        # Calculate IV Percentile (implement your specific logic here based on Excel formula)

        # Create the IV chart dictionary for the current item
        iv_chart_item = {
            'InstrumentIdentifier': item['InstrumentIdentifier'],
            'RV 30': rv_30,
            'RV 10': rv_10,
            'IV-RV Spread': iv_rv_spread,
            'IV Percentile': None  # Replace None with the calculated IV Percentile value
        }

        iv_chart.append(iv_chart_item)

    return iv_chart


def calculate_implied_volatility(rv):
    # Implement your specific calculation for implied volatility based on RV
    # For demonstration purposes, we'll assume a simple calculation where IV = RV + 10
    implied_volatility = rv + 10
    return implied_volatility


@app.route('/implied_volatility_chart', methods=['GET'])
def get_implied_volatility_chart():
    with open('GetLastQuoteArray_realtime_file.json', 'r') as file:
        data = json.load(file)

    iv_chart = calculate_iv_chart(data)

    return jsonify(iv_chart)


if __name__ == '__main__':
    app.run()
