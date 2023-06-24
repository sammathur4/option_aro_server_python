from import_files import *



def get(ws, exchange, symbols, isShortIdentifiers):
    exg = exchange
    sym = symbols
    isi = isShortIdentifiers
    msgs = asyncio.get_event_loop().run_until_complete(mass_subscribe_n_stream(ws, exg, sym, isi))
    print("msgs: ", msgs)
    return msgs

async def mass_subscribe_n_stream(ws, exg, sym, isi):
    try:
        req_msg = str(
            '{"MessageType":"GetLastQuoteArray","Exchange":"' + exg + '","isShortIdentifiers":"' + isi + '","InstrumentIdentifiers":' + str(
                sym) + '}')
        await ws.send(req_msg)
        print("Sending Request For: " + req_msg)
        await get_msg(ws)
    except:
        return msg

async def get_msg(ws):
    while True:
        try:
            message = await ws.recv()
        except websockets.ConnectionClosedOK:
            break
        json_data = json.loads(message)
        print("message direct:", json_data)

        if "Result" in json_data and isinstance(json_data["Result"], list):
            current_time = datetime.now().strftime("%Y %m %d %H:%M:%S")
            updated_time = datetime.now().strftime("%Y %m %d %H:%M:%S")

            for item in json_data["Result"]:
                item["current_time"] = current_time
                item["updated_time"] = updated_time
                item["id"] = str(uuid.uuid4())

                existing_data = main_collection.find_one({"InstrumentIdentifier": item["InstrumentIdentifier"]})

                if existing_data:
                    main_collection.update_one(
                        {"InstrumentIdentifier": item["InstrumentIdentifier"]},
                        {"$set": item}
                    )
                else:
                    main_collection.insert_one(item)

                historic_collection.insert_one(item)



instrumentidentifier2 = [
    {"Value": "BHARTIARTL-I"}, {"Value": "BHEL-I"}, {"Value": "BIOCON-I"}, {"Value": "BOSCHLTD-I"},
    {"Value": "BPCL-I"},
    {"Value": "BRITANNIA-I"},
    {"Value": "CANBK-I"}, {"Value": "CANFINHOME-I"}, {"Value": "CHOLAFIN-I"},
    {"Value": "CIPLA-I"},
    {"Value": "COALINDIA-I"},
    {"Value": "COFORGE-I"}, {"Value": "COLPAL-I"}, {"Value": "CONCOR-I"},
    {"Value": "COROMANDEL-I"},
    {"Value": "CUMMINSIND-I"},
    {"Value": "DABUR-I"}, {"Value": "DEEPAKNTR-I"}, {"Value": "DIVISLAB-I"},
    {"Value": "DLF-I"},
    {"Value": "DRREDDY-I"},
    {"Value": "EICHERMOT-I"}, {"Value": "ESCORTS-I"}, {"Value": "EXIDEIND-I"},
    {"Value": "FEDERALBNK-I"}]

while True:
    get(con, 'NFO', str(instrumentidentifier2), 'false')