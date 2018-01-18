import pandas as pd
# import emoji
import datetime as dt     


today = dt.datetime.today().strftime("%Y-%m-%d")
profit = 0
dividends = 0

coinTypes = {"btc": 'btc.csv', 
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



# coinTypesArray = []
# for coinType in coinTypes:
# 	table = pd.read_csv(coinTypes[coinType])
	
# 	coinTypesArray.append({"coin": "btc", "table": table})
# 	pass
# print(coinTypesArray)

# pd.options.display.precision = 16

bitCoinOrders = []
bitCoinOrders.append({"coin": "btc", "buyPrice": 2600, "coins": 0.0702, "date": "2017-06-28"})



bitCoinOrders.append({"coin": "eth", "buyPrice": 200, "coins": 1.60, "date": "2017-04-27"})



bitCoinOrders.append({"coin": "dash", "buyPrice": 170, "coins": 1.80, "date": "2017-06-24"})



bitCoinOrders.append({"coin": "ltc", "buyPrice": 38.02, "coins": 6.802, "date": "2017-07-20"})



bitCoinOrders.append({"coin": "omg", "buyPrice": 1.10, "coins": 27.50, "date": "2017-04-01"})

voxOrders = []
voxOrders.append({"buyPrice": 0.0472, "coins": 402.95, "date": "2017-07-29"})

bitCoinOrders.append({"coin": "xrp", "buyPrice": 0.1057, "coins": 100, "date": "2017-08-07"})
bitCoinOrders.append({"coin": "xrp", "buyPrice": 0.1069, "coins": 120.099, "date": "2017-10-20"})

bitCoinOrders.append({"coin": "vtc", "buyPrice": 1.00, "coins": 20, "date": "2017-09-23"})

exclOrders = []
exclOrders.append({"buyPrice": 0.545, "coins": 40.577, "date": "2017-07-20"})


bitCoinOrders.append({"coin": "gnt", "buyPrice": 0.2406, "coins": 90.04, "date": "2017-08-01"})
bitCoinOrders.append({"coin": "gnt", "buyPrice": 0.202, "coins": 91.06, "date": "2017-09-23"})


bitCoinOrders.append({"coin": "1st", "buyPrice": 0.4077, "coins": 40.7, "date": "2017-09-04"})


bitCoinOrders.append({"coin": "bts", "buyPrice": 0.10859, "coins": 102, "date": "2017-09-04"})


bitCoinOrders.append({"coin": "bat", "buyPrice": 0.2058, "coins": 102, "date": "2017-09-04"})


bitCoinOrders.append({"coin": "sc", "buyPrice": 0.00807, "coins": 2502.411, "date": "2017-09-05"})
bitCoinOrders.append({"coin": "sc", "buyPrice": 0.00408, "coins": 5029.41, "date": "2017-11-21"})

potOrders = []
potOrders.append({"buyPrice": 0.0705, "coins": 320.60, "date": "2017-08-11"})

orderHistory = []
additionalOrders = []
dfAdditionalOrders = pd.DataFrame(columns=['coin', 'amountSpent', 'buyPrice', 'coins', 'date'])

def calculate(arrayName, orderIndex, coin, buyPrice, coins, date):

	global profit
	global dividends
	global coinTypes
	global orderHistory

	# Set profit factor
	profitFactor = 3
	minimumSellValue = 40
	reinvestPercentage = 40

	df = pd.read_csv(coinTypes[coin])
	reversed_df = df.iloc[::-1]

	df['Date'] = pd.to_datetime(df['Date'])

	
	for index, row in df[df['Date'] >= date].iloc[::-1].iterrows():


		if type(row['High']) is str:
			currentPrice = float(row['High'].replace(',',''))
		else:
			currentPrice = row['High']
			pass
		
		percent = int(round((currentPrice/buyPrice)*100, 0))

		# print(percent)
		if percent > profitFactor*100:
			# print("sell")
			buyPrice = buyPrice*(profitFactor)
			singleProfit = (coins*(reinvestPercentage/100))*buyPrice


			if singleProfit == 0:
				continue
			# if the profit is less than $40 then sell all coins
			elif singleProfit < minimumSellValue:
				singleProfit = (coins*1)*buyPrice
				profit += singleProfit
				coins = coins*0
				dividends += singleProfit

				updateCoins(arrayName, orderIndex, coins)

				orderHistory.append({"array": arrayName, "order": "sell", "coin": coin, "orderIndex": orderIndex, "profit": singleProfit, "date": row['Date']})
			else:
				profit += singleProfit
				coins = coins*(1 - reinvestPercentage/100)

				updateCoins(arrayName, orderIndex, coins)


				orderHistory.append({"array": arrayName, "order": "sell", "coin": coin, "orderIndex": orderIndex, "profit": singleProfit, "date": row['Date']})
				buyNow(coin, singleProfit, row['Date'])
				pass

			

			pass
		
		# print(row['Low'], row['High'])
		pass
	
	# print(coin)
	# print(coins)
	pass


def updateCoins(arrayName, orderIndex, coins):

	global bitCoinOrders
	global dfAdditionalOrders

	if arrayName == "bitCoinOrders":
		bitCoinOrders[orderIndex]["coins"] = coins
	elif arrayName == "additionalOrders":
		dfAdditionalOrders.loc[orderIndex, "coins"] = coins

		pass


	pass


def buyNow(coin, amount, date):
	global coinTypes
	global additionalOrders
	global dfAdditionalOrders

	# Configure buy weights
	buyWeights = buyWeightsBuild()

	for singleWeight in buyWeights:
		if singleWeight["coin"] == coin:
			buyWeights.remove(singleWeight)
			continue
			pass

		pass


	totalWeights = 0
	for singleWeight in buyWeights:
		totalWeights += singleWeight["weight"]
		pass

	percDiff = 1/totalWeights
	for singleWeight in buyWeights:
		singleWeight["weight"] = singleWeight["weight"]*percDiff
		pass
	# End of setting configure buy weights


	for singleWeight in buyWeights:
		newAmount = amount*singleWeight["weight"]

		df = pd.read_csv(coinTypes[singleWeight["coin"]])
		df['Date'] = pd.to_datetime(df['Date'])
		row = df[df['Date'] == date]

		if type(row['Price'].values[0]) is str:
			price = float(row['Price'].values[0].replace(',',''))
		else:
			price = row['Price'].values[0]
			pass
		
		coinsBought = newAmount/price

		# print(newAmount)
		# print(price)
		coinsBought = coinsBought + 0.0011

		data = pd.DataFrame({"coin": [singleWeight["coin"]], "amountSpent": [newAmount], "buyPrice": [price], "coins": [coinsBought], "date": [date]})

		dfAdditionalOrders = pd.concat([dfAdditionalOrders,data]).reset_index(drop=True)

		# additionalOrders.append({"coin": singleWeight["coin"], "amountSpent": newAmount, "buyPrice": price, "coins": coinsBought, "date": date})
		pass

	pass

def buyWeightsBuild():
	buyWeights = []
	buyWeights.append({"coin": "btc", "weight": 0.25})
	buyWeights.append({"coin": "eth", "weight": 0.25})
	buyWeights.append({"coin": "dash", "weight": 0.25})
	buyWeights.append({"coin": "ltc", "weight": 0.25})


	return buyWeights
	pass

def totalArrayValue(array):

	global today

	totalValue = 0
	for item in array:
		coins = item["coins"]
		coin = item["coin"]

		df = pd.read_csv(coinTypes[coin])
		df['Date'] = pd.to_datetime(df['Date'])

		row = df[df['Date'] == today]

		if type(row['Price'].values[0]) is str:
			price = float(row['Price'].values[0].replace(',',''))
		else:
			price = row['Price'].values[0]
			pass

		value = price * coins
		totalValue += value
		pass

	return totalValue
	pass

def totalArrayValueDF(array):

	global today

	totalValue = 0
	for index, item in array.iterrows():
		coins = item["coins"]
		coin = item["coin"]

		df = pd.read_csv(coinTypes[coin])
		df['Date'] = pd.to_datetime(df['Date'])

		row = df[df['Date'] == today]

		if type(row['Price'].values[0]) is str:
			price = float(row['Price'].values[0].replace(',',''))
		else:
			price = row['Price'].values[0]
			pass

		value = price * coins
		totalValue += value
		pass

	return totalValue
	pass


print("original Value $"+str(totalArrayValue(bitCoinOrders)))

for index, order in enumerate(bitCoinOrders):
	calculate("bitCoinOrders", index, order["coin"], order["buyPrice"], order["coins"], order["date"])
	pass

# print(len(dfAdditionalOrders))
# print("profits "+str(profit))
print("Original Dividends $"+str(dividends))


for index, order in dfAdditionalOrders.iterrows():
	calculate("additionalOrders", index, order["coin"], order["buyPrice"], order["coins"], order["date"])
	pass

df = pd.DataFrame(bitCoinOrders)
df.to_csv("bitCoinOrders.csv", sep='\t')


# print(dfAdditionalOrders)
dfAdditionalOrders.to_csv("additionalOrders.csv", sep='\t')

df = pd.DataFrame(orderHistory)
df.to_csv("orderHistory.csv", sep='\t')



# print(len(dfAdditionalOrders))
# print("profits "+str(profit))
print("Final Dividends "+str(dividends))

after = totalArrayValue(bitCoinOrders)
additional = totalArrayValueDF(dfAdditionalOrders)
print("Original Investments Value $"+str(after))
print("New Investments Value $"+str(additional))


print("Final Total Value $"+str(after+additional+dividends))
# print("Final Total Value $"+str(after+additional+dividends)+emoji.emojize(' :moneybag: :moneybag: :moneybag:', use_aliases=True))
