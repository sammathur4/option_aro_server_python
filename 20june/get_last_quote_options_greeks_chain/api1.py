import json
from flask import Flask, jsonify
import time

import json
import os
import asyncio
from datetime import datetime
import gfdlws as gw
from server_details import *
from bson import ObjectId
import sys
import pymongo
import websockets
import uuid

"""
Strike price : 19500 
OPTIDX_NIFTY_06JUL2023_CE_19500

AT the money check
CALL: lastquoteoptiongreekschain will give us LTP, IV, find strike by using the last quote option
PUT: lastquoteoptiongreekschain will give us LTP, IV, find strike by using the last quote option

Every index--- 5sec
every stock -- 30 sec
"""
# new_lastquoteoptiongreekschain_historic_db = db['new_lastquoteoptiongreekschain_historic_db']
client = pymongo.MongoClient('mongodb+srv://sammathur4:wo7kdLODmeaFG7wL@optionaro.gpzp2ko.mongodb.net/')
db = client['OPTIONARO']
new_lastquoteoptiongreekschain_historic_db = db['new_lastquoteoptiongreekschain_historic_db']
msg = None

endpoint, port, auth_message, api_key = details()

con = gw.ws.connect(endpoint, api_key)


def lastquoteoptiongreekschain_store(instrument):
    # while True:
    response = gw.lastquoteoptiongreekschain.get(con, 'NFO', instrument)
    # print(response)
    response_str = json.loads(response)
    if response_str['Result']:
        for item in response_str['Result']:
            item.update(
                {
                    'updated_at': datetime.now()
                }
            )
            new_lastquoteoptiongreekschain_historic_db.insert_one(item)
    #         print(item)
    #         # Check if the data entry already exists
    #         print(item['InstrumentIdentifier'])
    #         existing_entry = lastquoteoptiongreekschain_realtime_db.find_one(
    #             {'InstrumentIdentifier': item['InstrumentIdentifier']})
    #
    #         if existing_entry:
    #             current_time = datetime.now()
    #             # Update existing entry with new data
    #             item.update(
    #                 {
    #                     'updated_at': current_time
    #                 }
    #             )
    #             lastquoteoptiongreekschain_historic_db.insert_one(item)
    #             lastquoteoptiongreekschain_realtime_db.update_one(
    #                 {'InstrumentIdentifier': item['InstrumentIdentifier']}, {'$set': item})
    #             print("Existing data updated")
    #             continue
    #
    #         else:
    #             current_time = datetime.now()
    #             item.update(
    #                 {
    #                     'created_at': current_time,
    #                     'updated_at': current_time
    #                 }
    #             )
    #             lastquoteoptiongreekschain_historic_db.insert_one(item)
    #             lastquoteoptiongreekschain_realtime_db.insert_one(item)
    #
    #     print("New data added")
    #
    # print("Waiting for 5 seconds")
    # time.sleep(5)
    # print("Wait over")


# instruments = [{"Value": "39489"}]
instruments = [
    {"Value": "ACC"},
    {"Value": "ADANIENT"}, {"Value": "ADANIPORTS"}, {"Value": "AMBUJACEM"},
    {"Value": "APOLLOHOSP"},
    {"Value": "ASHOKLEY"}, {"Value": "ASIANPAINT"}, {"Value": "ASTRAL"}, {"Value": "AUBANK"},
    {"Value": "AUROPHARMA"},
    {"Value": "ASHOKLEY"}, {"Value": "BAJAJ-AUTO"}, {"Value": "BAJAJFINSV"}, {"Value": "BAJFINANCE"}, {
        "Value": "BANDHANBNK"},
    {"Value": "BANKBARODA"}, {"Value": "BATAINDIA"}, {"Value": "BEL"}, {"Value": "BERGEPAINT"},
    {"Value": "BHARATFORG"}
]

for elem in instruments:
    print(elem['Value'])
    lastquoteoptiongreekschain_store(elem['Value'])
