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

client = pymongo.MongoClient('mongodb://localhost:27017')
db = client['OPTIONARO']
lastquoteoptiongreekschain_realtime_db = db["lastquoteoptiongreekschain_realtime"]
lastquoteoptiongreekschain_historic_db = db["lastquoteoptiongreekschain_historic"]

msg = None

endpoint, port, auth_message, api_key = details()

con = gw.ws.connect(endpoint, api_key)



