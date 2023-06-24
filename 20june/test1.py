# import uuid
# from import_files import *
# import asyncio
# import json
# import websockets
# from pymongo import MongoClient
#
# exg = None
# sym = None
# msg = None
# isi = None
#
# # Connect to MongoDB
# client = MongoClient('mongodb://localhost:27017')
# db = client['test1']
# collection = db['all_msg']
# collection2 = db['one_test']
#
#
# def get(ws, exchange, symbols, isShortIdentifiers):
#     exg = exchange
#     sym = symbols
#     isi = isShortIdentifiers
#     msgs = asyncio.get_event_loop().run_until_complete(mass_subscribe_n_stream(ws, exg, sym, isi))
#     print("msgs: ", msgs)
#
#     return msgs
#
#
# async def mass_subscribe_n_stream(ws, exg, sym, isi):
#     try:
#         req_msg = str(
#             '{"MessageType":"GetLastQuoteArray","Exchange":"' + exg + '","isShortIdentifiers":"' + isi + '","InstrumentIdentifiers":' + str(
#                 sym) + '}')
#         await ws.send(req_msg)
#         print("Sending Request For: " + req_msg)
#         await get_msg(ws)
#     except:
#         return msg
#
#
# async def get_msg(ws):
#     while True:
#         try:
#             message = await ws.recv()
#         except websockets.ConnectionClosedOK:
#             break
#         json_data = json.loads(message)
#         print("message direct:", json_data)
#
#         # Insert data into MongoDB
#         collection.insert_one(json_data)
#
#         if "Result" in json_data and isinstance(json_data["Result"], list):
#             current_time = datetime.now().strftime("%Y %m %d %H:%M:%S")
#             updated_time = datetime.now().strftime("%Y %m %d %H:%M:%S")
#
#             for item in json_data["Result"]:
#                 item["current_time"] = current_time
#                 item["updated_time"] = updated_time
#                 item["id"] = str(uuid.uuid4())
#
#                 # Insert data into another collection
#                 collection2.insert_one(item)
#
# instrumentidentifier1 = [
#     {"Value": "ACC-I"}, {"Value": "ADANIENT-I"}, {"Value": "ADANIPORTS-I"}, {"Value": "AMBUJACEM-I"},
#     {"Value": "APOLLOHOSP-I"},
#     {"Value": "ASHOKLEY-I"}, {"Value": "ASIANPAINT-I"}, {"Value": "ASTRAL-I"}, {"Value": "AUBANK-I"},
#     {"Value": "AUROPHARMA-I"},
#     {"Value": "ASHOKLEY-I"}, {"Value": "BAJAJ-AUTO-I"}, {"Value": "BAJAJFINSV-I"}, {"Value": "BAJFINANCE-I"}, {
#         "Value": "BANDHANBNK-I"},
#     {"Value": "BANKBARODA-I"}, {"Value": "BATAINDIA-I"}, {"Value": "BEL-I"}, {"Value": "BERGEPAINT-I"},
#     {"Value": "BHARATFORG-I"}]
#
# while True:
#     get(con, 'NFO', str(instrumentidentifier1), 'false')

#
# import pymongo
# import uuid
# import websockets
# from import_files import *
#
# client = pymongo.MongoClient('mongodb://localhost:27017')
# db = client['test1']
# main_collection = db['Realtime_1']
# historic_collection = db['Historic_1']
# msg = None
#
#
#
# def get(ws, exchange, symbols, isShortIdentifiers):
#     exg = exchange
#     sym = symbols
#     isi = isShortIdentifiers
#     msgs = asyncio.get_event_loop().run_until_complete(mass_subscribe_n_stream(ws, exg, sym, isi))
#     print("msgs: ", msgs)
#     return msgs
#
# async def mass_subscribe_n_stream(ws, exg, sym, isi):
#     try:
#         req_msg = str(
#             '{"MessageType":"GetLastQuoteArray","Exchange":"' + exg + '","isShortIdentifiers":"' + isi + '","InstrumentIdentifiers":' + str(
#                 sym) + '}')
#         await ws.send(req_msg)
#         print("Sending Request For: " + req_msg)
#         await get_msg(ws)
#     except:
#         return msg
#
# async def get_msg(ws):
#     while True:
#         try:
#             message = await ws.recv()
#         except websockets.ConnectionClosedOK:
#             break
#         json_data = json.loads(message)
#         print("message direct:", json_data)
#
#         if "Result" in json_data and isinstance(json_data["Result"], list):
#             current_time = datetime.now().strftime("%Y %m %d %H:%M:%S")
#             updated_time = datetime.now().strftime("%Y %m %d %H:%M:%S")
#
#             for item in json_data["Result"]:
#                 item["current_time"] = current_time
#                 item["updated_time"] = updated_time
#                 item["id"] = str(uuid.uuid4())
#
#                 existing_data = main_collection.find_one({"InstrumentIdentifier": item["InstrumentIdentifier"]})
#
#                 if existing_data:
#                     main_collection.update_one(
#                         {"InstrumentIdentifier": item["InstrumentIdentifier"]},
#                         {"$set": item}
#                     )
#                 else:
#                     main_collection.insert_one(item)
#
#                 historic_collection.insert_one(item)
#
#
# instrumentidentifier1 = [
#     {"Value": "ACC-I"}, {"Value": "ADANIENT-I"}, {"Value": "ADANIPORTS-I"}, {"Value": "AMBUJACEM-I"},
#     {"Value": "APOLLOHOSP-I"},
#     {"Value": "ASHOKLEY-I"}, {"Value": "ASIANPAINT-I"}, {"Value": "ASTRAL-I"}, {"Value": "AUBANK-I"},
#     {"Value": "AUROPHARMA-I"},
#     {"Value": "ASHOKLEY-I"}, {"Value": "BAJAJ-AUTO-I"}, {"Value": "BAJAJFINSV-I"}, {"Value": "BAJFINANCE-I"}, {
#         "Value": "BANDHANBNK-I"},
#     {"Value": "BANKBARODA-I"}, {"Value": "BATAINDIA-I"}, {"Value": "BEL-I"}, {"Value": "BERGEPAINT-I"},
#     {"Value": "BHARATFORG-I"}]
#
#
# while True:
#     get(con, 'NFO', str(instrumentidentifier1), 'false')


from import_files import *
endpoint, port, auth_message, api_key = details()

con = gw.ws.connect(endpoint, api_key)
gw.instruments.get(con, 'NFO', 'FUTSTK')
