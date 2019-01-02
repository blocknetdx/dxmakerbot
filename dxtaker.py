#!/usr/bin/env python3
import time
import random
import argparse
import sys
from utils import dxbottools
from utils import trexbot
from utils import dxsettings

parser = argparse.ArgumentParser()
parser.add_argument('--maker', help='maker chain', default='BLOCK')
parser.add_argument('--taker', help='taker chain', default='LTC')
args = parser.parse_args()


def takeorder(id, fromaddr, toaddr):
  results = dxbottools.takeorder(orderid, fromaddr, toaddr)
  return results


dxmaker = args.maker
dxtaker = args.taker

asks, bids = dxbottools.getorderbook(dxmaker, dxtaker)

bestbidpriceorder = dxbottools.gethighprice(bids)
bestaskpriceorder = dxbottools.getlowprice(asks)
# get order id from "asks" side
buyingorders = bool(random.getrandbits(1))
if buyingorders:
  orderid = bestaskpriceorder[2]
  results = takeorder(orderid, dxsettings.tradingaddress[dxtaker], dxsettings.tradingaddress[dxmaker])
else:
  orderid =  bestbidpriceorder[2]
  results = takeorder(orderid, dxsettings.tradingaddress[dxmaker], dxsettings.tradingaddress[dxtaker])

print(results)

