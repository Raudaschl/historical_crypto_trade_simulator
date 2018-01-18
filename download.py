import pandas as pd
import urllib.request
import json
from pandas.io.json import json_normalize


coin_types = {"btc": 'btc.csv', 
			"eth": 'eth.csv',
			"dash": "dash.csv",
			"ltc": "ltc.csv",
			"omg": "omg.csv",
			"xrp": "xrp.csv",
			"vtc": "vtc.csv",
			"gnt": "gnt.csv",
			"1st": "1st.csv",
			"bts": "bts.csv",
			"bat": "bat.csv",
			"sc": "sc.csv",
			"vox": "vox.csv",
			"pot": "pot.csv",
			"excl": "excl.csv",
			"iot": "iot.csv",
			"bch": "bch.csv"
			}

for coin_type, filename in coin_types.items():
	print(filename)

	endpoint = "https://min-api.cryptocompare.com/data/histoday?fsym="+str(coin_type).upper()+"&tsym=USD&limit=300&aggregate=1&e=CCCAGG"

	prices = urllib.request.urlopen(endpoint).read()

	data = json.loads(prices)
	prices = json_normalize(data['Data'])
	prices['time'] = pd.to_datetime(prices['time'].astype(int), unit='s')

	prices=prices.rename(columns = {'time':'Date', 'close':'Price'})
	prices.columns = map(str.title, prices.columns)
	prices = prices.iloc[::-1]

	print(prices)
    

	prices.to_csv(filename, index=False)

	pass
