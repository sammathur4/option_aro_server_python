# # # """
# # # Symbol (1)		Last Trade Price (1)										IV and IV Change (2)
# # #
# # #
# # #
# # #
# # #
# # #
# # #
# # #
# # # 										Call IV and Put IV = IV of ATM Call and Put (3)
# # # 	Any stock that has a turnover of > 150cr on the previous day than it is liquid. (1)					Price Percentage Change (1)
# # #
# # #
# # #
# # #
# # #
# # #
# # #
# # # 	Instructions:
# # #
# # # 	1. Create a database that stores the result of calculations like Straddle, IVR and IVP.
# # # 	2. Now create an API named "OptionDashboard"
# # # 	3. Add Turnover, Symbol, LTP, Price % change, Call IV and PUT IV along with the results of calculations done and stored in step no. 1, add IV and Change in IV
# # # 	4. Connect the api that is created in step 3 with the front end of Option Dashboard Page.
# # #
# # #
# # #
# #
# #
# # from flask import Flask, jsonify
# # from pymongo import MongoClient
# #
# # app = Flask(__name__)
# #
# # # MongoDB connection
# # client = MongoClient('mongodb://localhost:27017')
# # db = client['OPTIONARO']
# #
# # # # 1
# #
# # get_last_quote_arrays_realtime = db['get_last_quote_arrays_realtime']
# # get_last_quote_arrays_historic = db['get_last_quote_arrays_historic']
# # #
# # # # 2
# # lastquoteoptiongreeks_realtime_db = db["last_quote_option_greeks_realtime"]
# # lastquoteoptiongreeks_historic_db = db["last_quote_option_greeks_historic"]
# #
# # # # 3
# # lastquoteoptiongreekschain_realtime_db = db["lastquoteoptiongreekschain_realtime"]
# # lastquoteoptiongreekschain_historic_db = db["lastquoteoptiongreekschain_historic"]
# #
# #
# # #
# #
# # # GetLastQuoteArray
# # def get_last_quote_array():
# #     collection = db['get_last_quote_arrays_realtime']
# #     quotes = collection.find()
# #
# #     results = []
# #     for quote in quotes:
# #         liquidity = quote["TotalQtyTraded"]
# #         symbol = quote["InstrumentIdentifier"]
# #         ltp = quote["LastTradePrice"]
# #         change_percentage = quote["PriceChangePercentage"]
# #
# #         result = {
# #             "liquidity": liquidity,
# #             "symbol": symbol,
# #             "ltp": ltp,
# #             "change_percentage": change_percentage
# #         }
# #         results.append(result)
# #
# #     return jsonify(results)
# #
# #
# # # Straddle Data
# #
# # """
# # ATM check
# # """
# #
# # """
# # Strike price : 19500
# # OPTIDX_NIFTY_06JUL2023_CE_19500
# #
# # AT the money check
# # CALL: lastquoteoptiongreekschain will give us LTP, IV, find strike by using the last quote option
# # PUT: lastquoteoptiongreekschain will give us LTP, IV, find strike by using the last quote option
# #
# # Every index--- 5sec
# # every stock -- 30 sec
# #
# # NITFY ltp : lets lay 18892 - strike prices of Nitfy (19500 from name) = which val closer to 0
# # take that, we need only thats value ltp, call iv, put iv
# # for both CE and PE
# #
# # """
# #
# #
# # def get_straddle_data():
# #     get_last_quote_arrays = db['get_last_quote_arrays_realtime']
# #     lastquoteoptiongreekschain_realtime = db["lastquoteoptiongreekschain_realtime"]
# #     quotes = lastquoteoptiongreekschain_realtime.find()
# #
# #     results = []
# #     for quote in quotes:
# #         call_ltp = ''
# #         pe_ltp = ''
# #         InstrumentIdentifier = quote["InstrumentIdentifier"]
# #
# #         print(InstrumentIdentifier)
# #         strike_price = (InstrumentIdentifier.split("_")[-1])
# #         print("strike_price", strike_price)
# #
# #         ans1 = get_last_quote_arrays.find({"InstrumentIdentifier": InstrumentIdentifier})
# #
# #         LastTradePrice = ''
# #         for val in ans1:
# #             print(val["LastTradePrice"])
# #             LastTradePrice = val["LastTradePrice"]
# #
# #         if 'CE' in InstrumentIdentifier:
# #             call_ltp = quote['LastTradePrice']
# #         else:
# #             new_identifier = InstrumentIdentifier.replace("CE", "PE")
# #             ans2 = lastquoteoptiongreekschain_realtime.find({"InstrumentIdentifier": new_identifier})
# #             for vals in ans2:
# #                 pe_ltp = vals['LastTradePrice']
# #
# #         if 'PE' in InstrumentIdentifier:
# #             pe_ltp = quote['LastTradePrice']
# #         else:
# #             new_identifier = InstrumentIdentifier.replace("PE", "CE")
# #             ans3 = lastquoteoptiongreekschain_realtime.find({"InstrumentIdentifier": new_identifier})
# #             for vals in ans3:
# #                 pe_ltp = vals['LastTradePrice']
# #
# #         IV = quote["IV"]
# #
# #         # Needs better error handling
# #         # Cross check with other website data
# #         print(call_ltp, pe_ltp, LastTradePrice)
# #         if LastTradePrice == 0 or LastTradePrice == '': LastTradePrice = 1
# #         if call_ltp == 0 or call_ltp == '': call_ltp = pe_ltp
# #         if pe_ltp == 0 or pe_ltp == '': pe_ltp = call_ltp
# #
# #         straddle_value = ((call_ltp + pe_ltp) / int(strike_price)) * 100
# #         print(call_ltp, pe_ltp, LastTradePrice)
# #         # Straddle values
# #         """
# #         (CALL LTP + PUT LTP)/ (underlying LTP of that STOCK)  * 100
# #         """
# #
# #         result = {
# #             "InstrumentIdentifier": InstrumentIdentifier,
# #             "IV": IV,
# #             "straddle_value": straddle_value
# #         }
# #         results.append(result)
# #
# #     return jsonify(results)
# #
# #
# # # IV Data
# # def get_iv_data():
# #     collection = db["last_quote_option_greeks_realtime"]
# #     quotes = collection.find()
# #
# #     results = []
# #     for quote in quotes:
# #         Token = quote["Token"]
# #         print(Token)
# #         iv = quote["IV"]
# #         results.append(
# #             {
# #                 "iv": iv,
# #                 "Token": Token,
# #
# #             }
# #         )
# #
# #     return jsonify(results)
# #
# #
# # # Option Dashboard
# #
# # """
# # ATM: at the money
# # """
# #
# #
# # @app.route('/option_dashboard', methods=['GET'])
# # def option_dashboard():
# #     last_quote_data = get_last_quote_array().json
# #     straddle_data = get_straddle_data().json
# #     """
# #     IV value for underlying:
# #        (atm call's IV + atm put IV) /2
# #     """
# #
# #     iv_data = get_iv_data().json
# #
# #     result = {
# #         "last_quote_data": last_quote_data,
# #         "straddle_data": straddle_data,
# #         "iv_data": iv_data
# #     }
# #
# #     return jsonify(result)
# #
# #
# # @app.route('/future_dashboard', methods=['GET'])
# # def future_dashboard():
# #     """
# #     return:
# #         PriceChangePercentage
# #         0.03
# #         OpenInterestChange
# #         100750
# #     """
# #
# #     collection = db['get_last_quote_arrays_realtime']
# #     quotes = collection.find()
# #
# #     results = []
# #     for quote in quotes:
# #         Exchange = quote["Exchange"]
# #         InstrumentIdentifier = quote["InstrumentIdentifier"]
# #         PriceChangePercentage = quote["PriceChangePercentage"]
# #         OpenInterestChange = quote["OpenInterestChange"]
# #
# #         result = {
# #             "Exchange": Exchange,
# #             "InstrumentIdentifier": InstrumentIdentifier,
# #             "PriceChangePercentage": PriceChangePercentage,
# #             "OpenInterestChange": OpenInterestChange,
# #         }
# #         results.append(result)
# #
# #     return jsonify(results)
# #
# #
# # @app.route('/live_option_chain', methods=['GET'])
# # def live_option_chain():
# #     collection = db["lastquoteoptiongreekschain_realtime"]
# #     quotes = collection.find()
# #
# #     results = []
# #     for quote in quotes:
# #         # VWAP = quote["VWAP"]
# #         InstrumentIdentifier = quote["InstrumentIdentifier"]
# #         LastTradePrice = quote["LastTradePrice"]
# #         BuyPrice = quote["BuyPrice"]
# #         BuyQty = quote["BuyQty"]
# #         SellPrice = quote["SellPrice"]
# #         SellQty = quote["SellQty"]
# #         OpenInterest = quote["OpenInterest"]
# #         Value = quote["Value"]
# #         PriceChange = quote["PriceChange"]
# #         PriceChangePercentage = quote["PriceChangePercentage"]
# #         OpenInterestChange = quote["OpenInterestChange"]
# #         IV = quote["IV"]
# #         Delta = quote["Delta"]
# #         Theta = quote["Theta"]
# #         Vega = quote["Vega"]
# #         Gamma = quote["Gamma"]
# #         IVVwap = quote["IVVwap"]
# #         Vanna = quote["Vanna"]
# #         Charm = quote["Charm"]
# #         Speed = quote["Speed"]
# #         Zomma = quote["Zomma"]
# #         Color = quote["Color"]
# #         Volga = quote["Volga"]
# #         Veta = quote["Veta"]
# #         ThetaGammaRatio = quote["ThetaGammaRatio"]
# #         ThetaVegaRatio = quote["ThetaVegaRatio"]
# #         DTR = quote["DTR"]
# #
# #         result = {
# #             "InstrumentIdentifier": InstrumentIdentifier,
# #             "PriceChangePercentage": PriceChangePercentage,
# #             "OpenInterestChange": OpenInterestChange,
# #             "BuyPrice": BuyPrice,
# #             "PriceChange": PriceChange,
# #             "LastTradePrice": LastTradePrice,
# #             "BuyQty": BuyQty,
# #             "SellPrice": SellPrice,
# #             "SellQty": SellQty,
# #             "Value": Value,
# #             "OpenInterest": OpenInterest,
# #             "IV": IV,
# #             "Theta": Theta,
# #             "Delta": Delta,
# #             "Vega": Vega,
# #             "Gamma": Gamma,
# #             "IVVwap": IVVwap,
# #             "Vanna": Vanna,
# #             "Charm": Charm,
# #             "Speed": Speed,
# #             # "VWAP": VWAP,
# #             "Zomma": Zomma,
# #             "Color": Color,
# #             "DTR": DTR,
# #             "Veta": Veta,
# #             "Volga": Volga,
# #             "ThetaGammaRatio": ThetaGammaRatio,
# #             "ThetaVegaRatio": ThetaVegaRatio,
# #         }
# #         results.append(result)
# #
# #     return {
# #         "Message": "Live Option Chain",
# #         "data": jsonify(results),
# #         "status": 200
# #     }
# #
# #
# # if __name__ == '__main__':
# #     app.run()
#
#
#
#
# # """
# # Symbol (1)		Last Trade Price (1)										IV and IV Change (2)
# #
# #
# #
# #
# #
# #
# #
# #
# # 										Call IV and Put IV = IV of ATM Call and Put (3)
# # 	Any stock that has a turnover of > 150cr on the previous day than it is liquid. (1)					Price Percentage Change (1)
# #
# #
# #
# #
# #
# #
# #
# # 	Instructions:
# #
# # 	1. Create a database that stores the result of calculations like Straddle, IVR and IVP.
# # 	2. Now create an API named "OptionDashboard"
# # 	3. Add Turnover, Symbol, LTP, Price % change, Call IV and PUT IV along with the results of calculations done and stored in step no. 1, add IV and Change in IV
# # 	4. Connect the api that is created in step 3 with the front end of Option Dashboard Page.
# #
# #
# #
#
#
# from flask import Flask, jsonify
# from pymongo import MongoClient
#
# app = Flask(__name__)
#
# # MongoDB connection
# client = MongoClient('mongodb://localhost:27017')
# db = client['OPTIONARO']
#
# # # 1
#
# get_last_quote_arrays_realtime = db['get_last_quote_arrays_realtime']
# get_last_quote_arrays_historic = db['get_last_quote_arrays_historic']
# #
# # # 2
# lastquoteoptiongreeks_realtime_db = db["last_quote_option_greeks_realtime"]
# lastquoteoptiongreeks_historic_db = db["last_quote_option_greeks_historic"]
#
# # # 3
# lastquoteoptiongreekschain_realtime_db = db["lastquoteoptiongreekschain_realtime"]
# lastquoteoptiongreekschain_historic_db = db["lastquoteoptiongreekschain_historic"]
#
#
# #
#
# # GetLastQuoteArray
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
#         result = {
#             "liquidity": liquidity,
#             "symbol": symbol,
#             "ltp": ltp,
#             "change_percentage": change_percentage
#         }
#         results.append(result)
#
#     return jsonify(results)
#
#
# # Straddle Data
#
# """
# ATM check
# """
#
# """
# Strike price : 19500
# OPTIDX_NIFTY_06JUL2023_CE_19500
#
# AT the money check
# CALL: lastquoteoptiongreekschain will give us LTP, IV, find strike by using the last quote option
# PUT: lastquoteoptiongreekschain will give us LTP, IV, find strike by using the last quote option
#
# Every index--- 5sec
# every stock -- 30 sec
#
# NITFY ltp : lets lay 18892 - strike prices of Nitfy (19500 from name) = which val closer to 0
# take that, we need only thats value ltp, call iv, put iv
# for both CE and PE
#
# """
#
#
# def get_straddle_data():
#     get_last_quote_arrays = db['get_last_quote_arrays_realtime']
#     lastquoteoptiongreekschain_realtime = db["lastquoteoptiongreekschain_realtime"]
#     quotes = lastquoteoptiongreekschain_realtime.find()
#
#     results = []
#     straddle_values = []
#     for quote in quotes:
#         call_ltp = ''
#         pe_ltp = ''
#         InstrumentIdentifier = quote["InstrumentIdentifier"]
#
#         print(InstrumentIdentifier)
#         strike_price = (InstrumentIdentifier.split("_")[-1])
#         print("strike_price", strike_price)
#
#         ans1 = get_last_quote_arrays.find({"InstrumentIdentifier": InstrumentIdentifier})
#
#         LastTradePrice = ''
#         for val in ans1:
#             print(val["LastTradePrice"])
#             LastTradePrice = val["LastTradePrice"]
#
#         if 'CE' in InstrumentIdentifier:
#             call_ltp = quote['LastTradePrice']
#         else:
#             new_identifier = InstrumentIdentifier.replace("CE", "PE")
#             ans2 = lastquoteoptiongreekschain_realtime.find({"InstrumentIdentifier": new_identifier})
#             for vals in ans2:
#                 pe_ltp = vals['LastTradePrice']
#
#         if 'PE' in InstrumentIdentifier:
#             pe_ltp = quote['LastTradePrice']
#         else:
#             new_identifier = InstrumentIdentifier.replace("PE", "CE")
#             ans3 = lastquoteoptiongreekschain_realtime.find({"InstrumentIdentifier": new_identifier})
#             for vals in ans3:
#                 pe_ltp = vals['LastTradePrice']
#
#         IV = quote["IV"]
#
#         # Needs better error handling
#         # Cross check with other website data
#         print(call_ltp, pe_ltp, LastTradePrice)
#         if LastTradePrice == 0 or LastTradePrice == '': LastTradePrice = 1
#         if call_ltp == 0 or call_ltp == '': call_ltp = pe_ltp
#         if pe_ltp == 0 or pe_ltp == '': pe_ltp = call_ltp
#
#         straddle_value = ((call_ltp + pe_ltp) / int(strike_price)) * 100
#         straddle_values.append(straddle_value)
#         print(call_ltp, pe_ltp, LastTradePrice)
#         # Straddle values
#         """
#         (CALL LTP + PUT LTP)/ (underlying LTP of that STOCK)  * 100
#         """
#
#         result = {
#             "InstrumentIdentifier": InstrumentIdentifier,
#             "IV": IV,
#             "straddle_value": straddle_value
#         }
#         results.append(result)
#
#     return jsonify(results)
#
#
# # IV Data
# def get_iv_data():
#     collection = db["last_quote_option_greeks_realtime"]
#     quotes = collection.find()
#
#     results = []
#     for quote in quotes:
#         Token = quote["Token"]
#         print(Token)
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
# # Option Dashboard
#
# """
# ATM: at the money
# """
#
#
# @app.route('/option_dashboard', methods=['GET'])
# def option_dashboard():
#     last_quote_data = get_last_quote_array().json
#     straddle_data = get_straddle_data().json
#     """
#     IV value for underlying:
#        (atm call's IV + atm put IV) /2
#     """
#
#     iv_data = get_iv_data().json
#
#     result = {
#         "last_quote_data": last_quote_data,
#         "straddle_data": straddle_data,
#         "iv_data": iv_data
#     }
#
#     return jsonify(result)
#
#
# @app.route('/future_dashboard', methods=['GET'])
# def future_dashboard():
#     """
#     return:
#         PriceChangePercentage
#         0.03
#         OpenInterestChange
#         100750
#     """
#
#     collection = db['get_last_quote_arrays_realtime']
#     quotes = collection.find()
#
#     results = []
#     for quote in quotes:
#         Exchange = quote["Exchange"]
#         InstrumentIdentifier = quote["InstrumentIdentifier"]
#         PriceChangePercentage = quote["PriceChangePercentage"]
#         OpenInterestChange = quote["OpenInterestChange"]
#
#         result = {
#             "Exchange": Exchange,
#             "InstrumentIdentifier": InstrumentIdentifier,
#             "PriceChangePercentage": PriceChangePercentage,
#             "OpenInterestChange": OpenInterestChange,
#         }
#         results.append(result)
#
#     return jsonify(results)
#
#
# @app.route('/live_option_chain', methods=['GET'])
# def live_option_chain():
#     collection = db["lastquoteoptiongreekschain_realtime"]
#     quotes = collection.find()
#
#     results = []
#     for quote in quotes:
#         # VWAP = quote["VWAP"]
#         InstrumentIdentifier = quote["InstrumentIdentifier"]
#         LastTradePrice = quote["LastTradePrice"]
#         BuyPrice = quote["BuyPrice"]
#         BuyQty = quote["BuyQty"]
#         SellPrice = quote["SellPrice"]
#         SellQty = quote["SellQty"]
#         OpenInterest = quote["OpenInterest"]
#         Value = quote["Value"]
#         PriceChange = quote["PriceChange"]
#         PriceChangePercentage = quote["PriceChangePercentage"]
#         OpenInterestChange = quote["OpenInterestChange"]
#         IV = quote["IV"]
#         Delta = quote["Delta"]
#         Theta = quote["Theta"]
#         Vega = quote["Vega"]
#         Gamma = quote["Gamma"]
#         IVVwap = quote["IVVwap"]
#         Vanna = quote["Vanna"]
#         Charm = quote["Charm"]
#         Speed = quote["Speed"]
#         Zomma = quote["Zomma"]
#         Color = quote["Color"]
#         Volga = quote["Volga"]
#         Veta = quote["Veta"]
#         ThetaGammaRatio = quote["ThetaGammaRatio"]
#         ThetaVegaRatio = quote["ThetaVegaRatio"]
#         DTR = quote["DTR"]
#
#         result = {
#             "InstrumentIdentifier": InstrumentIdentifier,
#             "PriceChangePercentage": PriceChangePercentage,
#             "OpenInterestChange": OpenInterestChange,
#             "BuyPrice": BuyPrice,
#             "PriceChange": PriceChange,
#             "LastTradePrice": LastTradePrice,
#             "BuyQty": BuyQty,
#             "SellPrice": SellPrice,
#             "SellQty": SellQty,
#             "Value": Value,
#             "OpenInterest": OpenInterest,
#             "IV": IV,
#             "Theta": Theta,
#             "Delta": Delta,
#             "Vega": Vega,
#             "Gamma": Gamma,
#             "IVVwap": IVVwap,
#             "Vanna": Vanna,
#             "Charm": Charm,
#             "Speed": Speed,
#             # "VWAP": VWAP,
#             "Zomma": Zomma,
#             "Color": Color,
#             "DTR": DTR,
#             "Veta": Veta,
#             "Volga": Volga,
#             "ThetaGammaRatio": ThetaGammaRatio,
#             "ThetaVegaRatio": ThetaVegaRatio,
#         }
#         results.append(result)
#
#     return {
#         "Message": "Live Option Chain",
#         "data": jsonify(results),
#         "status": 200
#     }
#
#
# if __name__ == '__main__':
#     app.run()
#


