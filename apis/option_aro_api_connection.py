import json
import os
import asyncio
import time
from datetime import datetime
import gfdlws as gw
from server_api_details import *
from bson import ObjectId
import threading



"""
Save only this in database
get last option greek chain historic data
"""
endpoint, port, auth_message, api_key = details()

con = gw.ws.connect(endpoint, api_key)

lastquoteoptiongreekschain_historic_file = "lastquoteoptiongreekschain_historic.json"
lastquoteoptiongreekschain_realtime_file = "lastquoteoptiongreekschain_realtime.json"

lastquoteoptiongreeks_historic_file = "lastquoteoptiongreeks_historic.json"
lastquoteoptiongreeks_realtime_file = "lastquoteoptiongreeks_realtime.json"

GetLastQuoteArray_historic_file = "GetLastQuoteArray_historic_file.json"
GetLastQuoteArray_realtime_file = "GetLastQuoteArray_realtime_file.json"


def load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
    return data


def save_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


# def lastquoteoptiongreekschain_store():
#     while True:
#         response = gw.lastquoteoptiongreekschain.get(con, 'NFO', 'NIFTY')
#         response_str = json.loads(response)
#         if response_str['Result']:
#             for item in response_str['Result']:
#                 # Check if the data entry already exists
#                 print(item['InstrumentIdentifier'])
#                 existing_data = load_json(lastquoteoptiongreekschain_realtime_file)
#                 existing_entry = next(
#                     (entry for entry in existing_data if entry['InstrumentIdentifier'] == item['InstrumentIdentifier']),
#                     None)
#
#                 if existing_entry:
#                     current_time = str(datetime.now())
#                     # Update existing entry with new data
#                     item.update(
#                         {
#                             'updated_at': current_time
#                         }
#                     )
#                     with open(lastquoteoptiongreekschain_historic_file, 'a') as historic_file:
#                         json.dump(item, historic_file, indent=4)
#                         historic_file.write('\n')
#
#                     existing_entry.update(item)
#                     save_json(existing_data, lastquoteoptiongreekschain_realtime_file)
#                     print("Existing data updated")
#                     continue
#
#                 else:
#                     current_time = str(datetime.now())
#                     item.update(
#                         {
#                             'created_at': current_time,
#                             'updated_at': current_time
#                         }
#                     )
#                     with open(lastquoteoptiongreekschain_historic_file, 'a') as historic_file:
#                         json.dump(item, historic_file, indent=4)
#                         historic_file.write('\n')
#
#                     existing_data.append(item)
#                     save_json(existing_data, lastquoteoptiongreekschain_realtime_file)
#
#                 print("New data added")
#
#         print("Waiting for 5 seconds")
#         time.sleep(5)
#         print("Wait over")


def lastquoteoptiongreekschain_store():
    while True:
        response = gw.lastquoteoptiongreekschain.get(con, 'NFO', 'NIFTY')
        response_str = json.loads(response)
        if response_str['Result']:
            for item in response_str['Result']:
                # Check if the data entry already exists
                print(item['InstrumentIdentifier'])
                existing_data = load_json(lastquoteoptiongreekschain_realtime_file)
                existing_entry = existing_data.get(item['InstrumentIdentifier'])

                if existing_entry:
                    current_time = str(datetime.now())
                    # Update existing entry with new data
                    item.update(
                        {
                            'updated_at': current_time
                        }
                    )
                    existing_data[item['InstrumentIdentifier']].update(item)

                    with open(lastquoteoptiongreekschain_historic_file, 'a+') as historic_file:
                        json.dump(item, historic_file, indent=4)
                        historic_file.write('\n')

                    save_json(existing_data, lastquoteoptiongreekschain_realtime_file)
                    print("Existing data updated")
                else:
                    current_time = str(datetime.now())
                    item.update(
                        {
                            'created_at': current_time,
                            'updated_at': current_time
                        }
                    )
                    existing_data[item['InstrumentIdentifier']] = item

                    with open(lastquoteoptiongreekschain_historic_file, 'a') as historic_file:
                        json.dump(item, historic_file, indent=4)
                        historic_file.write('\n')

                    save_json(existing_data, lastquoteoptiongreekschain_realtime_file)
                    print("New data added")

        print("Waiting for 5 seconds")
        time.sleep(5)
        print("Wait over")


