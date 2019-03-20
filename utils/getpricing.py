#!/usr/bin/env python3
__author__ = "atcsecure"
__copyright__ = "All rights reserved"
__credits__ = ["atcsecure"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "atcsecure"
__status__ = "Alpha"

import time
import requests
from utils import coingecko
from bittrex.bittrex import Bittrex, API_V2_0
from utils import dxsettings

my_bittrex = Bittrex(None, None)


def getmarketprice(marketname, BOTuse):
  # get market price
  markets = []
  markets = marketname.split('-')
  lastprice = 0
  if markets[1] == 'BTC':
    marketname = '{0}-{1}'.format(markets[1], markets[0])

  if BOTuse == 'cg':
    print ('using coingeckoapi')
    cg = coingecko.CoinGeckoAPI()
    cg_coin_list = cg.get_coins_list()
    # cg uses id's, need to lookup id for market
    print ('looking for {}'.format(markets[1]))
    for coin in cg_coin_list:
      if coin['symbol'] == markets[1].lower():
        coin_id = coin['id']
        print ('found coin id: {}'.format(coin_id))
        currentprice = cg.get_price(ids=coin_id, vs_currencies=markets[0])
        lastprice = currentprice[coin_id]
        #print (markets[1])
        #print (markets[0])
        vsmarket = markets[0].lower()
        print ('lastprice: {}'.format(lastprice[vsmarket]))
        lastprice = lastprice[vsmarket]
        break

  if BOTuse == 'cb' and dxsettings.cryptobridgeURL:
    resp = requests.get(url=dxsettings.cryptobridgeURL)
    data = resp.json()
    cbmarketname = '{0}_{1}'.format(markets[1], markets[0])
    print ('>>>> Looking up CryptoBridge market: {}'.format(cbmarketname))
    for z in data:
      if (z['id']) == cbmarketname:
        lastprice = z['last']
        print ('>>>> Found market: {0}, Price: {1}'.format(cbmarketname,lastprice))

  if not lastprice:
    print ('>>>> Looking up Bittrex market: {}'.format(marketname))
    for attempt in range(0,5):
      summary = my_bittrex.get_market_summary(marketname)
      try:
        lastprice = summary['result'][0]['Last'] 
      except Exception as e:
        print('#### API call attempt #{2} - exception/error: {0}, Bittrex call failed for: {1}'.format(e, marketname, attempt))
        print(summary)
        time.sleep(2.5)
        lastprice = 0
        continue
      break
  return float(lastprice)

def getpricedata(maker, taker, BOTuse):
  basemarket = ('BTC-{0}'.format(maker))
  takermarket = ('BTC-{0}'.format(taker))
  print ('>>>> Maker: {0}, Taker: {1}'.format(maker,taker))
  print ('>>>> Base market: %s' % basemarket)
  if maker == 'BTC':
    marketprice = 1/getmarketprice(takermarket, BOTuse)
    return marketprice
  makerprice = getmarketprice(basemarket, BOTuse)
  print ('>>>> Taker market: %s' % takermarket)
  if taker == 'BTC':
    marketprice = makerprice
  else:
    takerprice = getmarketprice(takermarket, BOTuse)
    try:
      marketprice = makerprice / takerprice
    except:
      marketprice = 0
      print('ERROR: Price set to 0')
  return marketprice


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

