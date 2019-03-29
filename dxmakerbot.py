#!/usr/bin/env python3
import time
import random
import argparse
import sys
import logging
from utils import dxbottools
from utils import getpricing as pricebot
from utils import dxsettings

logging.basicConfig(filename='botdebug.log',
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s - %(message)s',
                    datefmt='[%Y-%m-%d:%H:%M:%S]')

parser = argparse.ArgumentParser()
parser.add_argument('--maker', help='asset being sold (default=BLOCK)', default='BLOCK')
parser.add_argument('--taker', help='asset being bought (default=LTC)', default='LTC')
parser.add_argument('--sellmin', help='min maker sell order size (default=0.001)', default=0.001)
parser.add_argument('--sellmax', help='max maker sell order size (default=1)', default=1)
parser.add_argument('--slidemin', help='minimum order price multipler (default=1.000001) minimum order price = slidemin * price source quote', default=1.000001)
parser.add_argument('--slidemax', help='maximum order price multipler (default=1.019999) maximum order price = slidemax * price source quote', default=1.019999)
parser.add_argument('--delay', help='sleep delay, in seconds, between loops to place/cancel orders (default=3)', default=3)
parser.add_argument('--maxloop', help='number of loops before canceling the oldest order (default=7)', default=7)
parser.add_argument('--maxopen', help='max number of open orders (default=5)', default=5)
parser.add_argument('--minbalance', help='min balance you want to maintain of the asset being sold (default=10)', default=10)
parser.add_argument('--usecb', help='enable cryptobridge pricing', action='store_true')
parser.add_argument('--usecg', help='enable coingecko pricing', action='store_true')
parser.add_argument('--usecustom', help='enable custom pricing', action='store_true')
parser.add_argument('--cancelall', help='cancel all orders and exit', action='store_true')
parser.add_argument('--cancelmarket', help='cancel all orders in a given market')
args = parser.parse_args()

BOTsellmarket = args.maker.upper()
BOTbuymarket = args.taker.upper()
BOTslidemin = float(args.slidemin)
BOTslidemax = float(args.slidemax)
BOTdelay = args.delay

BOTminbalance = args.minbalance
maxloopcount = args.maxloop
maxordercount = args.maxopen
loopcount = 0
ordercount = 0

if args.usecustom:
    BOTuse = 'custom'
elif args.usecg:
    BOTuse = 'cg'
elif args.usecb:
    BOTuse = 'cb'
else:
    BOTuse = 'bt'

if args.cancelall:
    results = dxbottools.cancelallorders()
    print(results)
    sys.exit(0)
elif args.cancelmarket:
    results = dxbottools.cancelallordersbymarket(args.cancelmarket.upper(), BOTbuymarket)
    sys.exit(0)

print('>>>> Start maker bot')
time.sleep(BOTdelay) # wait for cancel orders
print(BOTsellmarket, BOTbuymarket)
print('>>>> Checking pricing information')
if BOTsellmarket == BOTbuymarket:
    print('ERROR: Maker and taker asset cannot be the same')
    sys.exit(0)
marketprice = pricebot.getpricedata(BOTsellmarket, BOTbuymarket, BOTuse)
if marketprice == 0:
    print('#### Pricing not available')
    sys.exit(1)

print('>>>> Market price: {}'.format(pricebot.getpricedata(BOTsellmarket, BOTbuymarket, BOTuse)))

# order loop
try:
    makeraddress = dxsettings.tradingaddress[BOTsellmarket]
    takeraddress = dxsettings.tradingaddress[BOTbuymarket]
except KeyError as e:
    print('ERROR: {}'.format(e))
    print('Check dxsettings.py for address entry')
    sys.exit(1)

if __name__ == '__main__':
    while 1:  # loop forever
        mybalances = dxbottools.rpc_connection.dxGetTokenBalances()
        makerbalance = float(mybalances[BOTsellmarket])
        print('>>>> Pre-start balances: {}'.format(makerbalance))
        while makerbalance > 0:
            makermarketprice = pricebot.getpricedata(BOTsellmarket, BOTbuymarket, BOTuse)
            print('>>>> Market price: {}'.format(makermarketprice))
            mybalances = dxbottools.rpc_connection.dxGetTokenBalances()
            makerbalance = float(mybalances[BOTsellmarket])
            print('>>>> Balances: {}'.format(makerbalance))
            # generate random sell amount
            sellamount = random.uniform(float(args.sellmin), float(args.sellmax))
            sellamount = '%.6f' % sellamount
            # adjust price based on slide value
            print('>>>> Market price: {}'.format(makermarketprice))
            print('>>>> slidemin: {}'.format(BOTslidemin))
            print('>>>> slidemax: {}'.format(BOTslidemax))
            makermarketpriceslide = float(makermarketprice) * float(random.uniform(BOTslidemin, BOTslidemax))
            print('>>>> Slide adjusted maker price: {}'.format(makermarketpriceslide))
            print('>>>> Sell amount: {}'.format(str(sellamount)))
            buyamount = (float(sellamount) * float(makermarketpriceslide)) 
            buyamountclean = '%.6f' % buyamount
            print('>>>> Buy amount {}'.format(buyamountclean))
            currentopenorders = len(dxbottools.getopenordersbymarket(BOTsellmarket,BOTbuymarket))
            print('>>>> Current open orders: {}, maker: {}, taker: {}'.format(currentopenorders, BOTsellmarket, BOTbuymarket))
            if (ordercount < maxordercount) and (currentopenorders < (maxordercount)):
                try:
                    print('>>>> Placing order...')
                    results = {}
                    results = dxbottools.makeorder(BOTsellmarket, str(sellamount), makeraddress, BOTbuymarket, str(buyamountclean), takeraddress)
                    print('>>>> Order placed - id: {0}, maker_size: {1}, taker_size: {2}'.format(results['id'], results['maker_size'], results['taker_size']))
                    logging.info('Order placed - id: {0}, maker_size: {1}, taker_size: {2}'.format(results['id'], results['maker_size'], results['taker_size']))
                except Exception as err:
                    print('ERROR: %s' % err)
            else:
                print('##### Too many orders open - open order count: {}, loopcount: {}'.format(currentopenorders, loopcount))
            loopcount += 1
            ordercount += 1
            print('sleep')
            time.sleep(BOTdelay)
            if loopcount > maxloopcount:
                results = dxbottools.canceloldestorder(BOTsellmarket, BOTbuymarket)
                logging.info('Canceled order ID: {} '.format(results))
                print('>>>> Canceled oldest: {}'.format(results))
                loopcount = 0
                ordercount = 0
                time.sleep(BOTdelay)
        if makerbalance <= BOTminbalance:
            loopcount += 1
        if loopcount > maxloopcount:
            results = dxbottools.canceloldestorder(BOTsellmarket, BOTbuymarket)
            logging.info('Canceled order ID: {} '.format(results))
            print('>>>> Canceled oldest: {}'.format(results))
            loopcount = 0
            ordercount = 0
            time.sleep(BOTdelay)
            print('>>>> Canceled oldest sleeping...')


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
