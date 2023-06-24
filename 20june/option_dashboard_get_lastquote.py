import uuid
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
    msgs = asyncio.get_event_loop().run_until_complete(mass_subscribe_n_stream(ws, exg, sym, isi))
    print("msgs: ", msgs)

    return msgs


async def mass_subscribe_n_stream(ws, exg, sym, isi):
    try:
        req_msg = str(
            '{"MessageType":"GetLastQuoteArray","Exchange":"' + exg + '","isShortIdentifiers":"' + isi + '","InstrumentIdentifiers":' + str(
                sym) + '}')
        await ws.send(req_msg)
        print("Sending Request For : " + req_msg)
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
        with open('store_allmesg_getlastquote.json', 'a+') as file:
            json.dump(json_data, file, indent=4)
            file.write('\n')

        if "Result" in json_data and isinstance(json_data["Result"], list):
            current_time = datetime.now().strftime("%Y %m %d %H:%M:%S")
            updated_time = datetime.now().strftime("%Y %m %d %H:%M:%S")

            for item in json_data["Result"]:
                # item["Liquidity"] = (json_data["TotalQtyTraded"] * json_data["QuotationLot"]) / json_data[
                #     "AverageTradedPrice"]
                item["current_time"] = current_time
                item["updated_time"] = updated_time
                item["id"] = str(uuid.uuid4())

            with open('get_last_quote.json', 'a+') as file:
                json.dump(json_data, file, indent=4)
                file.write('\n')


instrumentidentifier0 = [
    {"Value": "ACC-I"}, {"Value": "ADANIENT-I"}, {"Value": "ADANIPORTS-I"},
    {"Value": "AMBUJACEM-I"}, {"Value": "APOLLOHOSP-I"},
    {"Value": "ASHOKLEY-I"}, {"Value": "ASIANPAINT-I"}, {"Value": "ASTRAL-I"},
    {"Value": "AUBANK-I"}, {"Value": "AUROPHARMA-I"},
    {"Value": "ASHOKLEY-I"}, {"Value": "BAJAJ-AUTO-I"}, {"Value": "BAJAJFINSV-I"},
    {"Value": "BAJFINANCE-I"}, {
        "Value": "BANDHANBNK-I"},
    {"Value": "BANKBARODA-I"}, {"Value": "BATAINDIA-I"}, {"Value": "BEL-I"},
    {"Value": "BERGEPAINT-I"}, {"Value": "BHARATFORG-I"},
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
    {"Value": "FEDERALBNK-I"},
    {"Value": "GAIL-I"},
    {"Value": "GODREJCP-I"},
    {"Value": "GODREJPROP-I"},
    {"Value": "GRASIM-I"},
    {"Value": "GUJGASLTD-I"},
    {"Value": "HAL-I"},
    {"Value": "HAVELLS-I"},
    {"Value": "HCLTECH-I"},
    {"Value": "HDFC-I"},
    {"Value": "HDFCAMC-I"},
    {"Value": "HDFCBANK-I"},
    {"Value": "HDFCLIFE-I"},
    {"Value": "HEROMOTOCO-I"},
    {"Value": "HINDALCO-I"},
    {"Value": "HINDPETRO-I"},
    {"Value": "HINDUNILVR-I"}, {"Value": "ICICIBANK-I"}, {"Value": "ICICIGI-I"}, {"Value": "ICICIPRULI-I"},
    {"Value": "IDEA-I"},
    {"Value": "IDFCFIRSTB-I"}, {"Value": "IEX-I"}, {"Value": "IGL-I"}, {"Value": "INDHOTEL-I"},
    {"Value": "INDIAMART-I"},
    {"Value": "IPCALAB-I"}, {"Value": "IRCTC-I"}, {"Value": "ITC-I"}, {"Value": "JINDALSTEL-I"},
    {"Value": "JSWSTEEL-I"},
    {"Value": "JUBLFOOD-I"}, {"Value": "KOTAKBANK-I"}, {"Value": "LALPATHLAB-I"},
    {"Value": "LICHSGFIN-I"}, {"Value": "LT-I"},
    {"Value": "LTTS-I"}, {"Value": "LUPIN-I"}, {"Value": "M&M-I"}, {"Value": "M&MFIN-I"},
    {"Value": "MANAPPURAM-I"},
    {"Value": "MARICO-I"}, {"Value": "MARUTI-I"}, {"Value": "MCDOWELL-N-I"},
    {"Value": "METROPOLIS-I"}, {"Value": "MFSL-I"},
    {"Value": "MGL-I"}, {"Value": "MPHASIS-I"}, {"Value": "MUTHOOTFIN-I"}, {"Value": "NAUKRI-I"},
    {"Value": "NAVINFLUOR-I"},
    {"Value": "NESTLEIND-I"}, {"Value": "NMDC-I"}, {"Value": "NTPC-I"}, {"Value": "OFSS-I"},
    {"Value": "ONGC-I"},
    {"Value": "PEL-I"}, {"Value": "PFC-I"}, {"Value": "PIDILITIND-I"}, {"Value": "PNB-I"},
    {"Value": "POLYCAB-I"},
    {"Value": "POWERGRID-I"}, {"Value": "RBLBANK-I"}, {"Value": "RECLTD-I"},
    {"Value": "RELIANCE-I"}, {"Value": "SAIL-I"},
    {"Value": "SBILIFE-I"}, {"Value": "SBIN-I"}, {"Value": "SRF-I"}, {"Value": "SUNPHARMA-I"},
    {"Value": "SYNGENE-I"}
]

