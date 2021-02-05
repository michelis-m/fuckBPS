# fuckBPS
Pump it fellas!

To run get keys from Binance. Instructions here: https://www.binance.com/en/support/faq/360002502072-How-to-create-API

Then go to console and write:                         
$export binance_api="key_here"                    
$export binance_secret="secret_here"

This will save your keys as a local environment variable, that is accessible only from your pc.

To install dependencies do:
$pip install binance

You can run the script as:
$python3 pumpit.py <coin_name> 
e.g.
$python3 pumpit.py PNT
 

There are variables in the script for sell walls. Check first lines of the code.
