# Historical Cryptocurrency Trade Simulator
## Steps
Requires pandas and python 3
pip install pandas

### Step 1
Download hisotical data
python download.py 
To download the prices for different crypotcurrencies for the last 300 days as a csv file. You can edit the coin types in the download.py file.

### Step 2
Run the script
python trader.py
This will produce the following outputs:

Original Value - The current value of your investments assuming no trade strategy has been applied apart from holding onto your investments
Original Dividends - The total dividends based from your initial investments  

Final Dividends - The total dividends based on original and new investments
Original Investments Value - The total value of your original investments after the strategy is applied
New Investments Value - The total value of new investments made based on your strategy
Final Total Value - The total value of your investments and any dividends taken

### Step 3 - Customise
#### Set Orders
bitCoinOrders array is filled with different orders

Example:
bitCoinOrders.append({"coin": "btc", "buyPrice": 2690, "coins": 0.0782, "date": "2017-05-27"})
coin: sent the currency symbol (needs to be one of the currencies downloaded before)
buyPrice: original buy price ($)
coins: number of coins bought
date: date purchased

#### Calculate Function
**Function**

The calculate function takes an array of orders and examines their value from the point of purchase. During this iteration I have set up trading strategy which aims to sell 40% of the coins from a single order when that order has increased in value by 300%. That 40% is then reinvested by buying other cryptocurrencies which is in the dfAdditionalOrders array. If the value of the 40% sell is less than $40 then I will sell all the coins outright and claim that amount for myself as dividends.

**Variables**
profitFactor - Set the % value where you will take profit. Setting 3 for example will automatically trigger a sell at 300%
reinvestPercentage - the percentage of the total value of the order when the profit factor is reached to reinvest
minimumSellValue - Sell all coins of this specific order when the value hits the profitFactor and the value of the reinvestment is less than this value

#### BuyWeightsBuild function
**Function**
This function sets the coins to buy from the profits of any sell (see above). They exclude the coin that was originally sold so for example if bitcoin turned a profit and was sold it would not buy more bitcoin with the profits. 

**Variables**
buyWeights.append({"coin": "btc", "weight": 0.25})
coin - the symbol of the currency you want to buy (must be one of the currencies downloaded)
weight - this is an indicator to how much you want to buy of one currency compared to another. The total value of all weights should add up to 1.