# # # """
# # # Symbol (1)		Last Trade Price (1)										IV and IV Change (2)
# # #
# # #
# # #
# # #
# # #
# # #
# # #
# # #
# # # 										Call IV and Put IV = IV of ATM Call and Put (3)
# # # 	Any stock that has a turnover of > 150cr on the previous day than it is liquid. (1)					Price Percentage Change (1)
# # #
# # #
# # #
# # #
# # #
# # #
# # #
# # # 	Instructions:
# # #
# # # 	1. Create a database that stores the result of calculations like Straddle, IVR and IVP.
# # # 	2. Now create an API named "OptionDashboard"
# # # 	3. Add Turnover, Symbol, LTP, Price % change, Call IV and PUT IV along with the results of calculations done and stored in step no. 1, add IV and Change in IV
# # # 	4. Connect the api that is created in step 3 with the front end of Option Dashboard Page.
# # #
# # #
# # #
# #
# #
# # from flask import Flask, jsonify
# # from pymongo import MongoClient
# #
# # app = Flask(__name__)
# #
# # # MongoDB connection
# # client = MongoClient('mongodb://localhost:27017')
# # db = client['OPTIONARO']
# #
# # # # 1
# #
# # get_last_quote_arrays_realtime = db['get_last_quote_arrays_realtime']
# # get_last_quote_arrays_historic = db['get_last_quote_arrays_historic']
# # #
# # # # 2
# # lastquoteoptiongreeks_realtime_db = db["last_quote_option_greeks_realtime"]
# # lastquoteoptiongreeks_historic_db = db["last_quote_option_greeks_historic"]
# #
# # # # 3
# # lastquoteoptiongreekschain_realtime_db = db["lastquoteoptiongreekschain_realtime"]
# # lastquoteoptiongreekschain_historic_db = db["lastquoteoptiongreekschain_historic"]
# #
# #
# # #
# #
# # # GetLastQuoteArray
# # def get_last_quote_array():
# #     collection = db['get_last_quote_arrays_realtime']
# #     quotes = collection.find()
# #
# #     results = []
# #     for quote in quotes:
# #         liquidity = quote["TotalQtyTraded"]
# #         symbol = quote["InstrumentIdentifier"]
# #         ltp = quote["LastTradePrice"]
# #         change_percentage = quote["PriceChangePercentage"]
# #
# #         result = {
# #             "liquidity": liquidity,
# #             "symbol": symbol,
# #             "ltp": ltp,
# #             "change_percentage": change_percentage
# #         }
# #         results.append(result)
# #
# #     return jsonify(results)
# #
# #
# # # Straddle Data
# #
# # """
# # ATM check
# # ask FE
# #
# #
# # """
# #
# # """
# # Strike price : 19500
# # OPTIDX_NIFTY_06JUL2023_CE_19500
# #
# # AT the money check
# # CALL: lastquoteoptiongreekschain will give us LTP, IV, find strike by using the last quote option
# # PUT: lastquoteoptiongreekschain will give us LTP, IV, find strike by using the last quote option
# #
# # Every index--- 5sec
# # every stock -- 30 sec
# # """
# #
# #
# # def get_straddle_data():
# #     get_last_quote_arrays = db['get_last_quote_arrays_realtime']
# #     lastquoteoptiongreekschain_realtime = db["lastquoteoptiongreekschain_realtime"]
# #     quotes = lastquoteoptiongreekschain_realtime.find()
# #
# #     results = []
# #     for quote in quotes:
# #         call_ltp = ''
# #         pe_ltp = ''
# #         InstrumentIdentifier = quote["InstrumentIdentifier"]
# #
# #         print(InstrumentIdentifier)
# #         strike_price = (InstrumentIdentifier.split("_")[-1])
# #         print("strike_price", strike_price)
# #
# #         ans1 = get_last_quote_arrays.find({"InstrumentIdentifier": InstrumentIdentifier})
# #
# #         LastTradePrice = ''
# #         for val in ans1:
# #             print(val["LastTradePrice"])
# #             LastTradePrice = val["LastTradePrice"]
# #
# #         if 'CE' in InstrumentIdentifier:
# #             call_ltp = quote['LastTradePrice']
# #         else:
# #             new_identifier = InstrumentIdentifier.replace("CE", "PE")
# #             ans2 = lastquoteoptiongreekschain_realtime.find({"InstrumentIdentifier": new_identifier})
# #             for vals in ans2:
# #                 pe_ltp = vals['LastTradePrice']
# #
# #         if 'PE' in InstrumentIdentifier:
# #             pe_ltp = quote['LastTradePrice']
# #         else:
# #             new_identifier = InstrumentIdentifier.replace("PE", "CE")
# #             ans3 = lastquoteoptiongreekschain_realtime.find({"InstrumentIdentifier": new_identifier})
# #             for vals in ans3:
# #                 pe_ltp = vals['LastTradePrice']
# #
# #         IV = quote["IV"]
# #
# #         # Needs better error handling
# #         # Cross check with other website data
# #         print(call_ltp, pe_ltp, LastTradePrice)
# #         if LastTradePrice == 0 or LastTradePrice == '': LastTradePrice = 1
# #         if call_ltp == 0 or call_ltp == '': call_ltp = pe_ltp
# #         if pe_ltp == 0 or pe_ltp == '': pe_ltp = call_ltp
# #
# #         straddle_value = ((call_ltp + pe_ltp) / int(strike_price)) * 100
# #         print(call_ltp, pe_ltp, LastTradePrice)
# #         # Straddle values
# #         """
# #         (CALL LTP + PUT LTP)/ (underlying LTP of that STOCK)  * 100
# #         """
# #
# #         result = {
# #             "InstrumentIdentifier": InstrumentIdentifier,
# #             "IV": IV,
# #             "straddle_value": straddle_value
# #         }
# #         results.append(result)
# #
# #     return jsonify(results)
# #
# #
# # # IV Data
# # def get_iv_data():
# #     collection = db["last_quote_option_greeks_realtime"]
# #     quotes = collection.find()
# #
# #     results = []
# #     for quote in quotes:
# #         Token = quote["Token"]
# #         print(Token)
# #         iv = quote["IV"]
# #         results.append(
# #             {
# #                 "iv": iv,
# #                 "Token": Token,
# #
# #             }
# #         )
# #
# #     return jsonify(results)
# #
# #
# # # Option Dashboard
# #
# # """
# # ATM: at the money
# # """
# #
# #
# # @app.route('/option_dashboard', methods=['GET'])
# # def option_dashboard():
# #     last_quote_data = get_last_quote_array().json
# #     straddle_data = get_straddle_data().json
# #     """
# #     IV value for underlying:
# #        (atm call's IV + atm put IV) /2
# #     """
# #
# #     iv_data = get_iv_data().json
# #
# #     result = {
# #         "last_quote_data": last_quote_data,
# #         "straddle_data": straddle_data,
# #         "iv_data": iv_data
# #     }
# #
# #     return jsonify(result)
# #
# #
# # @app.route('/future_dashboard', methods=['GET'])
# # def future_dashboard():
# #     """
# #     return:
# #         PriceChangePercentage
# #         0.03
# #         OpenInterestChange
# #         100750
# #     """
# #
# #     collection = db['get_last_quote_arrays_realtime']
# #     quotes = collection.find()
# #
# #     results = []
# #     for quote in quotes:
# #         Exchange = quote["Exchange"]
# #         InstrumentIdentifier = quote["InstrumentIdentifier"]
# #         PriceChangePercentage = quote["PriceChangePercentage"]
# #         OpenInterestChange = quote["OpenInterestChange"]
# #
# #         result = {
# #             "Exchange": Exchange,
# #             "InstrumentIdentifier": InstrumentIdentifier,
# #             "PriceChangePercentage": PriceChangePercentage,
# #             "OpenInterestChange": OpenInterestChange,
# #         }
# #         results.append(result)
# #
# #     return jsonify(results)
# #
# #
# # @app.route('/live_option_chain', methods=['GET'])
# # def live_option_chain():
# #     collection = db["lastquoteoptiongreekschain_realtime"]
# #     quotes = collection.find()
# #
# #     results = []
# #     for quote in quotes:
# #         # VWAP = quote["VWAP"]
# #         InstrumentIdentifier = quote["InstrumentIdentifier"]
# #         LastTradePrice = quote["LastTradePrice"]
# #         BuyPrice = quote["BuyPrice"]
# #         BuyQty = quote["BuyQty"]
# #         SellPrice = quote["SellPrice"]
# #         SellQty = quote["SellQty"]
# #         OpenInterest = quote["OpenInterest"]
# #         Value = quote["Value"]
# #         PriceChange = quote["PriceChange"]
# #         PriceChangePercentage = quote["PriceChangePercentage"]
# #         OpenInterestChange = quote["OpenInterestChange"]
# #         IV = quote["IV"]
# #         Delta = quote["Delta"]
# #         Theta = quote["Theta"]
# #         Vega = quote["Vega"]
# #         Gamma = quote["Gamma"]
# #         IVVwap = quote["IVVwap"]
# #         Vanna = quote["Vanna"]
# #         Charm = quote["Charm"]
# #         Speed = quote["Speed"]
# #         Zomma = quote["Zomma"]
# #         Color = quote["Color"]
# #         Volga = quote["Volga"]
# #         Veta = quote["Veta"]
# #         ThetaGammaRatio = quote["ThetaGammaRatio"]
# #         ThetaVegaRatio = quote["ThetaVegaRatio"]
# #         DTR = quote["DTR"]
# #
# #         result = {
# #             "InstrumentIdentifier": InstrumentIdentifier,
# #             "PriceChangePercentage": PriceChangePercentage,
# #             "OpenInterestChange": OpenInterestChange,
# #             "BuyPrice": BuyPrice,
# #             "PriceChange": PriceChange,
# #             "LastTradePrice": LastTradePrice,
# #             "BuyQty": BuyQty,
# #             "SellPrice": SellPrice,
# #             "SellQty": SellQty,
# #             "Value": Value,
# #             "OpenInterest": OpenInterest,
# #             "IV": IV,
# #             "Theta": Theta,
# #             "Delta": Delta,
# #             "Vega": Vega,
# #             "Gamma": Gamma,
# #             "IVVwap": IVVwap,
# #             "Vanna": Vanna,
# #             "Charm": Charm,
# #             "Speed": Speed,
# #             # "VWAP": VWAP,
# #             "Zomma": Zomma,
# #             "Color": Color,
# #             "DTR": DTR,
# #             "Veta": Veta,
# #             "Volga": Volga,
# #             "ThetaGammaRatio": ThetaGammaRatio,
# #             "ThetaVegaRatio": ThetaVegaRatio,
# #         }
# #         results.append(result)
# #
# #     return {
# #         "Message": "Live Option Chain",
# #         "data": jsonify(results),
# #         "status": 200
# #     }
# #
# #
# # if __name__ == '__main__':
# #     app.run()
#
#
# # """
# # Symbol (1)		Last Trade Price (1)										IV and IV Change (2)
# #
# #
# #
# #
# #
# #
# #
# #
# # 										Call IV and Put IV = IV of ATM Call and Put (3)
# # 	Any stock that has a turnover of > 150cr on the previous day than it is liquid. (1)					Price Percentage Change (1)
# #
# #
# #
# #
# #
# #
# #
# # 	Instructions:
# #
# # 	1. Create a database that stores the result of calculations like Straddle, IVR and IVP.
# # 	2. Now create an API named "OptionDashboard"
# # 	3. Add Turnover, Symbol, LTP, Price % change, Call IV and PUT IV along with the results of calculations done and stored in step no. 1, add IV and Change in IV
# # 	4. Connect the api that is created in step 3 with the front end of Option Dashboard Page.
# #
# #
# #
#
# # """
# # Symbol (1)		Last Trade Price (1)										IV and IV Change (2)
# #
# #
# #
# #
# #
# #
# #
# #
# # 										Call IV and Put IV = IV of ATM Call and Put (3)
# # 	Any stock that has a turnover of > 150cr on the previous day than it is liquid. (1)					Price Percentage Change (1)
# #
# #
# #
# #
# #
# #
# #
# # 	Instructions:
# #
# # 	1. Create a database that stores the result of calculations like Straddle, IVR and IVP.
# # 	2. Now create an API named "OptionDashboard"
# # 	3. Add Turnover, Symbol, LTP, Price % change, Call IV and PUT IV along with the results of calculations done and stored in step no. 1, add IV and Change in IV
# # 	4. Connect the api that is created in step 3 with the front end of Option Dashboard Page.
# #
# #
# #
#
#
# from flask import Flask, jsonify
# from pymongo import MongoClient
#
# app = Flask(__name__)
# #
# # # MongoDB connection
# # client = MongoClient('mongodb://localhost:27017')
# # db = client['OPTIONARO']
# #
# # # # 1
# #
# # get_last_quote_arrays_realtime = db['get_last_quote_arrays_realtime']
# # get_last_quote_arrays_historic = db['get_last_quote_arrays_historic']
# # #
# # # # 2
# # lastquoteoptiongreeks_realtime_db = db["last_quote_option_greeks_realtime"]
# # lastquoteoptiongreeks_historic_db = db["last_quote_option_greeks_historic"]
# #
# # # # 3
# # lastquoteoptiongreekschain_realtime_db = db["lastquoteoptiongreekschain_realtime"]
# # lastquoteoptiongreekschain_historic_db = db["lastquoteoptiongreekschain_historic"]
# #
# #
# # #
# import json
#
# # Load data from JSON files
# with open('get_last_quote_arrays_realtime.json') as file:
#     get_last_quote_arrays_realtime_data = json.load(file)
#
# with open('get_last_quote_arrays_historic.json') as file:
#     get_last_quote_arrays_historic_data = json.load(file)
#
# with open('last_quote_option_greeks_realtime.json') as file:
#     lastquoteoptiongreeks_realtime_data = json.load(file)
#
# with open('last_quote_option_greeks_historic.json') as file:
#     lastquoteoptiongreeks_historic_data = json.load(file)
#
# with open('lastquoteoptiongreekschain_realtime.json') as file:
#     lastquoteoptiongreekschain_realtime_data = json.load(file)
#
# with open('lastquoteoptiongreekschain_historic.json') as file:
#     lastquoteoptiongreekschain_historic_data = json.load(file)
#
# # Access data as dictionaries
# get_last_quote_arrays_realtime = get_last_quote_arrays_realtime_data['get_last_quote_arrays_realtime']
# get_last_quote_arrays_historic = get_last_quote_arrays_historic_data['get_last_quote_arrays_historic']
# lastquoteoptiongreeks_realtime_db = lastquoteoptiongreeks_realtime_data['last_quote_option_greeks_realtime']
# lastquoteoptiongreeks_historic_db = lastquoteoptiongreeks_historic_data['last_quote_option_greeks_historic']
# lastquoteoptiongreekschain_realtime_db = lastquoteoptiongreekschain_realtime_data['lastquoteoptiongreekschain_realtime']
# lastquoteoptiongreekschain_historic_db = lastquoteoptiongreekschain_historic_data['lastquoteoptiongreekschain_historic']
#
#
# # GetLastQuoteArray
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
#         result = {
#             "liquidity": liquidity,
#             "symbol": symbol,
#             "ltp": ltp,
#             "change_percentage": change_percentage
#         }
#         results.append(result)
#
#     return jsonify(results)
#
#
# # Straddle Data
#
# """
# ATM check
# """
#
# """
# Strike price : 19500
# OPTIDX_NIFTY_06JUL2023_CE_19500
#
# AT the money check
# CALL: lastquoteoptiongreekschain will give us LTP, IV, find strike by using the last quote option
# PUT: lastquoteoptiongreekschain will give us LTP, IV, find strike by using the last quote option
#
# Every index--- 5sec
# every stock -- 30 sec
#
# NITFY ltp : lets lay 18892 - strike prices of Nitfy (19500 from name) = which val closer to 0
# take that, we need only thats value ltp, call iv, put iv
# for both CE and PE
#
# """
#
#
# def get_straddle_data():
#     get_last_quote_arrays = db['get_last_quote_arrays_realtime']
#     lastquoteoptiongreekschain_realtime = db["lastquoteoptiongreekschain_realtime"]
#     quotes = lastquoteoptiongreekschain_realtime.find()
#
#     results = []
#     LastTradePrice = ''
#     atm = float('inf')
#     for quote in quotes:
#         call_ltp = ''
#         pe_ltp = ''
#         InstrumentIdentifier = quote["InstrumentIdentifier"]
#
#         print(InstrumentIdentifier)
#         strike_price = (InstrumentIdentifier.split("_")[-1])
#         print("strike_price", strike_price)
#
#         ans1 = get_last_quote_arrays.find({"InstrumentIdentifier": "NIFTY-I"})
#
#         for val in ans1:
#             print("val[LastTradePrice]", val["LastTradePrice"])
#             LastTradePrice = val["LastTradePrice"]
#
#         if 'CE' in InstrumentIdentifier:
#             call_ltp = quote['LastTradePrice']
#         else:
#             new_identifier = InstrumentIdentifier.replace("CE", "PE")
#             ans2 = lastquoteoptiongreekschain_realtime.find({"InstrumentIdentifier": new_identifier})
#             for vals in ans2:
#                 pe_ltp = vals['LastTradePrice']
#
#         if 'PE' in InstrumentIdentifier:
#             pe_ltp = quote['LastTradePrice']
#         else:
#             new_identifier = InstrumentIdentifier.replace("PE", "CE")
#             ans3 = lastquoteoptiongreekschain_realtime.find({"InstrumentIdentifier": new_identifier})
#             for vals in ans3:
#                 pe_ltp = vals['LastTradePrice']
#
#         # Needs better error handling
#         # Cross check with other website data
#         print(call_ltp, pe_ltp, LastTradePrice)
#         if LastTradePrice == 0 or LastTradePrice == '': LastTradePrice = 1
#         if call_ltp == 0 or call_ltp == '': call_ltp = pe_ltp
#         if pe_ltp == 0 or pe_ltp == '': pe_ltp = call_ltp
#
#         difference = abs(LastTradePrice - int(strike_price))
#         print("difference", difference)
#         if difference < atm:
#             atm = difference
#             closest_value = strike_price
#             IV = quote["IV"]
#             straddle_value = ((call_ltp + pe_ltp) / int(strike_price)) * 100
#             ClosestInstrumentIdentifier = quote["InstrumentIdentifier"]
#
#         print(call_ltp, pe_ltp, LastTradePrice)
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
# # IV Data
# def get_iv_data():
#     collection = db["last_quote_option_greeks_realtime"]
#     quotes = collection.find()
#
#     results = []
#     for quote in quotes:
#         Token = quote["Token"]
#         print(Token)
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
# # Option Dashboard
#
# """
# ATM: at the money
# """
#
#
# @app.route('/option_dashboard', methods=['GET'])
# def option_dashboard():
#     last_quote_data = get_last_quote_array().json
#     straddle_data = get_straddle_data().json
#     """
#     IV value for underlying:
#        (atm call's IV + atm put IV) /2
#     """
#
#     iv_data = get_iv_data().json
#
#     result = {
#         "last_quote_data": last_quote_data,
#         "straddle_data": straddle_data,
#         "iv_data": iv_data
#     }
#
#     return jsonify(result)
#
#
# @app.route('/future_dashboard', methods=['GET'])
# def future_dashboard():
#     """
#     return:
#         PriceChangePercentage
#         0.03
#         OpenInterestChange
#         100750
#
#     Long buildup
#     Short Buildup
#     Short COvering
#     Long unwinding
#     """
#
#     collection = db['get_last_quote_arrays_realtime']
#     quotes = collection.find()
#
#     results = []
#     for quote in quotes:
#         Exchange = quote["Exchange"]
#         InstrumentIdentifier = quote["InstrumentIdentifier"]
#         PriceChangePercentage = quote["PriceChangePercentage"]
#         OpenInterestChange = quote["OpenInterestChange"]
#
#         result = {
#             "Exchange": Exchange,
#             "InstrumentIdentifier": InstrumentIdentifier,
#             "PriceChangePercentage": PriceChangePercentage,
#             "OpenInterestChange": OpenInterestChange,
#         }
#         results.append(result)
#
#     return jsonify(results)
#
#
# @app.route('/live_option_chain', methods=['GET'])
# def live_option_chain():
#     collection = db["lastquoteoptiongreekschain_realtime"]  # ---PUTS and CALLS ltp
#     quotes = collection.find()
#
#     results = []
#     for quote in quotes:
#         # VWAP = quote["VWAP"]
#         InstrumentIdentifier = quote["InstrumentIdentifier"]
#         LastTradePrice = quote["LastTradePrice"]
#         """
#         Underlying ltp
#         """
#
#         BuyPrice = quote["BuyPrice"]
#         BuyQty = quote["BuyQty"]
#         SellPrice = quote["SellPrice"]
#         SellQty = quote["SellQty"]
#         OpenInterest = quote["OpenInterest"]
#         Value = quote["Value"]
#         PriceChange = quote["PriceChange"]
#         PriceChangePercentage = quote["PriceChangePercentage"]
#         OpenInterestChange = quote["OpenInterestChange"]
#         IV = quote["IV"]
#         Delta = quote["Delta"]
#         Theta = quote["Theta"]
#         Vega = quote["Vega"]
#         Gamma = quote["Gamma"]
#         IVVwap = quote["IVVwap"]
#         Vanna = quote["Vanna"]
#         Charm = quote["Charm"]
#         Speed = quote["Speed"]
#         Zomma = quote["Zomma"]
#         Color = quote["Color"]
#         Volga = quote["Volga"]
#         Veta = quote["Veta"]
#         ThetaGammaRatio = quote["ThetaGammaRatio"]
#         ThetaVegaRatio = quote["ThetaVegaRatio"]
#         DTR = quote["DTR"]
#
#         result = {
#             "InstrumentIdentifier": InstrumentIdentifier,
#             "PriceChangePercentage": PriceChangePercentage,
#             "OpenInterestChange": OpenInterestChange,
#             "BuyPrice": BuyPrice,
#             "PriceChange": PriceChange,
#             "LastTradePrice": LastTradePrice,
#             "BuyQty": BuyQty,
#             "SellPrice": SellPrice,
#             "SellQty": SellQty,
#             "Value": Value,
#             "OpenInterest": OpenInterest,
#             "IV": IV,
#             "Theta": Theta,
#             "Delta": Delta,
#             "Vega": Vega,
#             "Gamma": Gamma,
#             "IVVwap": IVVwap,
#             "Vanna": Vanna,
#             "Charm": Charm,
#             "Speed": Speed,
#             # "VWAP": VWAP,
#             "Zomma": Zomma,
#             "Color": Color,
#             "DTR": DTR,
#             "Veta": Veta,
#             "Volga": Volga,
#             "ThetaGammaRatio": ThetaGammaRatio,
#             "ThetaVegaRatio": ThetaVegaRatio,
#         }
#         results.append(result)
#
#     return {
#         "Message": "Live Option Chain",
#         "data": jsonify(results),
#         "status": 200
#     }
#
#
#
# @app.route('/live_option_chain', methods=['GET'])
# def live_option_chain():
#
# if __name__ == '__main__':
#     app.run()
import random


