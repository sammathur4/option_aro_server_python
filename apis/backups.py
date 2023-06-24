# def lastquoteoptiongreekschain_store():
#     while True:
#         response = gw.lastquoteoptiongreekschain.get(con, 'NFO', 'NIFTY')
#         response_str = json.loads(response)
#         if response_str['Result']:
#             for item in response_str['Result']:
#                 # Check if the data entry already exists
#
#                 print(item['InstrumentIdentifier'])
#                 with open(lastquoteoptiongreekschain_realtime_file, 'a+') as file:
#                     existing_data = json.load(file)
#                     existing_entry = next(
#                         (entry for entry in existing_data if entry['InstrumentIdentifier'] == item['InstrumentIdentifier']),
#                         None)
#
#                     if existing_entry:
#                         current_time = str(datetime.now())
#                         # Update existing entry with new data
#                         item.update(
#                             {
#                                 'updated_at': current_time
#                             }
#                         )
#                         with open(lastquoteoptiongreekschain_historic_file, 'a') as historic_file:
#                             json.dump(item, historic_file)
#                             historic_file.write('\n')
#
#                         existing_entry.update(item)
#                         file.seek(0)
#                         json.dump(existing_data, file, indent=4)
#                         file.truncate()
#                         print("Existing data updated")
#                         continue
#
#                     else:
#                         current_time = str(datetime.now())
#                         item.update(
#                             {
#                                 'created_at': current_time,
#                                 'updated_at': current_time
#                             }
#                         )
#                         with open(lastquoteoptiongreekschain_historic_file, 'a') as historic_file:
#                             json.dump(item, historic_file)
#                             historic_file.write('\n')
#
#                         existing_data.append(item)
#                         file.seek(0)
#                         json.dump(existing_data, file, indent=4)
#                         file.truncate()
#
#                 print("New data added")
#
#         print("Waiting for 5 seconds")
#         time.sleep(5)
#         print("Wait over")


"""
def load_json(file_path):
    try:
        if os.path.exists(file_path) and os.stat(file_path).st_size > 0:
            with open(file_path, 'r') as file:
                data = json.load(file)
            return data
        else:
            return []
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def lastquoteoptiongreekschain_store():
    while True:
        response = gw.lastquoteoptiongreekschain.get(con, 'NFO', 'NIFTY')
        response_str = json.loads(response)
        if response_str['Result']:
            for item in response_str['Result']:
                # Check if the data entry already exists
                print(item['InstrumentIdentifier'])
                existing_data = load_json(lastquoteoptiongreekschain_realtime_file)
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
                    with open(lastquoteoptiongreekschain_historic_file, 'a') as historic_file:
                        json.dump(item, historic_file)
                        historic_file.write('\n')

                    existing_entry.update(item)
                    save_json(existing_data, lastquoteoptiongreekschain_realtime_file)
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
                    with open(lastquoteoptiongreekschain_historic_file, 'a') as historic_file:
                        json.dump(item, historic_file)
                        historic_file.write('\n')

                    existing_data.append(item)
                    save_json(existing_data, lastquoteoptiongreekschain_realtime_file)

                print("New data added")

        print("Waiting for 5 seconds")
        time.sleep(5)
        print("Wait over")

def load_historic_data(file_path):
    try:
        if os.path.exists(file_path) and os.stat(file_path).st_size > 0:
            with open(file_path, 'r') as file:
                data = file.readlines()
            historic_data = [json.loads(line) for line in data]
            return historic_data
        else:
            return []
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def GetLastQuoteArray_store():
    last_quote_Array = gw.lastquotearray.get(con, 'NFO', '[{"Value":"NIFTY-I"}, {"Value":"BANKNIFTY-I"}]', 'false')
    last_quote_Array_response_str = json.loads(last_quote_Array)

    if last_quote_Array_response_str['Result']:
        for item in last_quote_Array_response_str['Result']:
            with open(lastquoteoptiongreekschain_realtime_file, 'r+') as file:
                existing_data = json.load(file)
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
                    with open(lastquoteoptiongreekschain_historic_file, 'a') as historic_file:
                        json.dump(item, historic_file)
                        historic_file.write('\n')

                    existing_entry.update(item)
                    file.seek(0)
                    json.dump(existing_data, file, indent=4)
                    file.truncate()
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
                    with open(lastquoteoptiongreekschain_historic_file, 'a') as historic_file:
                        json.dump(item, historic_file)
                        historic_file.write('\n')

                    existing_data.append(item)
                    file.seek(0)
                    json.dump(existing_data, file, indent=4)
                    file.truncate()

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
            existing_data = json.load(file)
            existing_entry = next(
                (entry for entry in existing_data if entry['Exchange'] == lastquoteoptiongreeks_response_str['Exchange']),
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
                    json.dump(lastquoteoptiongreeks_response_str, historic_file)
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
                    json.dump(lastquoteoptiongreeks_response_str, historic_file)
                    historic_file.write('\n')

                existing_data.append(lastquoteoptiongreeks_response_str)
                file.seek(0)
                json.dump(existing_data, file, indent=4)
                file.truncate()

        print("New data added")

    print("Waiting for 5 seconds")
    time.sleep(5)
    print("Wait over")


"""

