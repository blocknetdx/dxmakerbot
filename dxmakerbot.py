#!/usr/bin/env python3
import time
import random
import argparse
import sys
import logging
from utils import dxbottools
from utils import trexbot
from utils import dxsettings

logging.basicConfig(filename='botdebug.log',
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s - %(message)s',
                    datefmt='[%Y-%m-%d:%H:%M:%S]')

parser = argparse.ArgumentParser()
parser.add_argument('--maker', help='maker chain', default='BLOCK')
parser.add_argument('--taker', help='taker chain', default='LTC')
parser.add_argument('--slidemin', help='price slide adjustment', default=1.000001)
parser.add_argument('--slidemax', help='price slide adjustment', default=1.019999)
parser.add_argument('--cancelall', help='cancel all orders and exist', action='store_true')
parser.add_argument('--cancelmarket', help='cancel all orders in a given market')
parser.add_argument('--sellmin', help='maker sell min order size', default=0.001)
parser.add_argument('--sellmax', help='maker sell max order size', default=1)
parser.add_argument('--delay', help='sleep delay value', default=3)
parser.add_argument('--maxloop', help='max number of order loops', default=7)
parser.add_argument('--maxopen', help='max number of open orders', default=5)
parser.add_argument('--minbalance', help='minbalance value for loop', default=10)
parser.add_argument('--usecb', help='enable cryptobridge pricing', action='store_true')
args = parser.parse_args()

BOTsellmarket = args.maker.upper()
BOTbuymarket = args.taker.upper()
BOTslidemin = float(args.slidemin)
BOTslidemax = float(args.slidemax)
BOTdelay = args.delay
BOTusecb = args.usecb
BOTminbalance = args.minbalance
maxloopcount = args.maxloop
maxordercount = args.maxopen
loopcount = 0
ordercount = 0

if args.cancelall:
    results = dxbottools.cancelallorders()
    print(results)
    sys.exit(0)
elif args.cancelmarket:
    results = dxbottools.cancelallordersbymarket(args.cancelmarket.upper())
    sys.exit(0)

print('>>>> Start maker bot')
time.sleep(BOTdelay) # wait for cancel orders
print(BOTsellmarket, BOTbuymarket)
print('>>>> Checking pricing information')
marketprice = trexbot.getpricedata(BOTsellmarket, BOTbuymarket, BOTusecb)
if marketprice == 0:
    print('#### Pricing not availabe')
    sys.exit(1)

print('>>>> Makers market price: {}'.format(trexbot.getpricedata(BOTsellmarket, BOTbuymarket, BOTusecb)))

# order loop
makeraddress = dxsettings.tradingaddress[BOTsellmarket]
takeraddress = dxsettings.tradingaddress[BOTbuymarket]

if __name__ == "__main__":
    while 1:  # loop forever
        mybalances = dxbottools.rpc_connection.dxGetTokenBalances()
        makerbalance = float(mybalances[BOTsellmarket])
        print('>>>> Pre-start balances: {}'.format(makerbalance))
        while makerbalance > 0:
            makermarketprice = trexbot.getpricedata(BOTsellmarket, BOTbuymarket, BOTusecb)
            print('>>>> Market price: {}'.format(makermarketprice))
            mybalances = dxbottools.rpc_connection.dxGetTokenBalances()
            makerbalance = float(mybalances[BOTsellmarket])
            print('>>>> Balances: {}'.format(makerbalance))
            #generate random sell amount
            sellamount = random.uniform(float(args.sellmin), float(args.sellmax))
            sellamount = '%.6f' % sellamount

            #adjust price based on slide value
            print('>>>> makerprice: {}'.format(makermarketprice))
            print('>>>> slidemin: {}'.format(BOTslidemin))
            print('>>>> sldiemax: {}'.format(BOTslidemax))
            makermarketpriceslide = float(makermarketprice) * float(random.uniform(BOTslidemin, BOTslidemax))
            print('>>>> slide adjusted makerprice: {}'.format(makermarketpriceslide))
            print('>>>> sell amount: {}'.format(str(sellamount)))
            buyamount = (float(sellamount) * float(makermarketpriceslide)) 
            buyamountclean = '%.6f' % buyamount
            print('>>>> buyamount {}'.format(buyamountclean))
            currentopenorders = len(dxbottools.getopenordersbymaker(BOTsellmarket))
            print('>>>> currentopenorders: {} maker: {}'.format(currentopenorders, BOTsellmarket))
            if (ordercount < maxordercount) and (currentopenorders < (maxordercount)):
                try:
                    print('>>>> Placing order...')
                    results = {}
                    results = dxbottools.makeorder(BOTsellmarket, str(sellamount), makeraddress, BOTbuymarket, str(buyamountclean), takeraddress)
                    print('>>>> Order placed, id: {0} maker_size: {1} taker_size: {2}'.format(results['id'], results['maker_size'], results['taker_size']))
                    logging.info('Order placed, id: {0} maker_size: {1} taker_size: {2}'.format(results['id'], results['maker_size'], results['taker_size']))
                except Exception as err:
                    print('ERROR: %s' % err)
                    print('Completed')
            else:
                print('##### Too many orders open - open order count: {}, loopcount: {}'.format(currentopenorders, loopcount))
            loopcount += 1
            ordercount += 1
            print('sleep')
            time.sleep(BOTdelay)
            if loopcount > maxloopcount:
                results = dxbottools.canceloldestorder(BOTsellmarket)
                logging.info('Canceled order ID: {} '.format(results))
                print('>>>> Canceled oldest: {}'.format(results))
                loopcount = 0
                ordercount = 0
                time.sleep(BOTdelay)
        if makerbalance <= BOTminbalance:
            loopcount += 1
        if loopcount > maxloopcount:
            results = dxbottools.canceloldestorder(BOTsellmarket)
            logging.info('Canceled order ID: {} '.format(results))
            print('>>>> Canceled oldest: {}'.format(results))
            loopcount = 0
            ordercount = 0
            time.sleep(BOTdelay)
            print('>>>> Canceled oldest sleeping...')


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
