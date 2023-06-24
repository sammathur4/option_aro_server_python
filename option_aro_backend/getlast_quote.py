from import_files import *

"""													
{													
MessageType: "GetLastQuoteArray",													
Exchange: "NFO",													
isShortIdentifiers: "false",													
InstrumentIdentifiers: [
    {Value:"NIFTY-I"}, 
    {Value:"BANKNIFTY-I"}, 
    {Value:"MIDCAPNIFTY-I"}, 
    {Value:"FINNIFTY-I"}, 
    {Value:"AARTIIND-I"},													
    {Value:"ACC-I"}, 
    {Value:"ADANIENT-I"}, 
    {Value:"ADANIPORTS-I"}, 
    {Value:"AMBUJACEM-I"}, 
    {Value:"APOLLOHOSP-I"},										
    {Value:"ASHOKLEY-I"}, 
    {Value:"ASIANPAINT-I"}, 
    {Value:"ASTRAL-I"}, 
    {Value:"AUBANK-I"}, 
    {Value:"AUROPHARMA-I"},										
    {Value:"ASHOKLEY-I"}, 
    {Value:"BAJAJ-AUTO-I"}, 
    {Value:"BAJAJFINSV-I"}, 
    {Value:"BAJFINANCE-I"}, 
    {Value:"BANDHANBNK-I"},										
    {Value:"BANKBARODA-I"}, 
    {Value:"BATAINDIA-I"}, 
    {Value:"BEL-I"}, 
    {Value:"BERGEPAINT-I"}, 
    {Value:"BHARATFORG-I"}
]										
};													
doSend(request);													


"""

GetLastQuoteArray_historic_file = "GetLastQuoteArray_historic_file.json"
GetLastQuoteArray_realtime_file = "GetLastQuoteArray_realtime_file.json"

instrument_identifier_getlastquotearray = [
    {"Value": "NIFTY-I"},
    {"Value": "BANKNIFTY-I"},
    {"Value": "MIDCAPNIFTY-I"},
    {"Value": "FINNIFTY-I"},
    {"Value": "AARTIIND-I"},
    {"Value": "ACC-I"},
    {"Value": "ADANIENT-I"},
    {"Value": "ADANIPORTS-I"},
    {"Value": "AMBUJACEM-I"},
    {"Value": "APOLLOHOSP-I"},
    {"Value": "ASHOKLEY-I"},
    {'Value': "ASIANPAINT-I"},
    {"Value": "ASTRAL-I"},
    {"Value": "AUBANK-I"},
    {"Value": "AUROPHARMA-I"},
    {"Value": "ASHOKLEY-I"},
    {"Value": "BAJAJ-AUTO-I"},
    {"Value": "BAJAJFINSV-I"},
    {"Value": "BAJFINANCE-I"},
    {"Value": "BANDHANBNK-I"},
    {"Value": "BANKBARODA-I"},
    {"Value": "BATAINDIA-I"},
    {"Value": "BEL-I"},
    {"Value": "BERGEPAINT-I"},
    {"Value": "BHARATFORG-I"}
]


# def GetLastQuoteArray_store():
#     last_quote_Array = gw.lastquotearray.get(con,
#                                              'NFO',
#                                              str(instrument_identifier_getlastquotearray),
#                                              'false'
#                                              )
#     last_quote_Array_response_str = json.loads(last_quote_Array)
#
#     if last_quote_Array_response_str['Result']:
#         for item in last_quote_Array_response_str['Result']:
#             if os.path.isfile(GetLastQuoteArray_realtime_file):
#                 with open(GetLastQuoteArray_realtime_file, 'r+') as file:
#                     file_content = file.read()
#                     if file_content:
#                         existing_data = json.loads(file_content)
#                     else:
#                         existing_data = []
#             else:
#                 existing_data = []
#
#             existing_entry = next(
#                 (entry for entry in existing_data if entry['InstrumentIdentifier'] == item['InstrumentIdentifier']),
#                 None)
#
#             if existing_entry:
#                 current_time = str(datetime.now())
#                 # Update existing entry with new data
#                 item.update(
#                     {
#                         'updated_at': current_time
#                     }
#                 )
#                 with open(GetLastQuoteArray_historic_file, 'a+') as historic_file:
#                     json.dump(item, historic_file, indent=4)
#                     historic_file.write('\n')
#
#                 existing_entry.update(item)
#                 with open(GetLastQuoteArray_realtime_file, 'w') as file:
#                     json.dump(existing_data, file, indent=4)
#                 print("Existing data updated")
#                 continue
#
#             else:
#                 current_time = str(datetime.now())
#                 item.update(
#                     {
#                         'created_at': current_time,
#                         'updated_at': current_time
#                     }
#                 )
#                 with open(GetLastQuoteArray_historic_file, 'a') as historic_file:
#                     json.dump(item, historic_file, indent=4)
#                     historic_file.write('\n')
#
#                 existing_data.append(item)
#                 with open(GetLastQuoteArray_realtime_file, 'w') as file:
#                     json.dump(existing_data, file, indent=4)
#
#             print("New data added")
#
#     print("Waiting for 5 seconds")
#     time.sleep(5)
#     print("Wait over")
#
#
# GetLastQuoteArray_store()


import json
import os


def GetLastQuoteArray_store():
    last_quote_Array = gw.lastquotearray.get(con,
                                             'NFO',
                                             str(instrument_identifier_getlastquotearray),
                                             'false'
                                             )
    last_quote_Array_response_str = json.loads(last_quote_Array)

    # Check if the file already exists
    if os.path.exists('data.json'):
        print("File already exists. Data will be appended.")
        with open('data.json', 'r') as file:
            existing_data = json.load(file)

        # Merge existing data with new data
        existing_data.extend(last_quote_Array_response_str)

        with open('data.json', 'w') as file:
            json.dump(existing_data, file, indent=4)
    else:
        with open('data.json', 'w') as file:
            json.dump(last_quote_Array_response_str, file, indent=4)

    print("Data stored successfully in data.json file.")

GetLastQuoteArray_store()