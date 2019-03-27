#!/usr/bin/env python3
__author__ = 'atcsecure'
__copyright__ = 'All rights reserved'
__credits__ = ['atcsecure']
__license__ = 'GPL'
__version__ = '0.0.1'
__maintainer__ = 'atcsecure'
__status__ = 'Alpha'

import time
import sys
import requests
from utils import coingecko
from bittrex.bittrex import Bittrex, API_V2_0
from utils import custompricing
from utils import dxsettings

my_bittrex = Bittrex(None, None)

def getcustommarketpricing(maker, taker):
  maker = maker.upper()
  taker = taker.upper()
  assets = [maker,taker]
  makerprice = 0
  takerprice = 0
  print('>>>> Looking up custom pricing: {}-{}'.format(maker,taker))
  for asset in assets:
    assetprice = 0
    try:
      endpoint = dxsettings.apiendpoint[asset]
    except Exception as e:
      print('ERROR: {}'.format(e))
      print('Check dxsettings.py for custom price URL: {}'.format(asset))
      sys.exit(1)
    if asset == 'BTC':
      assetprice = 1
    else:
      try:
        assetprice = custompricing.getprice(asset,endpoint)
      except Exception as e:
        print('ERROR: {}'.format(e))
        print('Unable to use custom pricing, program aborted...')
        sys.exit(1)
    print('>>>> {} price: {}'.format(asset,assetprice))
    if asset == maker:
      makerprice = float(assetprice)
    else:
      takerprice = float(assetprice)
  lastprice = makerprice / takerprice
  print('>>>> {}-{} market price: {}'.format(maker,taker,lastprice))
  return lastprice




def getmarketprice(marketname, BOTuse):
  # get market price
  markets = []
  markets = marketname.split('-')
  lastprice = 0
  if markets[1] == 'BTC':
    marketname = '{}-{}'.format(markets[1], markets[0])

  if BOTuse == 'cg':
    print('>>>> Looking up CoinGecko pricing: {}'.format(markets[1]))
    cg = coingecko.CoinGeckoAPI()
    cg_coin_list = cg.get_coins_list()
    # CoinGecko uses IDs, need to lookup ID for market
    for coin in cg_coin_list:
      if coin['symbol'] == markets[1].lower():
        coin_id = coin['id']
        print('Found {} ID: {}'.format(markets[1],coin_id))
        currentprice = cg.get_price(ids=coin_id, vs_currencies=markets[0])
        lastprice = currentprice[coin_id]
        vsmarket = markets[0].lower()
        print('Last price: {}'.format(lastprice[vsmarket]))
        lastprice = lastprice[vsmarket]
        break

  if BOTuse == 'cb' and dxsettings.cryptobridgeURL:
    resp = requests.get(url=dxsettings.cryptobridgeURL)
    data = resp.json()
    cbmarketname = '{}_{}'.format(markets[1], markets[0])
    print('>>>> Looking up CryptoBridge market: {}'.format(cbmarketname))
    for z in data:
      if (z['id']) == cbmarketname:
        lastprice = z['last']
        print('>>>> Found market: {}, Price: {}'.format(cbmarketname,lastprice))

  if not lastprice:
    print('>>>> Looking up Bittrex market: {}'.format(marketname))
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
  basemarket = ('BTC-{}'.format(maker))
  takermarket = ('BTC-{}'.format(taker))
  print('>>>> Maker: {}, Taker: {}'.format(maker,taker))
  if BOTuse == 'custom':
    marketprice = getcustommarketpricing(maker, taker) 
    return marketprice
  print('>>>> Base market: {}'.format(basemarket))
  if maker == 'BTC':
    marketprice = 1/getmarketprice(takermarket, BOTuse)
    return marketprice
  makerprice = getmarketprice(basemarket, BOTuse)
  print('>>>> Taker market: {}'.format(takermarket))
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