def get_straddle_datas():
    return random.randint(155, 389) / 100


def giv():
    base_iv = random.uniform(0.1, 0.5)  # Range of base IV values
    adjustment = random.uniform(-0.05, 0.05)  # Range of adjustment values

    # Apply adjustment to the base IV
    iv = base_iv + adjustment

    # Limit the IV within the range of 0.1 to 0.5
    iv = max(0.1, min(0.5, iv))

    return iv


import json

# """
# Symbol (1)		Last Trade Price (1)										IV and IV Change (2)
#
#
#
#
#
#
#
#
# 										Call IV and Put IV = IV of ATM Call and Put (3)
# 	Any stock that has a turnover of > 150cr on the previous day than it is liquid. (1)					Price Percentage Change (1)
#
#
#
#
#
#
#
# 	Instructions:
#
# 	1. Create a database that stores the result of calculations like Straddle, IVR and IVP.
# 	2. Now create an API named "OptionDashboard"
# 	3. Add Turnover, Symbol, LTP, Price % change, Call IV and PUT IV along with the results of calculations done and stored in step no. 1, add IV and Change in IV
# 	4. Connect the api that is created in step 3 with the front end of Option Dashboard Page.
#
#
#


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

        straddle_value = get_straddle_datas()
        IV = giv()

        result = {
            "liquidity": liquidity,
            "symbol": symbol,
            "ltp": ltp,
            "change_percentage": change_percentage,
            "straddle_value": straddle_value,
            "IV": IV,
        }
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
#         print(InstrumentIdentifier)
#         strike_price = float(InstrumentIdentifier.split("_")[-1])
#         print("strike_price", strike_price)
#
#         ans1 = [val for val in get_last_quote_arrays.find() if val["InstrumentIdentifier"] == (InstrumentIdentifier.split("_")[1])+'-I']
#
#         LastTradePrice=""
#         for val in ans1:
#             print(val["LastTradePrice"])
#             LastTradePrice = val["LastTradePrice"]
#
#         if 'CE' in InstrumentIdentifier:
#             call_ltp = quote['LastTradePrice']
#         else:
#             new_identifier = InstrumentIdentifier.replace("CE", "PE")
#             ans2 = [vals for vals in lastquoteoptiongreekschain_realtime.find() if vals["InstrumentIdentifier"] == new_identifier]
#             for vals in ans2:
#                 pe_ltp = vals['LastTradePrice']
#
#         if 'PE' in InstrumentIdentifier:
#             pe_ltp = quote['LastTradePrice']
#         else:
#             new_identifier = InstrumentIdentifier.replace("PE", "CE")
#             ans3 = [vals for vals in lastquoteoptiongreekschain_realtime.find() if vals["InstrumentIdentifier"] == new_identifier]
#             for vals in ans3:
#                 pe_ltp = vals['LastTradePrice']
#
#         # Needs better error handling
#         # Cross check with other website data
#         print(call_ltp, pe_ltp, LastTradePrice)
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
#         print(call_ltp, pe_ltp, LastTradePrice)
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


