
def details():
    # client = pymongo.MongoClient("mongodb://localhost:27017")
    # client = pymongo.MongoClient("mongodb+srv://sammathur4:wo7kdLODmeaFG7wL@optionaro.gpzp2ko.mongodb.net/")
    #
    # db = client["option_Aro"]
    # lastquoteoptiongreekschain_realtime_db = db["lastquoteoptiongreekschain_realtime_db"]
    # lastquoteoptiongreekschain_historic_db = db["lastquoteoptiongreekschain_historic_db"]
    #
    # last_quote_Array_realtime_db = db["last_quote_Array_realtime_db"]
    # last_quote_Array_historic_db = db["last_quote_Array_historic_db"]
    #
    # lastquoteoptiongreeks_realtime__db = db["lastquoteoptiongreeks_realtime_db"]
    # lastquoteoptiongreeks_historic_db = db["lastquoteoptiongreeks_historic_db"]

    endpoint = "ws://nimblewebstream.lisuns.com:4575"
    port = "4575"
    api_key = "40e5c1ea-15a5-495f-9cd5-79b4ab1fa347"
    auth_message = {
        "function": "Authenticate",
        "apikey": api_key
    }

    # return client, db, lastquoteoptiongreekschain_realtime_db, lastquoteoptiongreekschain_historic_db, \
    #     last_quote_Array_realtime_db, last_quote_Array_historic_db, \
    #     lastquoteoptiongreeks_realtime__db, lastquoteoptiongreeks_historic_db, \
    #     endpoint, port, auth_message, api_key

    return endpoint, port, auth_message, api_key
