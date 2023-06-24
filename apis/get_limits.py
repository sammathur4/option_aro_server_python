import json

import gfdlws as gw

from server_api_details import *

client, db, realtime_db, historic_db, endpoint, port, auth_message, api_key = details()
con = gw.ws.connect(endpoint, api_key)
ans = gw.limitation.get(con)
