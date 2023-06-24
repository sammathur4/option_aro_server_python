
import asyncio
import json
import time
from datetime import datetime
import gfdlws as gw
from server_api_details import *
from bson import ObjectId
#
#
# # client = pymongo.MongoClient("mongodb://localhost:27017")
#
# client = pymongo.MongoClient("mongodb+srv://sammathur4:wo7kdLODmeaFG7wL@optionaro.gpzp2ko.mongodb.net/")

# db = client["option_Aro"]
lastquoteoptiongreekschain_realtime_db = db["lastquoteoptiongreekschain_realtime_db"]
lastquoteoptiongreekschain_historic_db = db["lastquoteoptiongreekschain_historic_db"]
#
# last_quote_Array_realtime_db = db["last_quote_Array_realtime_db"]
# last_quote_Array_historic_db = db["last_quote_Array_historic_db"]
#
# lastquoteoptiongreeks_realtime_db = db["lastquoteoptiongreeks_realtime_db"]
# lastquoteoptiongreeks_historic_db = db["lastquoteoptiongreeks_historic_db"]

endpoint = "ws://nimblewebstream.lisuns.com:4575"
port = "4575"
api_key = "40e5c1ea-15a5-495f-9cd5-79b4ab1fa347"
auth_message = {
    "function": "Authenticate",
    "apikey": api_key
}



con = gw.ws.connect(endpoint, api_key)
# # To store data from API
def lastquoteoptiongreekschain_store():
    while True:
        response = gw.lastquoteoptiongreekschain.get(con, 'NFO', 'NIFTY')
        response_str = json.loads(response)
        if response_str['Result']:
            for item in response_str['Result']:
                # Check if the data entry already exists

                print(item['InstrumentIdentifier'])
                existing_entry = lastquoteoptiongreekschain_realtime_db.find_one(
                    {'InstrumentIdentifier': item['InstrumentIdentifier']})

                if existing_entry:
                    current_time = datetime.now()
                    # Update existing entry with new data
                    item.update(
                        {
                            'updated_at': current_time
                        }
                    )
                    lastquoteoptiongreekschain_historic_db.insert_one(item)
                    lastquoteoptiongreekschain_realtime_db.update_one(
                        {'InstrumentIdentifier': item['InstrumentIdentifier']}, {'$set': item})
                    print("Existing data updated")
                    continue

                else:
                    current_time = datetime.now()
                    item.update(
                        {
                            'created_at': current_time,
                            'updated_at': current_time
                        }
                    )
                    lastquoteoptiongreekschain_historic_db.insert_one(item)
                    lastquoteoptiongreekschain_realtime_db.insert_one(item)

            print("New data added")

        print("Waiting for 5 seconds")
        time.sleep(5)
        print("Wait over")


def GetLastQuoteArray_store():
    last_quote_Array = gw.lastquotearray.get(con, 'NFO', '[{"Value":"NIFTY-I"}, {"Value":"BANKNIFTY-I"}]', 'false')
    last_quote_Array_response_str = json.loads(last_quote_Array)

    if last_quote_Array_response_str['Result']:
        for item in last_quote_Array_response_str['Result']:
            existing_entry = lastquoteoptiongreekschain_realtime_db.find_one(
                {'InstrumentIdentifier': item['InstrumentIdentifier']})
            data_id = existing_entry['_id']

            if existing_entry:
                current_time = datetime.now()
                # Update existing entry with new data
                item.update(
                    {
                        'updated_at': current_time
                    }
                )
                lastquoteoptiongreekschain_historic_db.insert_one(item)
                lastquoteoptiongreekschain_realtime_db.update_one(
                    {
                        'InstrumentIdentifier': item['InstrumentIdentifier'],
                        "_id": ObjectId(data_id)
                    },
                    {
                        '$set': item
                    }
                )
                print("Existing data updated")
                continue

            else:
                current_time = datetime.now()
                item.update(
                    {
                        'created_at': current_time,
                        'updated_at': current_time
                    }
                )
                lastquoteoptiongreekschain_historic_db.insert_one(item)
                lastquoteoptiongreekschain_realtime_db.insert_one(item)

        print("New data added")

    print("Waiting for 5 seconds")
    time.sleep(5)
    print("Wait over")


def lastquoteoptiongreeks_store():
    lastquoteoptiongreeks = gw.lastquoteoptiongreeks.get(con, 'NFO', api_key)
    lastquoteoptiongreeks_response_str = json.loads(lastquoteoptiongreeks)

    if lastquoteoptiongreeks_response_str:
        print(lastquoteoptiongreeks_response_str)
        # Check if the data entry already exists
        existing_entry = lastquoteoptiongreeks_realtime_db.find_one(
            {'Exchange': lastquoteoptiongreeks_response_str['Exchange']})

        if existing_entry:
            data_id = existing_entry['_id']
            current_time = datetime.now()
            # Update existing entry with new data
            lastquoteoptiongreeks_response_str.update(
                {
                    'updated_at': current_time
                }
            )
            lastquoteoptiongreeks_historic_db.insert_one(lastquoteoptiongreeks_response_str)
            lastquoteoptiongreeks_realtime_db.update_one(
                {"_id": ObjectId(data_id),
                 'Exchange': lastquoteoptiongreeks_response_str['Exchange']
                 },
                {
                    '$set': {
                        "Token": lastquoteoptiongreeks_response_str['Token'],
                        'Timestamp': lastquoteoptiongreeks_response_str['Timestamp'],
                        'IV': lastquoteoptiongreeks_response_str['IV'],
                        'Delta': lastquoteoptiongreeks_response_str['Delta'],
                        'Theta': lastquoteoptiongreeks_response_str['Theta'],
                        'Vega': lastquoteoptiongreeks_response_str['Vega'],
                        'Gamma': lastquoteoptiongreeks_response_str['Gamma'],
                        'IVVwap': lastquoteoptiongreeks_response_str['IVVwap'],
                        'Vanna': lastquoteoptiongreeks_response_str['Vanna'],
                        'Charm': lastquoteoptiongreeks_response_str['Charm'],
                        'Speed': lastquoteoptiongreeks_response_str['Speed'],
                        'Zomma': lastquoteoptiongreeks_response_str['Zomma'],
                        'Color': lastquoteoptiongreeks_response_str['Color'],
                        'Volga': lastquoteoptiongreeks_response_str['Volga'],
                        'Veta': lastquoteoptiongreeks_response_str['Veta'],
                        'ThetaGammaRatio': lastquoteoptiongreeks_response_str['ThetaGammaRatio'],
                        'ThetaVegaRatio': lastquoteoptiongreeks_response_str['ThetaVegaRatio'],
                        'DTR': lastquoteoptiongreeks_response_str['DTR'],
                        'MessageType': lastquoteoptiongreeks_response_str['MessageType'],


                    }
                }
            )
            print("Existing data updated")

        else:
            current_time = datetime.now()
            lastquoteoptiongreeks_response_str.update(
                {
                    'created_at': current_time,
                    'updated_at': current_time
                }
            )
            lastquoteoptiongreeks_historic_db.insert_one(lastquoteoptiongreeks_response_str)
            lastquoteoptiongreeks_realtime_db.insert_one(lastquoteoptiongreeks_response_str)

        print("New data added")

    print("Waiting for 5 seconds")
    time.sleep(5)
    print("Wait over")



lastquoteoptiongreekschain_store()