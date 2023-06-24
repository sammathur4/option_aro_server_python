import json
from flask import Flask, jsonify
import time

import json
import os
import asyncio
from datetime import datetime
import gfdlws as gw
from server_details import *
from bson import ObjectId
import sys
import pymongo
import websockets
import uuid

# client = pymongo.MongoClient('mongodb://localhost:27017')
client = pymongo.MongoClient('mongodb+srv://sammathur4:wo7kdLODmeaFG7wL@optionaro.gpzp2ko.mongodb.net/')
db = client['OPTIONARO']
lastquoteoptiongreeks_realtime_db = db["last_quote_option_greeks_realtime"]
lastquoteoptiongreeks_historic_db = db["last_quote_option_greeks_historic"]
msg = None

endpoint, port, auth_message, api_key = details()

con = gw.ws.connect(endpoint, api_key)



