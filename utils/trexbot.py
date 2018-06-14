import json
import time
from bittrex.bittrex import Bittrex, API_V2_0

my_bittrex = Bittrex(None, None)

def getmarketprice(marketname):
  # get market price
  summary = my_bittrex.get_market_summary(marketname)
  lastprice = summary['result'][0]['Last'] 
  return lastprice

def getpricedata():
  #x = my_bittrex.get_market_summary('BTC-LTC')

  USDBTCmarket = "USD-BTC"
  BTCLTCmarket = "BTC-LTC"
  blockmarket  = "BTC-BLOCK"

  usdbtcprice = getmarketprice(USDBTCmarket)
  btcltcprice = getmarketprice(BTCLTCmarket)
  blockbtcprice = getmarketprice(blockmarket)
  ltcusdprice = (usdbtcprice * btcltcprice)
  blockusdprice = (usdbtcprice * blockbtcprice)
  blockusdltcprice = blockusdprice / ltcusdprice
  blockltcprice = blockbtcprice / btcltcprice
  return blockltcprice