def GetLastQuoteArray_store():
    last_quote_Array = gw.lastquotearray.get(con, 'NFO', '[{"Value":"NIFTY-I"}, {"Value":"BANKNIFTY-I"}]', 'false')
    last_quote_Array_response_str = json.loads(last_quote_Array)

    if last_quote_Array_response_str['Result']:
        for item in last_quote_Array_response_str['Result']:
            if os.path.isfile(GetLastQuoteArray_realtime_file):
                with open(GetLastQuoteArray_realtime_file, 'r+') as file:
                    file_content = file.read()
                    if file_content:
                        existing_data = json.loads(file_content)
                    else:
                        existing_data = []
            else:
                existing_data = []

            existing_entry = next(
                (entry for entry in existing_data if entry['InstrumentIdentifier'] == item['InstrumentIdentifier']),
                None)

            if existing_entry:
                current_time = str(datetime.now())
                # Update existing entry with new data
                item.update(
                    {
                        'updated_at': current_time
                    }
                )
                with open(GetLastQuoteArray_historic_file, 'a') as historic_file:
                    json.dump(item, historic_file, indent=4)
                    historic_file.write('\n')

                existing_entry.update(item)
                with open(GetLastQuoteArray_realtime_file, 'w') as file:
                    json.dump(existing_data, file, indent=4)
                print("Existing data updated")
                continue

            else:
                current_time = str(datetime.now())
                item.update(
                    {
                        'created_at': current_time,
                        'updated_at': current_time
                    }
                )
                with open(GetLastQuoteArray_historic_file, 'a') as historic_file:
                    json.dump(item, historic_file, indent=4)
                    historic_file.write('\n')

                existing_data.append(item)
                with open(GetLastQuoteArray_realtime_file, 'w') as file:
                    json.dump(existing_data, file, indent=4)

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
        with open(lastquoteoptiongreeks_realtime_file, 'a+') as file:
            file.seek(0)
            file_content = file.read()
            if file_content:
                existing_data = json.loads(file_content)
            else:
                existing_data = []

            existing_entry = next(
                (entry for entry in existing_data if
                 entry['Exchange'] == lastquoteoptiongreeks_response_str['Exchange']),
                None)

            if existing_entry:
                data_id = existing_entry['_id']
                current_time = str(datetime.now())
                # Update existing entry with new data
                lastquoteoptiongreeks_response_str.update(
                    {
                        'updated_at': current_time
                    }
                )
                with open(lastquoteoptiongreeks_historic_file, 'a') as historic_file:
                    json.dump(lastquoteoptiongreeks_response_str, historic_file, indent=4)
                    historic_file.write('\n')

                existing_entry.update({
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
                    'updated_at': current_time
                })
                file.seek(0)
                json.dump(existing_data, file, indent=4)
                file.truncate()
                print("Existing data updated")

            else:
                current_time = str(datetime.now())
                lastquoteoptiongreeks_response_str.update(
                    {
                        'created_at': current_time,
                        'updated_at': current_time
                    }
                )
                with open(lastquoteoptiongreeks_historic_file, 'a') as historic_file:
                    json.dump(lastquoteoptiongreeks_response_str, historic_file, indent=4)
                    historic_file.write('\n')

                existing_data.append(lastquoteoptiongreeks_response_str)
                file.seek(0)
                json.dump(existing_data, file, indent=4)
                file.truncate()

        print("New data added")

    print("Waiting for 5 seconds")
    time.sleep(5)
    print("Wait over")


# Create threads for each function
thread1 = threading.Thread(target=lastquoteoptiongreekschain_store())
thread2 = threading.Thread(target=GetLastQuoteArray_store())
thread3 = threading.Thread(target=lastquoteoptiongreeks_store())

# Start the threads
thread1.start()
thread2.start()
thread3.start()

# Wait for all threads to finish
thread1.join()
thread2.join()
thread3.join()

# All functions have completed
print("All functions have finished executing.")
# lastquoteoptiongreekschain_store()
# GetLastQuoteArray_store()
# lastquoteoptiongreeks_store()
