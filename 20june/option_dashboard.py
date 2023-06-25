import json
from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
# client = MongoClient('mongodb+srv://sammathur4:wo7kdLODmeaFG7wL@optionaro.gpzp2ko.mongodb.net/')
client = MongoClient('mongodb://localhost:27017')
db = client['OPTIONARO']

get_last_quote_arrays_realtime = db['get_last_quote_arrays_realtime']
get_last_quote_arrays_historic = db['get_last_quote_arrays_historic']

lastquoteoptiongreeks_realtime_db = db["last_quote_option_greeks_realtime"]
lastquoteoptiongreeks_historic_db = db["last_quote_option_greeks_historic"]

lastquoteoptiongreekschain_realtime_db = db["lastquoteoptiongreekschain_realtime"]
lastquoteoptiongreekschain_historic_db = db["lastquoteoptiongreekschain_historic"]

new_lastquoteoptiongreekschain_historic_db = db['new_lastquoteoptiongreekschain_historic_db']

database = "GetLastQuoteArray_realtime_file.json"
data = json.loads(open(database).read())

database = "lastquoteoptiongreekschain_realtime.json"
data2 = json.loads(open(database).read())


def get_straddle_data():
    get_last_quote_arrays = db['get_last_quote_arrays_realtime']
    lastquoteoptiongreekschain_realtime = db["lastquoteoptiongreekschain_realtime"]

    results = []
    closest_difference = float('inf')
    closest_value = 0
    IV = 0
    straddle_value = 0
    ClosestInstrumentIdentifier = ''

    for quote in lastquoteoptiongreekschain_realtime.find():
        call_ltp = ''
        pe_ltp = ''
        InstrumentIdentifier = quote["InstrumentIdentifier"]

        #         # print(InstrumentIdentifier)
        strike_price = float(InstrumentIdentifier.split("_")[-1])
        #         # print("strike_price", strike_price)

        ans1 = [val for val in get_last_quote_arrays.find() if
                val["InstrumentIdentifier"] == (InstrumentIdentifier.split("_")[1]) + '-I']

        LastTradePrice = ""
        for val in ans1:
            #             # print(val["LastTradePrice"])
            LastTradePrice = val["LastTradePrice"]

        if 'CE' in InstrumentIdentifier:
            call_ltp = quote['LastTradePrice']
        else:
            new_identifier = InstrumentIdentifier.replace("CE", "PE")
            ans2 = [vals for vals in lastquoteoptiongreekschain_realtime.find() if
                    vals["InstrumentIdentifier"] == new_identifier]
            for vals in ans2:
                pe_ltp = vals['LastTradePrice']

        if 'PE' in InstrumentIdentifier:
            pe_ltp = quote['LastTradePrice']
        else:
            new_identifier = InstrumentIdentifier.replace("PE", "CE")
            ans3 = [vals for vals in lastquoteoptiongreekschain_realtime.find() if
                    vals["InstrumentIdentifier"] == new_identifier]
            for vals in ans3:
                pe_ltp = vals['LastTradePrice']

        # Needs better error handling
        # Cross check with other website data
        #         # print(call_ltp, pe_ltp, LastTradePrice)
        if LastTradePrice == 0 or LastTradePrice == '':
            LastTradePrice = 1
        if call_ltp == 0 or call_ltp == '':
            call_ltp = pe_ltp
        if pe_ltp == 0 or pe_ltp == '':
            pe_ltp = call_ltp

        difference = abs(LastTradePrice - strike_price)
        if difference < closest_difference:
            closest_difference = difference
            closest_value = strike_price
            IV = quote["IV"]
            straddle_value = ((call_ltp + pe_ltp) / strike_price) * 100
            ClosestInstrumentIdentifier = quote["InstrumentIdentifier"]

        #         # print(call_ltp, pe_ltp, LastTradePrice)
        # Straddle values
        """
        (CALL LTP + PUT LTP)/ (underlying LTP of that STOCK)  * 100
        """

    result = {
        "InstrumentIdentifier": ClosestInstrumentIdentifier,
        "IV": IV,
        "straddle_value": straddle_value
    }
    results.append(result)

    return jsonify(results)


def get_iv_data():
    collection = db["last_quote_option_greeks_realtime"]
    quotes = collection.find()

    results = []
    for quote in quotes:
        Token = quote["Token"]
        #         # print(Token)
        iv = quote["IV"]
        results.append(
            {
                "iv": iv,
                "Token": Token,

            }
        )

    return jsonify(results)


