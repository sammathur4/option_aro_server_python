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
from makingconnection import *
endpoint, port, auth_message, api_key = details()

con = connect(endpoint, api_key)

import json
from flask import Flask, jsonify

app = Flask(__name__)



