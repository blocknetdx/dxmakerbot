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
import requests
from bittrex.bittrex import Bittrex, API_V2_0

my_bittrex = Bittrex(None, None)
cryptobridgeURL = 'https://api.crypto-bridge.org/api/v1/ticker'
cryptobridgeURL = ''

def getmarketprice(marketname):
  # get market price
  markets = []
  markets = marketname.split('-')
  lastprice = 0
  if markets[1] == 'BTC':
    marketname = '{0}-{1}'.format(markets[1], markets[0])

  if cryptobridgeURL:
    resp = requests.get(url=cryptobridgeURL)
    data = resp.json()
    cbmarketname = '{0}_{1}'.format(markets[1], markets[0])
    print ('>>>> Looking up cryptobridge market: {}'.format(cbmarketname))
    for z in data:
      if (z['id']) == cbmarketname:
        lastprice = z['last']
        print ('>>>> Found Market: {0} Price: {1}'.format(cbmarketname,lastprice))

  if not lastprice:
    print ('>>>> Looking up BITTREX market: {}'.format(marketname))
    for attempt in range(0,5):
      summary = my_bittrex.get_market_summary(marketname)
      try:
        lastprice = summary['result'][0]['Last'] 
      except Exception as e:
        print('#### API call attempt# {2} - exception/error {0}, bittrex called failed for {1}'.format(e, marketname, attempt))
        print(summary)
        time.sleep(2.5)
        lastprice = 0
        continue
      break
  return float(lastprice)

def getpricedata(maker, taker):
  basemarket = ('BTC-{0}'.format(maker))
  takermarket = ('BTC-{0}'.format(taker))
  print ('>>>> maker: {0}, taker: {1}'.format(maker,taker))
  print ('>>>> basemarket: %s' % basemarket)
  if maker == 'BTC':
    marketprice = 1/getmarketprice(takermarket)
    return marketprice
  makerprice = getmarketprice(basemarket)
  print ('>>>> takermarket: %s' % takermarket)
  if taker == 'BTC':
    marketprice = makerprice
  else:
    takerprice = getmarketprice(takermarket)
    try:
      marketprice = makerprice / takerprice
    except:
      marketprice = 0
      print('ERROR: price set to 0')
  return marketprice


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