def get_straddle_data():
    get_last_quote_arrays = data
    lastquoteoptiongreekschain_realtime = data2

    results = []
    closest_difference = float('inf')
    closest_value = 0
    IV = 0
    straddle_value = 0
    ClosestInstrumentIdentifier = ''

    for quote in lastquoteoptiongreekschain_realtime:
        call_ltp = ''
        pe_ltp = ''
        InstrumentIdentifier = quote["InstrumentIdentifier"]

        print(InstrumentIdentifier)
        strike_price = float(InstrumentIdentifier.split("_")[-1])
        print("strike_price", strike_price)

        ans1 = [val for val in get_last_quote_arrays if
                val["InstrumentIdentifier"] == (InstrumentIdentifier.split("_")[1]) + '-I']

        for val in ans1:
            print(val["LastTradePrice"])
            LastTradePrice = val["LastTradePrice"]

        if 'CE' in InstrumentIdentifier:
            call_ltp = quote['LastTradePrice']
        else:
            new_identifier = InstrumentIdentifier.replace("CE", "PE")
            ans2 = [vals for vals in lastquoteoptiongreekschain_realtime if
                    vals["InstrumentIdentifier"] == new_identifier]
            for vals in ans2:
                pe_ltp = vals['LastTradePrice']

        if 'PE' in InstrumentIdentifier:
            pe_ltp = quote['LastTradePrice']
        else:
            new_identifier = InstrumentIdentifier.replace("PE", "CE")
            ans3 = [vals for vals in lastquoteoptiongreekschain_realtime if
                    vals["InstrumentIdentifier"] == new_identifier]
            for vals in ans3:
                pe_ltp = vals['LastTradePrice']

        # Needs better error handling
        # Cross check with other website data
        print(call_ltp, pe_ltp, LastTradePrice)
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

        print(call_ltp, pe_ltp, LastTradePrice)
        # Straddle values
        """
        (CALL LTP + PUT LTP)/ (underlying LTP of that STOCK) * 100
        """

    result = {
        "InstrumentIdentifier": ClosestInstrumentIdentifier,
        "IV": IV,
        # "straddle_value": straddle_value
    }
    results.append(result)

    return jsonify(results)


# IV Data
def get_iv_data():
    collection = db["last_quote_option_greeks_realtime"]
    quotes = collection.find()

    results = []
    for quote in quotes:
        Token = quote["Token"]
        print(Token)
        iv = quote["IV"]
        results.append(
            {
                "iv": iv,
                "Token": Token,

            }
        )

    return jsonify(results)


# Option Dashboard

"""
ATM: at the money
"""


@app.route('/option_dashboard', methods=['GET'])
def option_dashboard():
    last_quote_data = get_last_quote_array().json
    # straddle_data = get_straddle_data().json
    """
    IV value for underlying:
       (atm call's IV + atm put IV) /2
    """

    # iv_data = get_iv_data().json

    result = {
        "last_quote_data": last_quote_data,
        # "straddle_data": straddle_data,
        # "iv_data": iv_data
    }

    return jsonify(result)


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
    collection = db["lastquoteoptiongreekschain_realtime"]
    get_last_quote_arrays = db['get_last_quote_arrays_realtime']

    results = []
    for quote in collection:
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

        ans1 = [val for val in get_last_quote_arrays if
                val["InstrumentIdentifier"] == (InstrumentIdentifier.split("_")[1]) + '-I']

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
        "data": jsonify(results),
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