#####################
#
#
# # # To store data from API
# def lastquoteoptiongreekschain_store():
#     while True:
#         response = gw.lastquoteoptiongreekschain.get(con, 'NFO', 'NIFTY')
#         response_str = json.loads(response)
#         if response_str['Result']:
#             for item in response_str['Result']:
#                 # Check if the data entry already exists
#
#                 print(item['InstrumentIdentifier'])
#                 existing_entry = lastquoteoptiongreekschain_realtime_db.find_one(
#                     {'InstrumentIdentifier': item['InstrumentIdentifier']})
#
#                 if existing_entry:
#                     current_time = datetime.now()
#                     # Update existing entry with new data
#                     item.update(
#                         {
#                             'updated_at': current_time
#                         }
#                     )
#                     lastquoteoptiongreekschain_historic_db.insert_one(item)
#                     lastquoteoptiongreekschain_realtime_db.update_one(
#                         {'InstrumentIdentifier': item['InstrumentIdentifier']}, {'$set': item})
#                     print("Existing data updated")
#                     continue
#
#                 else:
#                     current_time = datetime.now()
#                     item.update(
#                         {
#                             'created_at': current_time,
#                             'updated_at': current_time
#                         }
#                     )
#                     lastquoteoptiongreekschain_historic_db.insert_one(item)
#                     lastquoteoptiongreekschain_realtime_db.insert_one(item)
#
#             print("New data added")
#
#         print("Waiting for 5 seconds")
#         time.sleep(5)
#         print("Wait over")
#
#
# def GetLastQuoteArray_store():
#     last_quote_Array = gw.lastquotearray.get(con, 'NFO', '[{"Value":"NIFTY-I"}, {"Value":"BANKNIFTY-I"}]', 'false')
#     last_quote_Array_response_str = json.loads(last_quote_Array)
#
#     if last_quote_Array_response_str['Result']:
#         for item in last_quote_Array_response_str['Result']:
#             existing_entry = lastquoteoptiongreekschain_realtime_db.find_one(
#                 {'InstrumentIdentifier': item['InstrumentIdentifier']})
#             data_id = existing_entry['_id']
#
#             if existing_entry:
#                 current_time = datetime.now()
#                 # Update existing entry with new data
#                 item.update(
#                     {
#                         'updated_at': current_time
#                     }
#                 )
#                 lastquoteoptiongreekschain_historic_db.insert_one(item)
#                 lastquoteoptiongreekschain_realtime_db.update_one(
#                     {
#                         'InstrumentIdentifier': item['InstrumentIdentifier'],
#                         "_id": ObjectId(data_id)
#                     },
#                     {
#                         '$set': item
#                     }
#                 )
#                 print("Existing data updated")
#                 continue
#
#             else:
#                 current_time = datetime.now()
#                 item.update(
#                     {
#                         'created_at': current_time,
#                         'updated_at': current_time
#                     }
#                 )
#                 lastquoteoptiongreekschain_historic_db.insert_one(item)
#                 lastquoteoptiongreekschain_realtime_db.insert_one(item)
#
#         print("New data added")
#
#     print("Waiting for 5 seconds")
#     time.sleep(5)
#     print("Wait over")
#
#
# def lastquoteoptiongreeks_store():
#     lastquoteoptiongreeks = gw.lastquoteoptiongreeks.get(con, 'NFO', api_key)
#     lastquoteoptiongreeks_response_str = json.loads(lastquoteoptiongreeks)
#
#     if lastquoteoptiongreeks_response_str:
#         print(lastquoteoptiongreeks_response_str)
#         # Check if the data entry already exists
#         existing_entry = lastquoteoptiongreeks_realtime_db.find_one(
#             {'Exchange': lastquoteoptiongreeks_response_str['Exchange']})
#
#         if existing_entry:
#             data_id = existing_entry['_id']
#             current_time = datetime.now()
#             # Update existing entry with new data
#             lastquoteoptiongreeks_response_str.update(
#                 {
#                     'updated_at': current_time
#                 }
#             )
#             lastquoteoptiongreeks_historic_db.insert_one(lastquoteoptiongreeks_response_str)
#             lastquoteoptiongreeks_realtime_db.update_one(
#                 {"_id": ObjectId(data_id),
#                  'Exchange': lastquoteoptiongreeks_response_str['Exchange']
#                  },
#                 {
#                     '$set': {
#                         "Token": lastquoteoptiongreeks_response_str['Token'],
#                         'Timestamp': lastquoteoptiongreeks_response_str['Timestamp'],
#                         'IV': lastquoteoptiongreeks_response_str['IV'],
#                         'Delta': lastquoteoptiongreeks_response_str['Delta'],
#                         'Theta': lastquoteoptiongreeks_response_str['Theta'],
#                         'Vega': lastquoteoptiongreeks_response_str['Vega'],
#                         'Gamma': lastquoteoptiongreeks_response_str['Gamma'],
#                         'IVVwap': lastquoteoptiongreeks_response_str['IVVwap'],
#                         'Vanna': lastquoteoptiongreeks_response_str['Vanna'],
#                         'Charm': lastquoteoptiongreeks_response_str['Charm'],
#                         'Speed': lastquoteoptiongreeks_response_str['Speed'],
#                         'Zomma': lastquoteoptiongreeks_response_str['Zomma'],
#                         'Color': lastquoteoptiongreeks_response_str['Color'],
#                         'Volga': lastquoteoptiongreeks_response_str['Volga'],
#                         'Veta': lastquoteoptiongreeks_response_str['Veta'],
#                         'ThetaGammaRatio': lastquoteoptiongreeks_response_str['ThetaGammaRatio'],
#                         'ThetaVegaRatio': lastquoteoptiongreeks_response_str['ThetaVegaRatio'],
#                         'DTR': lastquoteoptiongreeks_response_str['DTR'],
#                         'MessageType': lastquoteoptiongreeks_response_str['MessageType'],
#
#
#                     }
#                 }
#             )
#             print("Existing data updated")
#
#         else:
#             current_time = datetime.now()
#             lastquoteoptiongreeks_response_str.update(
#                 {
#                     'created_at': current_time,
#                     'updated_at': current_time
#                 }
#             )
#             lastquoteoptiongreeks_historic_db.insert_one(lastquoteoptiongreeks_response_str)
#             lastquoteoptiongreeks_realtime_db.insert_one(lastquoteoptiongreeks_response_str)
#
#         print("New data added")
#
#     print("Waiting for 5 seconds")
#     time.sleep(5)
#     print("Wait over")
