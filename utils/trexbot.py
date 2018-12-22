#!/usr/bin/env python3
__author__ = "atcsecure"
__copyright__ = "All rights reserved"
__credits__ = ["atcsecure"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "atcsecure"
__status__ = "Alpha"

import json
import time
from bittrex.bittrex import Bittrex, API_V2_0

my_bittrex = Bittrex(None, None)

def getmarketprice(marketname):
  # get market price
  summary = my_bittrex.get_market_summary(marketname)
  for attempt in range(0,5):
    while True:
      try:
        lastprice = summary['result'][0]['Last'] 
      except:
        print('API call exception/error')
        time.sleep(1.5)
        continue
      break
  return lastprice

def getpricedata(maker, taker):
  basemarket = ('BTC-{0}'.format(maker))
  takermarket = ('BTC-{0}'.format(taker))

  makerprice = getmarketprice(basemarket)
  takerprice = getmarketprice(takermarket)

  marketprice = makerprice / takerprice

  return marketprice


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
