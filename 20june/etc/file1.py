import pandas as pd
import pandas_datareader.data as web
import numpy as np

FB = web.YahooOptions('NIFTY-I')

for exp in FB.expiry_dates:
    print(exp.isoformat())
