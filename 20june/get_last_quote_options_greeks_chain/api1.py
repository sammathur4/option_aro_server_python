from import_files import *


"""
Strike price : 19500 
OPTIDX_NIFTY_06JUL2023_CE_19500

AT the money check
CALL: lastquoteoptiongreekschain will give us LTP, IV, find strike by using the last quote option
PUT: lastquoteoptiongreekschain will give us LTP, IV, find strike by using the last quote option

Every index--- 5sec
every stock -- 30 sec
"""
def lastquoteoptiongreekschain_store():
    while True:
        response = gw.lastquoteoptiongreekschain.get(con, 'NFO', 'NIFTY')
        response_str = json.loads(response)
        if response_str['Result']:
            for item in response_str['Result']:
                print(item)
                # Check if the data entry already exists

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



lastquoteoptiongreekschain_store()
