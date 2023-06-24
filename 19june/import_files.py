import json
from flask import Flask, jsonify
import time

import json
import os
import asyncio
import time
from datetime import datetime
import gfdlws as gw
from server_details import *
from bson import ObjectId
import sys

endpoint, port, auth_message, api_key = details()

con = gw.ws.connect(endpoint, api_key)



