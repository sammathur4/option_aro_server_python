

from  import_files import *


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


instrumentidentifier5 = [{"Value": "MGL-I"}, {"Value": "MPHASIS-I"}, {"Value": "MUTHOOTFIN-I"}, {"Value": "NAUKRI-I"},
                         {"Value": "NAVINFLUOR-I"},
                         {"Value": "NESTLEIND-I"}, {"Value": "NMDC-I"}, {"Value": "NTPC-I"}, {"Value": "OFSS-I"},
                         {"Value": "ONGC-I"},
                         {"Value": "PEL-I"}, {"Value": "PFC-I"}, {"Value": "PIDILITIND-I"}, {"Value": "PNB-I"},
                         {"Value": "POLYCAB-I"},
                         {"Value": "POWERGRID-I"}, {"Value": "RBLBANK-I"}, {"Value": "RECLTD-I"},
                         {"Value": "RELIANCE-I"}, {"Value": "SAIL-I"},
                         {"Value": "SBILIFE-I"}, {"Value": "SBIN-I"}, {"Value": "SRF-I"}, {"Value": "SUNPHARMA-I"},
                         {"Value": "SYNGENE-I"}]

while True:
    get(con, 'NFO', str(instrumentidentifier5), 'false')