# Function to calculate straddle value
def calculate_straddle_value(atm_ce_ltp, atm_pe_ltp, underlying_ltp):
    straddle_value = (atm_ce_ltp + atm_pe_ltp) / underlying_ltp * 100
    #     # print("straddle_value", straddle_value)
    return straddle_value


# Variables to track closest ATM values
def strike_price(instrument_name):
    closest_strike = None
    closest_strike_diff = float('inf')
    closest_instrument_identifier = ''

    # Retrieve all option chain records
    records = new_lastquoteoptiongreekschain_historic_db.find()
    # Iterate over the records to find the ATM value
    for record in records:
        instrument_identifier = record["InstrumentIdentifier"]
        # print(instrument_name.replace("-I", ""), instrument_identifier)

        if instrument_name.replace("-I", "") in instrument_identifier:
            strike_prices = int(instrument_identifier.split("_")[-1])
            underlying_ltp = record["LastTradePrice"]
            # print(strike_prices, underlying_ltp)

            # Calculate the difference between the strike price and underlying LTP
            diff = abs(strike_prices - underlying_ltp)

            # Check if the current record has a closer strike price to the underlying LTP
            if diff < closest_strike_diff:
                closest_strike_diff = diff
                closest_strike = strike_prices
                closest_instrument_identifier = instrument_identifier

            if closest_instrument_identifier is None and closest_strike is None:
                return "No data", "No data"

            return closest_instrument_identifier, closest_strike


def get_last_quote_array():
    collection = db['get_last_quote_arrays_realtime']
    quotes = collection.find()

    results = []
    for quote in quotes:
        liquidity = quote["TotalQtyTraded"]
        symbol = quote["InstrumentIdentifier"]
        print(symbol)
        ltp = quote["LastTradePrice"]
        change_percentage = quote["PriceChangePercentage"]

        atm_ce_ltp = None
        atm_pe_ltp = None
        call_iv = None
        put_iv = None
        closest_strike = None
        closest_instrument_identifier = None
        closest_strike_diff = float('inf')

        # Check if the change_percentage is a dictionary with "$numberDouble" key
        if isinstance(change_percentage, dict) and "$numberDouble" in change_percentage:
            change_percentage = change_percentage["$numberDouble"]

        # Retrieve all option chain records
        records = new_lastquoteoptiongreekschain_historic_db.find()
        # Iterate over the records to find the ATM value
        for record in records:
            instrument_identifier = record["InstrumentIdentifier"]
            if symbol.replace("-I", "") in instrument_identifier:
                print("instrument_identifier", instrument_identifier, "invalid aya")
                strike_prices = float(instrument_identifier.split("_")[-1])
                underlying_ltp = float(record["LastTradePrice"])

                if underlying_ltp != 0.0:

                    # Calculate the difference between the strike price and underlying LTP
                    print(strike_prices, underlying_ltp, type(strike_prices), type(underlying_ltp))
                    diff = abs(strike_prices - underlying_ltp)

                    # Check if the current record has a closer strike price to the underlying LTP
                    if diff < closest_strike_diff:
                        closest_strike_diff = diff
                        closest_strike = strike_prices
                        closest_instrument_identifier = instrument_identifier

                    if closest_instrument_identifier is None and closest_strike is None:
                        print("No data", "No data")

            if closest_instrument_identifier is not None and closest_strike is not None:
                # for quotes in records:
                if closest_instrument_identifier.replace("-I", "") in record['InstrumentIdentifier']:
                    # print("Sssssssssssssssssssssssssssssssssssssss")

                    # Check if InstrumentIdentifier has "CE"
                    if "CE" in record["InstrumentIdentifier"]:
                        # Calculate call IV
                        call_iv = record['IV']
                        atm_ce_ltp = record['LastTradePrice']

                        # Calculate put IV
                        ce_data = record["InstrumentIdentifier"]

                        record_put_iv = new_lastquoteoptiongreekschain_historic_db.find(
                            {"InstrumentIdentifier": ce_data.replace("CE", "PE")})
                        if record_put_iv is not None:
                            for elem in record_put_iv:
                                put_iv = elem['IV']
                                atm_pe_ltp = elem['LastTradePrice']
                                #                                 # print("Put IV1:", put_iv)
                                break

                    # Check if InstrumentIdentifier has "CE"
                    elif "PE" in record["InstrumentIdentifier"]:
                        # Calculate call IV
                        put_iv = record['IV']
                        atm_pe_ltp = record['LastTradePrice']

                        # Calculate put IV
                        pe_data = record["InstrumentIdentifier"]

                        print(pe_data.replace("PE", "CE"), record["InstrumentIdentifier"])

                        record_ce_iv = new_lastquoteoptiongreekschain_historic_db.find(
                            {"InstrumentIdentifier": pe_data.replace("PE", "CE")})
                        if record_ce_iv is not None:
                            for elem in record_ce_iv:
                                call_iv = elem['IV']
                                atm_ce_ltp = elem['LastTradePrice']
                                #                                 # print("CE IV1:", call_iv)
                                break
                        else:
                            pass

                    print("atm_ce_ltp, atm_pe_ltp, closest_strike", atm_ce_ltp, atm_pe_ltp, closest_strike)
                    # straddle = calculate_straddle_value(atm_ce_ltp, atm_pe_ltp, closest_strike)
                    if atm_pe_ltp is not None and atm_pe_ltp is not None and closest_strike is not None:
                        straddle = ((atm_ce_ltp + atm_pe_ltp) / closest_strike) * 100
                        """
                        IV value for underlying:
                           (atm call's IV + atm put IV) /2
                        """
                        IV = (call_iv + put_iv) / 2

                        result = {
                            "liquidity": liquidity,
                            "symbol": symbol,
                            "ltp": ltp,
                            "change_percentage": change_percentage,
                            "straddle_value": straddle,
                            "ce_iv": call_iv,
                            "pe_iv": put_iv,
                            "IV": IV,
                        }
                        results.append(result)

                else:
                    pass
        else:
            pass

    return jsonify(results)


