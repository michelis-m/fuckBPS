from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
from decimal import * 
getcontext().prec = 8
import sys, os

# **************************************************
# * This script will buy any coin with BTC as base *
# * Run as python3 buy.py <COINNAME>               *
# **************************************************

# **************************************************
# Set your keys as:                                *
# Go to console and write:                         *
# export binance_api="key_here"                    *
# export binance_secret="secret_here"              *
# **************************************************
API_KEY = os.environ.get('binance_api')
API_SECRET = os.environ.get('binance_secret')

# Connect to client
client = Client(API_KEY, API_SECRET)

# **************************************************************
# VARIABLES TO CHANGE (Do not change any of the other code)    *
# **************************************************************
PERCENTAGE_TO_BUY = 0.5     # How much of your BTC 

BALANCE_PRNTG_1 = 0.4       # How much percentage of bought coin you want to sell at first wall
PROFIT_TARGET_1 = 0.5       # How much profit the first wall should have (0.5 = 50%)

BALANCE_PRNTG_2 = 0.3       # BALANCE_PRNTG_1 / 2 & 3 must add up to 1 (100%)
PROFIT_TARGET_2 = 0.8       # Any tarrget here should be higher than previous one

BALANCE_PRNTG_3 = 0.3
PROFIT_TARGET_3 = 1.2

STOP_LOSS = 0.21            # If price drops below target sell everything and cry (0.2 = 20%)
                            # Most coins have stop loss restrictions so I recommend to keep this
                            # above 0.2. There is possibility that some coins also dont accept stop
                            # loss at all. In this case the script will sell your coins immediately
# **************************************************************

def sell_coin(coin_to_buy, bought_price, asset_name):
    # Coin balance remaining
    coin_balance = client.get_asset_balance(asset=asset_name)['free']
    info = client.get_symbol_info(coin_to_buy)

    # Check if coin has STOP_LOSS option otherwise sell instantly
    if 'STOP_LOSS_LIMIT' in info['orderTypes']:
        try:
            # Sell At First Stop Wall
            profit_order_1 = client.order_oco_sell(
                symbol=coin_to_buy,
                quantity=int(float(coin_balance)*BALANCE_PRNTG_1),
                price="{:.8f}".format(bought_price*(1 + PROFIT_TARGET_1)),
                stopPrice="{:.8f}".format(bought_price*(1 - STOP_LOSS + 0.01)),                                            
                stopLimitPrice= "{:.8f}".format(bought_price*(1 - STOP_LOSS)),
                stopLimitTimeInForce='FOK'
            )
            print("First profit order placed!")

            # Sell At First Stop Wall
            profit_order_2 = client.order_oco_sell(
                symbol=coin_to_buy,
                quantity=int(float(coin_balance)*BALANCE_PRNTG_2),
                price="{:.8f}".format(bought_price*(1 + PROFIT_TARGET_2)),
                stopPrice= "{:.8f}".format(bought_price*(1 - STOP_LOSS + 0.01)),                                            
                stopLimitPrice= "{:.8f}".format(bought_price*(1 - STOP_LOSS)),
                stopLimitTimeInForce='FOK'
            )
            print("Second profit order placed!")

            # Sell At First Stop Wall
            profit_order_3 = client.order_oco_sell(
                symbol=coin_to_buy,
                quantity=int(float(coin_balance)*BALANCE_PRNTG_3),
                price="{:.8f}".format(bought_price*(1 + PROFIT_TARGET_3)),
                stopPrice="{:.8f}".format(bought_price*(1 - STOP_LOSS + 0.01)),                                            
                stopLimitPrice="{:.8f}".format(bought_price*(1 - STOP_LOSS)),
                stopLimitTimeInForce='FOK'
            )
            print("Third profit order placed!")

        except BinanceAPIException as e:
            # error handling goes here
            print(e)
            print("A profit order failed! SELL MANUALLY ASAP!")
        except BinanceOrderException as e:
            # error handling goes here
            print(e)
            print("A profit order failed! SELL MANUALLY ASAP!")

    else:
        try:
            order = client.create_order(
                symbol=coin_to_buy,
                side="SELL",
                type="MARKET",
                quantity=int(float(coin_balance))
            )
            print("Sold instantly!")
        except BinanceAPIException as e:
            # error handling goes here
            print(e)
            print("Last order failed SELL MANUALLY ASAP!")
        except BinanceOrderException as e:
            # error handling goes here
            print(e)
            print("Last order failed SELL MANUALLY ASAP!")

def make_order(coin_to_buy, quantity_to_buy):
    # Try to make first order
    try: 
        order = client.create_order(
            symbol=coin_to_buy,
            side="BUY",
            type="MARKET",
            quantity=quantity_to_buy
        )
        bought_price = order['fills'][-1]['price']
        print("*********************")
        print("Bought at: ", bought_price)
        print("*********************")

    except BinanceAPIException as e:
        # error handling goes here
        print(e)
        print("No order placed for :", coin_to_buy)
    except BinanceOrderException as e:
        # error handling goes here
        print(e)
        print("No order placed for:", coin_to_buy)

    return float("{:.8f}".format(float(bought_price)))
    

def main(argv):

    # Current Balance
    balance = client.get_asset_balance(asset='BTC')['free']
    print("Current Balance in BTC: ", balance)

    # Convert the buying coin to 50% of your BTC reserve
    asset_name = sys.argv[1]
    coin_to_buy = asset_name + "BTC"
    coin_price = client.get_orderbook_ticker(symbol=coin_to_buy)['askPrice']
    quantity_to_buy = round((float(balance)/float(coin_price))*PERCENTAGE_TO_BUY, 0)

    print("Pair To Buy: ", coin_to_buy)
    print("Coin Price: ", coin_price)
    print("Buying quantity: ", quantity_to_buy)

    # Creating the orders
    bought_price = make_order(coin_to_buy, quantity_to_buy)

    # Selling
    sell_coin(coin_to_buy, bought_price, asset_name)

    # get balance for a specific asset only (BTC)
    print("BTC remaining: ", client.get_asset_balance(asset='BTC')['free'])

    print("Done!")
    print("Good luck bro :)")

if __name__ == "__main__":
    main(sys.argv[1:])