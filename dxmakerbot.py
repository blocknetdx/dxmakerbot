#!/usr/bin/python3
import time
import random
from utils import dxbottools
from utils import trexbot
from utils import dxsettings
  
##
BOTsellmarket = "BLOCK"
BOTbuymarket = "LTC"
BOTslide = 0.999

# lets clear the orders on startup
dxbottools.cancelallorders()

# init values
maxloopcount = 10 # 1 loop per minute, then cancel all orders, start over
loopcount = 0
maxordercount = 1
ordercount = 0
mybalances = dxbottools.rpc_connection.dxGetTokenBalances()
blockbalance = float(mybalances['BLOCK'])
# order loop

if __name__ == "__main__":
  while 1:  # loop forever
    while blockbalance > 50:
      blockltcprice = trexbot.getpricedata()
      print (blockltcprice)
      print ('loopcount', loopcount)
      print ('ordercount', ordercount)
      mybalances = dxbottools.rpc_connection.dxGetTokenBalances()
      blockbalance = float(mybalances['BLOCK'])
      print ('Balances', blockbalance)
      #generate random sell amount of block
      sellamount = random.uniform(0.5111, 9.9999)
      sellamount = '%.6f' % sellamount

      # calc buy amount


      #adjust block ltc price
      print('block: ', blockltcprice)
      print('slide: ', BOTslide)
      blockltcpriceslide = float(blockltcprice) * float(BOTslide)
      
      print ('blockprice: ', blockltcpriceslide)
      #place sell order         
      print ('sell amount', str(sellamount))

      # we have the price per block sellamount * blockltcprice
      buyamount = float(sellamount) * float(blockltcpriceslide)
      buyamountclean = '%.6f' % buyamount
      if ordercount < maxordercount:
        results = dxbottools.rpc_connection.dxMakeOrder(BOTsellmarket, str(sellamount), dxsettings.blocktradingaddress, BOTbuymarket, str(buyamountclean), dxsettings.ltctradingaddress, "exact")
      else:
        print('too many orders open')
      loopcount += 1
      ordercount += 1
      print (results)
      time.sleep(60)
      if loopcount > maxloopcount:
        dxbottools.cancelallorders()
        loopcount = 0
        ordercount = 0


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
