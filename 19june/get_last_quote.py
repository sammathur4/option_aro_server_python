"""

import asyncio
import websockets


exg = None
sym = None
msg = None
isi = None


def get(ws, exchange, symbols,isShortIdentifiers):
    exg = exchange
    sym = symbols
    isi = isShortIdentifiers
    asyncio.get_event_loop().run_until_complete(mass_subscribe_n_stream(ws, exg, sym, isi))
    return


async def mass_subscribe_n_stream(ws, exg, sym, isi):
    try:
        req_msg = str('{"MessageType":"GetLastQuoteArray","Exchange":"' + exg + '","isShortIdentifiers":"' + isi + '","InstrumentIdentifiers":' + str(sym) + '}')
        await ws.send(req_msg)
        print("Request : " + req_msg)
        await get_msg(ws)
    except:
        return msg


async def get_msg(ws):
    while True:
        try:
            message = await ws.recv()
        except websockets.ConnectionClosedOK:
            break
        print(message)


"""

from import_files import *
import asyncio
import json

import websockets

exg = None
sym = None
msg = None
isi = None


def get(ws, exchange, symbols, isShortIdentifiers):
    exg = exchange
    sym = symbols
    isi = isShortIdentifiers
    asyncio.get_event_loop().run_until_complete(mass_subscribe_n_stream(ws, exg, sym, isi))
    return


async def mass_subscribe_n_stream(ws, exg, sym, isi):
    try:
        req_msg = str(
            '{"MessageType":"GetLastQuoteArray","Exchange":"' + exg + '","isShortIdentifiers":"' + isi + '","InstrumentIdentifiers":' + str(
                sym) + '}')
        await ws.send(req_msg)
        print("Request : " + req_msg)
        await get_msg(ws)
    except:
        return msg


async def get_msg(ws):
    while True:
        try:
            message = await ws.recv()
        except websockets.ConnectionClosedOK:
            break

        save_data_to_json(message)


def save_data_to_json(data):
    # Parse the JSON string
    json_data = json.loads(data)

    # Check if the "Result" key is present and its value is a list of dictionaries
    if "Result" in json_data and isinstance(json_data["Result"], list):
        print("Yes")
        result = json_data["Result"]

        # Write the "Result" value to a JSON file
        with open('get_last_quote.json', 'a+') as file:
            json.dump(result, file, indent=4)


get(con, 'NFO', '[{"Value":"NIFTY-I"}, {"Value":"BANKNIFTY-I"}]', 'false')