instrumentidentifier1 = [
    {"Value": "ACC-I"}, {"Value": "ADANIENT-I"}, {"Value": "ADANIPORTS-I"}, {"Value": "AMBUJACEM-I"},
    {"Value": "APOLLOHOSP-I"},
    {"Value": "ASHOKLEY-I"}, {"Value": "ASIANPAINT-I"}, {"Value": "ASTRAL-I"}, {"Value": "AUBANK-I"},
    {"Value": "AUROPHARMA-I"},
    {"Value": "ASHOKLEY-I"}, {"Value": "BAJAJ-AUTO-I"}, {"Value": "BAJAJFINSV-I"}, {"Value": "BAJFINANCE-I"}, {
        "Value": "BANDHANBNK-I"},
    {"Value": "BANKBARODA-I"}, {"Value": "BATAINDIA-I"}, {"Value": "BEL-I"}, {"Value": "BERGEPAINT-I"},
    {"Value": "BHARATFORG-I"}]

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

instrumentidentifier3 = [
    {"Value": "GAIL-I"},
    {"Value": "GODREJCP-I"},
    {"Value": "GODREJPROP-I"},
    {"Value": "GRASIM-I"},
    {"Value": "GUJGASLTD-I"},
    {"Value": "HAL-I"},
    {"Value": "HAVELLS-I"},
    {"Value": "HCLTECH-I"},
    {"Value": "HDFC-I"},
    {"Value": "HDFCAMC-I"},
    {"Value": "HDFCBANK-I"},
    {"Value": "HDFCLIFE-I"},
    {"Value": "HEROMOTOCO-I"},
    {"Value": "HINDALCO-I"},
    {"Value": "HINDPETRO-I"},
    {"Value": "HINDUNILVR-I"}, {"Value": "ICICIBANK-I"}, {"Value": "ICICIGI-I"}, {"Value": "ICICIPRULI-I"},
    {"Value": "IDEA-I"},
    {"Value": "IDFCFIRSTB-I"}, {"Value": "IEX-I"}, {"Value": "IGL-I"}, {"Value": "INDHOTEL-I"},
    {"Value": "INDIAMART-I"}]

instrumentidentifier4 = [{"Value": "IPCALAB-I"}, {"Value": "IRCTC-I"}, {"Value": "ITC-I"}, {"Value": "JINDALSTEL-I"},
                         {"Value": "JSWSTEEL-I"},
                         {"Value": "JUBLFOOD-I"}, {"Value": "KOTAKBANK-I"}, {"Value": "LALPATHLAB-I"},
                         {"Value": "LICHSGFIN-I"}, {"Value": "LT-I"},
                         {"Value": "LTTS-I"}, {"Value": "LUPIN-I"}, {"Value": "M&M-I"}, {"Value": "M&MFIN-I"},
                         {"Value": "MANAPPURAM-I"},
                         {"Value": "MARICO-I"}, {"Value": "MARUTI-I"}, {"Value": "MCDOWELL-N-I"},
                         {"Value": "METROPOLIS-I"}, {"Value": "MFSL-I"}]

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

# while True:
#     get(con, 'NFO', str(instrumentidentifier1), 'false')
#     get(con, 'NFO', str(instrumentidentifier2), 'false')
#     get(con, 'NFO', str(instrumentidentifier3), 'false')
#     get(con, 'NFO', str(instrumentidentifier4), 'false')
#     get(con, 'NFO', str(instrumentidentifier5), 'false')

