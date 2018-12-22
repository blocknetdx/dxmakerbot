#!/usr/bin/env python3
import time
import random
import argparse
import sys
from utils import dxbottools
from utils import trexbot
from utils import dxsettings

# TODO: Implementing CLI based arg's
parser = argparse.ArgumentParser()
parser.add_argument('--maker', help='maker chain', default='BLOCK')
parser.add_argument('--taker', help='taker chain', default='LTC')
parser.add_argument('--slide', help='price slide adjustment', default=0.999887)
args = parser.parse_args()

#
print ('running with args')
print (args)
##
BOTsellmarket = args.maker.upper()
BOTbuymarket = args.taker.upper()
BOTslide = args.slide

results = dxbottools.cancelallorders()
print (results)
time.sleep(1.5) # wait for cancel orders
print ("start bot")
print (" - checking trex api ...")
print ('makers market price: %s' %(trexbot.getpricedata(BOTsellmarket, BOTbuymarket)))
# init values
maxloopcount = 30 # 1 loop per minute, then cancel all orders, start over
loopcount = 0
maxordercount = 10
ordercount = 0

# order loop

if __name__ == "__main__":
  while 1:  # loop forever
    #print('.', end='')
    mybalances = dxbottools.rpc_connection.dxGetTokenBalances()
    blockbalance = float(mybalances[BOTsellmarket]) 
    print('pre-start balances: %s' % blockbalance)
    while blockbalance > 10:
      print ('balance ok')
      makermarketprice = trexbot.getpricedata(BOTsellmarket, BOTbuymarket)
      print (makermarketprice)
      print ('loopcount', loopcount)
      print ('ordercount', ordercount)
      mybalances = dxbottools.rpc_connection.dxGetTokenBalances()
      blockbalance = float(mybalances[BOTsellmarket])
      print ('Balances', blockbalance)
      #generate random sell amount of block
      sellamount = random.uniform(0.511133, 15.999999)
      sellamount = '%.6f' % sellamount

      # calc buy amount


      #adjust block ltc price
      print('block: ', makermarketprice)
      print('slide: ', BOTslide)
      makermarketpriceslide = float(makermarketprice) * float(random.uniform(1.0011,1.0999))
      
      print ('blockprice: ', makermarketpriceslide)
      #place sell order         
      print ('sell amount', str(sellamount))

      # we have the price per block sellamount * makermarketprice
      buyamount = float(sellamount) * float(makermarketpriceslide)
      buyamountclean = '%.6f' % buyamount
      if ordercount < maxordercount:
        results = dxbottools.rpc_connection.dxMakeOrder(BOTsellmarket, str(sellamount), dxsettings.blocktradingaddress, BOTbuymarket, str(buyamountclean), dxsettings.ltctradingaddress, "exact")
        #print (results['id'])
        #print (results['taker_size'])
        #print (results['maker_size'])
        print (results)
      else:
        print('too many orders open')
      loopcount += 1
      ordercount += 1
      print ('sleep')
      time.sleep(3)
      if loopcount > maxloopcount:
        dxbottools.canceloldestorder()
        loopcount = 0
        ordercount = 0
        time.sleep(3.5)
    if blockbalance <= 10:
      loopcount += 1
    if loopcount > maxloopcount:
      dxbottools.canceloldestorder()
      print ("canceled oldest")
      loopcount = 0
      ordercount = 0
      time.sleep(3.5)
      print ('canceled oldest sleeping...')
      time.sleep(120)


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