@app.route('/option_dashboard', methods=['GET'])
def option_dashboard():
    result = {
        "last_quote_data": get_last_quote_array().json,
    }

    return jsonify(result)


if __name__ == '__main__':
    app.run()

########################
########################
######################

# `
# # Calculate call IV
# # call_iv = calculate_call_iv()
#
#
# # Calculate put IV
# # put_iv = calculate_put_iv()
# # # # print("Put IV:", put_iv)
#
#
# # if __name__ == '__main__':
# # # # print("Straddle value:", straddle)
# # # # print("Call IV:", call_iv)
# # # # print("Put IV:", put_iv)
# # app.run()
#
#
# # GetLastQuoteArray
# """
# ATM check
#
# 1. ek new collection-
#     KEY: Strike value, coming from name of instrument
#     Ce_IV
#     PE_IV
#     Last Trade Time
#
# 2. Create a function, that Call this db using strike value, fetch ce pe values.
#
# 3. This function returns straddle value. Store straddle value in new collection with strike value
# """
# """
# ATM: at the money
# """
#
# import json
# from flask import Flask, jsonify
# from pymongo import MongoClient
#
# app = Flask(__name__)
#
# # MongoDB connection
# client = MongoClient('mongodb+srv://sammathur4:wo7kdLODmeaFG7wL@optionaro.gpzp2ko.mongodb.net/')
# db = client['OPTIONARO']
#
# get_last_quote_arrays_realtime = db['get_last_quote_arrays_realtime']
# get_last_quote_arrays_historic = db['get_last_quote_arrays_historic']
#
# lastquoteoptiongreeks_realtime_db = db["last_quote_option_greeks_realtime"]
# lastquoteoptiongreeks_historic_db = db["last_quote_option_greeks_historic"]
#
# lastquoteoptiongreekschain_realtime_db = db["lastquoteoptiongreekschain_realtime"]
# lastquoteoptiongreekschain_historic_db = db["lastquoteoptiongreekschain_historic"]
#
# database = "GetLastQuoteArray_realtime_file.json"
# data = json.loads(open(database).read())
#
# database = "lastquoteoptiongreekschain_realtime.json"
# data2 = json.loads(open(database).read())
#
#
# def get_straddle_data():
#     get_last_quote_arrays = db['get_last_quote_arrays_realtime']
#     lastquoteoptiongreekschain_realtime = db["lastquoteoptiongreekschain_realtime"]
#
#     results = []
#     closest_difference = float('inf')
#     closest_value = 0
#     IV = 0
#     straddle_value = 0
#     ClosestInstrumentIdentifier = ''
#
#     for quote in lastquoteoptiongreekschain_realtime.find():
#         call_ltp = ''
#         pe_ltp = ''
#         InstrumentIdentifier = quote["InstrumentIdentifier"]
#
# # #         print(InstrumentIdentifier)
#         strike_price = float(InstrumentIdentifier.split("_")[-1])
# # #         print("strike_price", strike_price)
#
#         ans1 = [val for val in get_last_quote_arrays.find() if
#                 val["InstrumentIdentifier"] == (InstrumentIdentifier.split("_")[1]) + '-I']
#
#         LastTradePrice = ""
#         for val in ans1:
# # #             print(val["LastTradePrice"])
#             LastTradePrice = val["LastTradePrice"]
#
#         if 'CE' in InstrumentIdentifier:
#             call_ltp = quote['LastTradePrice']
#         else:
#             new_identifier = InstrumentIdentifier.replace("CE", "PE")
#             ans2 = [vals for vals in lastquoteoptiongreekschain_realtime.find() if
#                     vals["InstrumentIdentifier"] == new_identifier]
#             for vals in ans2:
#                 pe_ltp = vals['LastTradePrice']
#
#         if 'PE' in InstrumentIdentifier:
#             pe_ltp = quote['LastTradePrice']
#         else:
#             new_identifier = InstrumentIdentifier.replace("PE", "CE")
#             ans3 = [vals for vals in lastquoteoptiongreekschain_realtime.find() if
#                     vals["InstrumentIdentifier"] == new_identifier]
#             for vals in ans3:
#                 pe_ltp = vals['LastTradePrice']
#
#         # Needs better error handling
#         # Cross check with other website data
# # #         print(call_ltp, pe_ltp, LastTradePrice)
#         if LastTradePrice == 0 or LastTradePrice == '':
#             LastTradePrice = 1
#         if call_ltp == 0 or call_ltp == '':
#             call_ltp = pe_ltp
#         if pe_ltp == 0 or pe_ltp == '':
#             pe_ltp = call_ltp
#
#         difference = abs(LastTradePrice - strike_price)
#         if difference < closest_difference:
#             closest_difference = difference
#             closest_value = strike_price
#             IV = quote["IV"]
#             straddle_value = ((call_ltp + pe_ltp) / strike_price) * 100
#             ClosestInstrumentIdentifier = quote["InstrumentIdentifier"]
#
# # #         print(call_ltp, pe_ltp, LastTradePrice)
#         # Straddle values
#         """
#         (CALL LTP + PUT LTP)/ (underlying LTP of that STOCK)  * 100
#         """
#
#     result = {
#         "InstrumentIdentifier": ClosestInstrumentIdentifier,
#         "IV": IV,
#         "straddle_value": straddle_value
#     }
#     results.append(result)
#
#     return jsonify(results)
#
#
# def get_iv_data():
#     collection = db["last_quote_option_greeks_realtime"]
#     quotes = collection.find()
#
#     results = []
#     for quote in quotes:
#         Token = quote["Token"]
# # #         print(Token)
#         iv = quote["IV"]
#         results.append(
#             {
#                 "iv": iv,
#                 "Token": Token,
#
#             }
#         )
#
#     return jsonify(results)
#
#
# # Function to calculate straddle value
# def calculate_straddle_value(atm_ce_ltp, atm_pe_ltp, underlying_ltp):
#     straddle_value = (atm_ce_ltp + atm_pe_ltp) / underlying_ltp * 100
# # #     print("straddle_value", straddle_value)
#     return straddle_value
#
#
# # Retrieve all option chain records
# records = lastquoteoptiongreekschain_realtime_db.find()
#
#
# # Variables to track closest ATM values
# def strike_price():
#     closest_strike = None
#     closest_strike_diff = float('inf')
#     closest_instrument_identifier = ''
#
#     # Iterate over the records to find the ATM value
#     for record in records:
#         instrument_identifier = record["InstrumentIdentifier"]
# # #         print(instrument_identifier.split("_")[-1])
#         strike_price = int(instrument_identifier.split("_")[-1])
#         underlying_ltp = record["LastTradePrice"]
#
#         # Calculate the difference between the strike price and underlying LTP
#         diff = abs(strike_price - underlying_ltp)
#
#         # Check if the current record has a closer strike price to the underlying LTP
#         if diff < closest_strike_diff:
#             closest_strike_diff = diff
#             closest_strike = strike_price
#             closest_instrument_identifier = instrument_identifier
# # #             # print(instrument_identifier)
#
#     # Print the closest ATM value (strike price)
# # #     print("Closest Instrument Identifier:", closest_instrument_identifier)
# # #     print("ATM Value (Strike Price):", closest_strike)
#
#     return closest_instrument_identifier, closest_strike
#
#
# straddle = calculate_straddle_value(atm_ce_ltp, atm_pe_ltp, closest_strike)
#
#
# def get_last_quote_array():
#     collection = db['get_last_quote_arrays_realtime']
#     quotes = collection.find()
#
#     results = []
#     for quote in quotes:
#         liquidity = quote["TotalQtyTraded"]
#         symbol = quote["InstrumentIdentifier"]
#         ltp = quote["LastTradePrice"]
#         change_percentage = quote["PriceChangePercentage"]
#
#         # Check if the change_percentage is a dictionary with "$numberDouble" key
#         if isinstance(change_percentage, dict) and "$numberDouble" in change_percentage:
#             change_percentage = change_percentage["$numberDouble"]
#
#         # straddle_value = get_straddle_datas()
#         # stradele_data = get_new_straddle_data().json
#
#         # call_id = symbol
#         # iv = iv_values.get(call_id)
#         #
#         # if iv is None:
#         #     iv = giv()
#         #     iv_values[call_id] = iv
#
# # #         # print(symbol)
#         # cached_data = data_cache.get(symbol)
#         # pe_iv, ce_iv = 0, 0
#         #
#         # if cached_data is None:
#         #     IV = giv()
#         #     # IV = (call_iv + pe_iv)/2
#         #     straddle_value = get_new_straddle_data()
# # #         #     print(straddle_value)
#         #     cached_data = {
#         #         "iv": IV,
#         #         "straddle_value": straddle_value
#         #     }
#         #     data_cache[symbol] = cached_data
#         # else:
#         #     IV = cached_data['iv']
#         #     straddle_value = cached_data['straddle_value']
# # #         #     print(straddle_value, cached_data['straddle_value'])
#
#         # IV = giv()
#         """
#             if CE in symbol
#             ce_iv = quote["iv]
#
#             if PE in symbol
#             pe_iv = quote['iv
#         """
#
#         "Straddle value = (ATM CE ltp + ATM PE ltp / Underlying LTP) *100"
#
#         atm_ce_ltp = None
#         atm_pe_ltp = None
#         ce_iv = None
#         put_iv = None
#
#         closest_instrument_identifier, closest_strike = strike_price()
#         record = lastquoteoptiongreekschain_realtime_db.find({"InstrumentIdentifier": closest_instrument_identifier})
#         for quotes in record:
#             # Check if InstrumentIdentifier has "CE"
#             if "CE" in quotes["InstrumentIdentifier"]:
#                 # Calculate call IV
#                 call_iv = quotes['IV']
#                 atm_ce_ltp = quotes['LastTradePrice']
# # #                 print("Call IV:", call_iv)
#
#                 # Calculate put IV
#                 ce_data = quotes["InstrumentIdentifier"]
#                 pe_data = ce_data.replace("CE", "PE")
#                 record_put_iv = lastquoteoptiongreekschain_realtime_db.find({"InstrumentIdentifier": pe_data})
#                 if record_put_iv is not None:
#                     for elem in record_put_iv:
#                         put_iv = elem['IV']
#                         atm_pe_ltp = quotes['LastTradePrice']
# # #                         print("Put IV:", put_iv)
#                 else:
#                     pass
#
#             # Check if InstrumentIdentifier has "CE"
#             if "PE" in quotes["InstrumentIdentifier"]:
#                 # Calculate call IV
#                 put_iv = quotes['IV']
#                 atm_pe_ltp = quotes['LastTradePrice']
# # #                 print("Put IV:", put_iv)
#
#                 # Calculate put IV
#                 pe_data = quotes["InstrumentIdentifier"]
#                 ce_data = pe_data.replace("PE", "CE")
#                 record_ce_iv = lastquoteoptiongreekschain_realtime_db.find({"InstrumentIdentifier": ce_data})
#                 if record_ce_iv is not None:
#                     for elem in record_ce_iv:
#                         ce_iv = elem['IV']
#                         atm_ce_ltp = quotes['LastTradePrice']
# # #                         print("CE IV:", ce_iv)
#                 else:
#                     pass
#
#         if ce_iv is not None and put_iv is not None:
#             IV = (ce_iv + put_iv) / 2
#         else:
#             IV = 0.0
#
#         result = {
#             "liquidity": liquidity,
#             "symbol": symbol,
#             "ltp": ltp,
#             "change_percentage": change_percentage,
#             "straddle_value": calculate_straddle_value(atm_ce_ltp, atm_pe_ltp, closest_strike),
#             "ce_iv": ce_iv,
#             "pe_iv": put_iv,
#             "IV": IV,
#         }
# # #         print(result)
#         results.append(result)
#
#     return jsonify(results)
#
#
# @app.route('/option_dashboard', methods=['GET'])
# def option_dashboard():
#     last_quote_data = get_last_quote_array().json
#     # straddle_data = get_straddle_data().json
#     """
#     IV value for underlying:
#        (atm call's IV + atm put IV) /2
#     """
#
#     # iv_data = get_iv_data().json
#
#     result = {
#         "last_quote_data": last_quote_data,
#         # "straddle_data": straddle_data,
#         # "iv_data": iv_data
#     }
#
#     return jsonify(result)
#
#
# if __name__ == '__main__':
#     app.run()`
