#
# import asyncio
# import websockets
# import os
#
# url = None
# key = None
# exg = None
# prd = None
# exp = None
# otp = None
# srp = None
#
#
# def get(ws, exchange, product, expiry=None, optiontype=None, strikeprice=None):
#     if exchange == "":
#         print("Exchange is mandatory.")
#     else:
#         exg = exchange
#
#     if product == "":
#         prd = ''
#     else:
#         prd = product
#
#     if expiry == "":
#         exp = ''
#     else:
#         exp = expiry
#
#     if optiontype == "":
#         otp = ''
#     else:
#         otp = optiontype
#
#     if strikeprice == "":
#         srp = ''
#     else:
#         srp = strikeprice
#
#     asyncio.get_event_loop().run_until_complete(
#         mass_subscribe_n_stream(ws, exg, prd, exp, otp, srp))
#     return
#
#
# async def mass_subscribe_n_stream(ws, exg, prd, exp, otp, srp):
#     try:
#         req_msg = '{"MessageType":"GetLastQuoteOptionGreeksChain","Exchange":"' + exg + '","Product":"' + prd + '"'
#         if exp is not None:
#             req_msg = req_msg + ',"Expiry":"' + exp + '"'
#         if otp is not None:
#             req_msg = req_msg + ',"optionType":"' + otp + '"'
#         if srp is not None:
#             req_msg = req_msg + ',"strikePrice":"' + srp + '"'
#
#         req_msg = str(req_msg + '}')
#         print("Request : " + req_msg)
#         await ws.send(req_msg)
#         await get_msg(ws)
#     except:
#         print('In Exception...' + str(os.error))
#         return
#
#
# async def get_msg(ws):
#     while True:
#         try:
#             message = await ws.recv()
#         except websockets.ConnectionClosedOK:
#             print('Connection closed')
#             break
#         print('something' + message)


import asyncio
import websockets
import json

url = None
key = None
exg = None
sym = None
msg = None
ws = None


def connect(endpoint, apikey):
    ws = asyncio.get_event_loop().run_until_complete(mass_subscribe_n_stream(endpoint, apikey))
    return ws


async def mass_subscribe_n_stream(endpoint, apikey):
    ws = await asyncio.wait_for(websockets.connect(endpoint, max_size=2 ** 50), timeout=60)
    stst = await authenticate(ws, apikey)  # Authenticates the connection
    if stst == 'Key Authenticated!!!':
        return ws
    else:
        print('Not connected. Trying again. Please wait...')
        stst = await authenticate(ws, apikey)


async def authenticate(ws, key):
    try:
        msg = 'Performing Authentication'
        print(msg)
        authentication_msg = json.dumps({
            "MessageType": "Authenticate",
            "Password": key
        })
        authenticated = False
        await ws.send(authentication_msg)
        while not authenticated:  # Stay in this loop until successful authentication.
            response = await ws.recv()
            response = json.loads(response)
            print(response)
            if response['MessageType'] == "AuthenticateResult":
                if response['Complete']:
                    status = 'Key Authenticated!!!'
                    return status
                else:
                    print('Not connected. Trying again. Please wait...')
                    await ws.send(authentication_msg)
    except:
        return msg
