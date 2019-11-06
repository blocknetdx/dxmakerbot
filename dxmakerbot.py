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

# for better variables naming, understanding, finding and code management and autocomplete 
# variables has been divided into 3 groups global config as c, global static as s, global dynamic as d
class GlobVars(): pass    
#global config variables
c = GlobVars()
#global static variables
s = GlobVars()
#global dynamic variables
d = GlobVars()

def start_welcome_message():
    global c, s, d
    print('>>>> Starting maker bot')

def global_vars_preconfig_init():
    global c, s, d
    print('>>>> Global variables initialization')
    d.price_maker = 0
    d.ordersfinished = 0
    d.ordersfinishedtime = 0
    d.custom_dynamic_spread = 0
    d.balance_maker_total = 0
    d.balance_maker_left = 0
    d.balance_taker = 0

def load_config_verify_or_exit():
    global c, s, d
    print('>>>> Verifying configuration')
    
    error_num = 0
    
    if hasattr(c, 'BOTmakeraddress') == False:
        print('**** ERROR, <makeraddress> is not specified')
        error_num += 1
        
    if hasattr(c, 'BOTtakeraddress') == False:
        print('**** ERROR, <takeraddress> is not specified')
        error_num += 1
    
    # arguments: basic values
    if c.BOTsellstart <= 0:
        print('**** ERROR, <sellstart> value <{0}> is invalid'.format(c.BOTsellstart))
        error_num += 1
        
    if c.BOTsellend <= 0:
        print('**** ERROR, <sellend> value <{0}> is invalid'.format(c.BOTsellend))
        error_num += 1
        
    if c.BOTslidestart <= 1:
        print('**** ERROR, <slidestart> value <{0}> is invalid'.format(c.BOTslidestart))
        if not c.imreallysurewhatimdoing:
            error_num += 1
            
    if c.BOTslideend <= 1:
        print('**** ERROR, <slideend> value <{0}> is invalid'.format(c.BOTslideend))
        if not c.imreallysurewhatimdoing:
            error_num += 1
    
    if c.BOTmaxopenorders < 1:
        print('**** ERROR, <maxopen> value <{0}> is invalid'.format(c.BOTmaxopenorders))
        error_num += 1
            
    if c.BOTbalancesavenumber < 0:
        print('**** ERROR, <balancesavenumber> value <{0}> is invalid'.format(c.BOTbalancesavenumber))
        error_num += 1
    
    if c.BOTbalancesavepercent < 0 or c.BOTbalancesavepercent > 1:
        print('**** ERROR, <balancesavepercent> value <{0}> is invalid'.format(c.BOTbalancesavepercent))
        error_num += 1
    
    # arguments: dynamic values, special pump/dump order
    if c.BOTslidedynpositive < 0:
        print('**** ERROR, <slidedynpositive> value <{0}> is invalid'.format(c.BOTslidedynpositive))
        if not c.imreallysurewhatimdoing:
            error_num += 1
            
    if c.BOTslidedynnegative < 0:
        print('**** ERROR, <slidedynnegative> value <{0}> is invalid'.format(c.BOTslidedynnegative))
        if not c.imreallysurewhatimdoing:
            error_num += 1
        
    if c.BOTslidedynzoneignore < 0 or c.BOTslidedynzoneignore > 1:
        print('**** ERROR, <slidedynzoneignore> value <{0}> is invalid'.format(c.BOTslidedynzoneignore))
        error_num += 1
    
    if c.BOTslidedynzonemax < 0 or c.BOTslidedynzonemax > 1:
        print('**** ERROR, <slidedynzonemax> value <{0}> is invalid'.format(c.BOTslidedynzonemax))
        error_num += 1
    
    if c.BOTslidepump < 0:
        print('**** ERROR, <slidepump> value <{0}> is invalid'.format(c.BOTslidepump))
        error_num += 1
    
    if c.BOTpumpamount <= 0 and c.BOTslidepump > 0:
        print('**** ERROR, <pumpamount> value <{0}> is invalid'.format(c.BOTpumpamount))
        error_num += 1
        
    # arguments: reset orders by events
    if c.BOTresetonpricechangepositive < 0:
        print('**** ERROR, <resetonpricechangepositive> value <{0}> is invalid'.format(c.BOTresetonpricechangepositive))
        error_num += 1
    
    if c.BOTresetonpricechangenegative < 0:
        print('**** ERROR, <resetonpricechangenegative> value <{0}> is invalid'.format(c.BOTresetonpricechangenegative))
        error_num += 1
    
    if c.BOTresetafterdelay < 0:
        print('**** ERROR, <resetafterdelay> value <{0}> is invalid'.format(c.BOTresetafterdelay))
        error_num += 1
    
    if c.BOTresetafterorderfinishnumber < 0:
        print('**** ERROR, <resetafterorderfinishnumber> value <{0}> is invalid'.format(c.BOTresetafterorderfinishnumber))
        error_num += 1
    
    if c.BOTresetafterorderfinishdelay < 0:
        print('**** ERROR, <resetafterorderfinishdelay> value <{0}> is invalid'.format(c.BOTresetafterorderfinishdelay))
        error_num += 1
    
    # arguments: internal values changes
    if c.BOTdelayinternal < 1:
        print('**** ERROR, <delayinternal> value <{0}> is invalid'.format(c.BOTdelayinternal))
        error_num += 1
    
    if c.BOTdelaycheckprice < 1:
        print('**** ERROR, <delaycheckprice> value <{0}> is invalid'.format(c.BOTdelaycheckprice))
        error_num += 1
        
    if error_num > 0:
        print('>>>> Verifying configuration failed')
        sys.exit(1)
    else:
        print('>>>> Verifying configuration success')

def load_config():
    global c, s, d
    print('>>>> Loading program configuration')
    
    parser = argparse.ArgumentParser()
    
    # arguments: main maker/taker
    parser.add_argument('--maker', help='asset being sold (default=BLOCK)', default='BLOCK')
    parser.add_argument('--taker', help='asset being bought (default=LTC)', default='LTC')
    parser.add_argument('--makeraddress', help='trading address of asset being sold (default=None)', default=None)
    parser.add_argument('--takeraddress', help='trading address of asset being bought (default=None)', default=None)

    # arguments: basic values
    parser.add_argument('--sellstart', help='size of first order or random from range sellstart and sellend (default=0.001)', default=0.001)
    parser.add_argument('--sellend', help='size of last order or random from range sellstart and sellend  (default=0.001)', default=0.001)
    parser.add_argument('--sellrandom', help='orders size will be random number between sellstart and sellend, otherwise sequence of orders starting by sellstart amount and ending with sellend amount, ', action='store_true')
    parser.add_argument('--slidestart', help='price of first order will be equal to slidestart * price source quote(default=1.01 means +1%%)', default=1.01)
    parser.add_argument('--slideend', help='price of last order will be equal to slideend * price source quote(default=1.021 means +2.1%%)', default=1.021)
    parser.add_argument('--maxopen', help='Max amount of orders to have open at any given time. Placing orders sequence: first placed order is at slidestart(price slide),sellstart(amount) up to slideend(price slide),sellend(amount), last order placed is slidepump if configured, is not counted into this number (default=5)', default=5)
    parser.add_argument('--reopenfinished', help='reopen finished orders (default=1 means enabled)', default=1)
    parser.add_argument('--balancesavenumber', help='min taker balance you want to save and do not use for making orders specified by number (default=0)', default=0)
    parser.add_argument('--balancesavepercent', help='min taker balance you want to save and do not use for making orders specified by percent of maker+taker balance (default=0.05 means 5%%)', default=0.05)

    # arguments: dynamic values, special pump/dump order
    parser.add_argument('--slidedynpositive', help='dynamic price slide increase positive, applied if maker price goes up, range between 0 and slidedynpositive, dynamically computed by assets ratio (default=0, 0.5 means maximum at +50%% of price)', default=0)
    parser.add_argument('--slidedynnegative', help='dynamic price slide increase negative, applied if maker price goes down, range between 0 and slidedynnegative, dynamically computed by assets ratio (default=0, 0.1 means maximum at +10%% of price)', default=0)
    parser.add_argument('--slidedynzoneignore', help='dynamic price slide increase ignore is zone when dynamic slide is not activated(default=0.05 means 5%% of balance)', default=0.05)
    parser.add_argument('--slidedynzonemax', help='percentage when dynamic order price slide increase gonna reach maximum(default=0.9 means at 90%%)', default=0.9)
    parser.add_argument('--slidepump', help='if slide pump is non zero a special order out of slidemax is set, this order will be filled when pump happen(default=0 disabled, 0.5 means order will be placed +50%% out of maximum slide)', default=0)
    parser.add_argument('--pumpamount', help='pump order size, otherwise sellend is used(default=--sellend)', default=0)

    # arguments: reset orders by events
    parser.add_argument('--resetonpricechangepositive', help='percentual price positive change(you can buy more) when reset all orders (default=0, 0.05 means reset at +5%% change)', default=0)
    parser.add_argument('--resetonpricechangenegative', help='percentual price negative change(you can buy less) when reset all orders (default=0, 0.05 means reset at -5%% change)', default=0)
    parser.add_argument('--resetafterdelay', help='delay before resetting all orders in seconds (default=0 means disabled)', default=0)
    parser.add_argument('--resetafterorderfinishnumber', help='number of orders to be finished before resetting orders (default=0 means not set)', default=0)
    parser.add_argument('--resetafterorderfinishdelay', help='delay after finishing last order before resetting orders in seconds (default=0 not set)', default=0)

    # arguments: internal values changes
    parser.add_argument('--delayinternal', help='sleep delay, in seconds, between loops to place/cancel orders or other internal operations(can be used ie. case of bad internet connection...) (default=9)', default=9)
    parser.add_argument('--delaycheckprice', help='sleep delay, in seconds to check again pricing (default=180)', default=180)

    # arguments: pricing source arguments
    parser.add_argument('--usecb', help='enable cryptobridge pricing', action='store_true')
    parser.add_argument('--usecg', help='enable coingecko pricing', action='store_true')
    parser.add_argument('--usecustom', help='enable custom pricing', action='store_true')

    # arguments: utility arguments
    parser.add_argument('--cancelall', help='cancel all orders and exit', action='store_true')
    parser.add_argument('--cancelmarket', help='cancel all orders in market specified by pair --maker and --taker', action='store_true')
    
    # arguments: special arguments
    parser.add_argument('--imreallysurewhatimdoing', help='this argument allows you to specify meaningless configuration variables in special cases like you want to sell under actual price', action='store_true')
    
    args = parser.parse_args()

    # arguments: main maker/taker
    c.BOTsellmarket = args.maker.upper()
    c.BOTbuymarket = args.taker.upper()
    
    if c.BOTsellmarket in dxsettings.tradingaddress:
        c.BOTmakeraddress = dxsettings.tradingaddress[c.BOTsellmarket]
        
    if c.BOTbuymarket in dxsettings.tradingaddress:
        c.BOTtakeraddress = dxsettings.tradingaddress[c.BOTbuymarket]
    
    if args.makeraddress:
        c.BOTmakeraddress = args.makeraddress
        
    if args.takeraddress:
        c.BOTtakeraddress = args.takeraddress
    
    # arguments: basic values
    c.BOTsellrandom = args.sellrandom
    c.BOTsellstart = float(args.sellstart)
    c.BOTsellend = float(args.sellend)
    c.BOTsellmin = min(c.BOTsellstart, c.BOTsellend)
    c.BOTslidestart = float(args.slidestart)
    c.BOTslideend = float(args.slideend)
    c.BOTslidemin = min(c.BOTslidestart, c.BOTslideend)
    c.BOTslidemax = max(c.BOTslidestart, c.BOTslideend)
    c.BOTmaxopenorders = int(args.maxopen)
    c.BOTreopenfinished = int(args.reopenfinished)
        
    c.BOTbalancesavenumber = float(args.balancesavenumber)
    c.BOTbalancesavepercent = float(args.balancesavepercent)

    # arguments: dynamic values, special pump/dump order
    c.BOTslidedynpositive = float(args.slidedynpositive)
    c.BOTslidedynnegative = float(args.slidedynnegative)
    c.BOTslidedynzoneignore = float(args.slidedynzoneignore)
    c.BOTslidedynzonemax = float(args.slidedynzonemax)
    c.BOTslidepump = float(args.slidepump)
    c.BOTslidepumpenabled = (True if c.BOTslidepump > 0 else False)
    c.BOTpumpamount = (float(args.pumpamount) if float(args.pumpamount) > 0 else c.BOTsellend)
    
    # arguments: reset orders by events
    c.BOTresetonpricechangepositive = float(args.resetonpricechangepositive)
    c.BOTresetonpricechangenegative = float(args.resetonpricechangenegative)
    c.BOTresetafterdelay = int(args.resetafterdelay)
    c.BOTresetafterorderfinishnumber = int(args.resetafterorderfinishnumber)
    c.BOTresetafterorderfinishdelay = int(args.resetafterorderfinishdelay)
    
    # arguments: internal values changes
    c.BOTdelayinternal = int(args.delayinternal)
    c.BOTdelaycheckprice = int(args.delaycheckprice)
    
    # arguments: pricing source arguments
    if args.usecustom:
        c.BOTuse = 'custom'
    elif args.usecg:
        c.BOTuse = 'cg'
    elif args.usecb:
        c.BOTuse = 'cb'
    else:
        c.BOTuse = 'bt'
    
    # arguments: utility arguments
    c.cancelall = args.cancelall
    c.cancelmarket = args.cancelmarket
    
    # arguments: special arguments
    c.imreallysurewhatimdoing = args.imreallysurewhatimdoing
    
    load_config_verify_or_exit()
    
# global variables which have dependency on configuration be done
def global_vars_postconfig_init():
    global c, s, d
    print('>>>> Global variables post-configuration initialization')
    
    if c.BOTreopenfinished == 0:
        s.reopenstatuses = ['clear', 'expired', 'offline', 'canceled', 'invalid', 'rolled back', 'rollback failed']
    else:
        s.reopenstatuses = ['clear', 'expired', 'offline', 'canceled', 'invalid', 'rolled back', 'rollback failed', 'finished']
    
    s.ordersvirtualmax = c.BOTmaxopenorders + int(c.BOTslidepumpenabled) # pump and dump order is extra if exist
    d.ordersvirtual = [0]*s.ordersvirtualmax
    for i in range(s.ordersvirtualmax):
        d.ordersvirtual[i] = {}
        d.ordersvirtual[i]['status'] = 'canceled'
        d.ordersvirtual[i]['id'] = 0

# do utils and exit
def do_utils_and_exit():
    global c, s, d
    if c.cancelall:
        print('>>>> Utility to cancell all orders on all markets was specified and exit')
        results = dxbottools.cancelallorders()
        print(results)
        sys.exit(0)
    elif c.cancelmarket:
        print('>>>> Utility to cancell {0}-{1} orders was specified and exit'.format(c.BOTsellmarket, c.BOTbuymarket))
        results = dxbottools.cancelallordersbymarket(c.BOTsellmarket, c.BOTbuymarket)
        sys.exit(0)

# check if pricing works or exit        
def check_pricing_works_exit():
    global c, s, d
    print('>>>> Checking pricing information for {0} {1}'.format(c.BOTsellmarket, c.BOTbuymarket))
    
    if c.BOTsellmarket == c.BOTbuymarket:
        print('ERROR: Maker and taker asset cannot be the same')
        sys.exit(0)
        
    price_maker = update_pricing()
    if price_maker == 0:
        print('#### Pricing not available')
        sys.exit(1)

# try to update pricing information
def update_pricing():
    global c, s, d
    print('>>>> Updating pricing information for {0} {1}'.format(c.BOTsellmarket, c.BOTbuymarket))
    
    price_maker = pricebot.getpricedata(c.BOTsellmarket, c.BOTbuymarket, c.BOTuse)
    print('>>>> pricing information for {0} {1} previous {2} actual {3}'.format(c.BOTsellmarket, c.BOTbuymarket, d.price_maker, price_maker))
    if price_maker != 0:
        d.price_maker = price_maker
    
    return price_maker

def update_balances():
    global c, s, d
    balance_all = dxbottools.rpc_connection.dxGetTokenBalances()
    d.balance_maker_left = float(balance_all[c.BOTsellmarket])
    d.balance_taker = float(balance_all[c.BOTbuymarket])
    print('>>>> Actual balances: {} {} {} {}'.format(c.BOTsellmarket, d.balance_maker_left, c.BOTbuymarket, d.balance_taker))

# custom dynamic spread(slide) computation
def update_custom_dynamic_spread():
    global c, s, d
    print('>>>> Updating custom_dynamic_spread')
    
    # dynamic price slide == custom dynamic spread
    # integrate custom dynamic spread(slide)
    balance_taker_in_maker = (d.balance_taker / d.price_maker) #convert taker balance to by price
    balance_total = d.balance_maker_total + balance_taker_in_maker

    # custom_dynamic_spread_intensity number is min at 0 to max at 1 number
    # custom_dynamic_spread_intensity starting by 0 at "custom_dynamic_spread_ignore_zone",
    # groving up to 1 when reached "custom_dynamic_spread_max_zone"
    #
    # Theory about:
    #
    # if price of TAKER(TO BUY) is going up, opposite BOT is selling more and more,
    # so this BOT have more and more MAKER(TO SELL)
    # in this case you wanna buy TAKER by MAKER cheaper with smaller spread, but with possible market overturn expectations
    # for this case slidedynnegative argument is used
    #
    # if price of TAKER(TO BUY) is going down, opposite BOT is selling less and less,
    # also this BOT is buying more and more,
    # so this BOT have less and less MAKER(TO SELL)
    # for this case slidedynpositive argument is used
    # 
    # custom_dynamic_spread_intensity in general means how much intensity of
    # slidedynnegative or slidedynpositive to use,
    # computation of dynamic spread is than:
    # case 1 if price of TAKER(TO BUY) is going up = slidedynnegative * abs(custom_dynamic_spread_intensity)
    # case 2 if price of TAKER(TO BUY) is going down = slidedynpositive * custom_dynamic_spread_intensity
    #
    # final spread(slide) than is gonna be sum of this-dynamic-spread and spread
    
    if balance_total == 0:
        custom_dynamic_spread_intensity = 0
    else:
        custom_dynamic_spread_intensity = (balance_taker_in_maker - d.balance_maker_total) / (balance_total * c.BOTslidedynzonemax)
    
    custom_dynamic_spread_intensity = min(custom_dynamic_spread_intensity, 1)
    custom_dynamic_spread_intensity = max(custom_dynamic_spread_intensity, -1)
    
    if abs(custom_dynamic_spread_intensity) < c.BOTslidedynzoneignore:
        d.custom_dynamic_spread = 0
        print('>>>> Using custom_dynamic_spread {0} because custom_dynamic_spread_intensity {1} is in slidedynzoneignore {2}'.format(d.custom_dynamic_spread, custom_dynamic_spread_intensity, c.BOTslidedynzoneignore))
    elif custom_dynamic_spread_intensity > 0:
        d.custom_dynamic_spread = abs(custom_dynamic_spread_intensity) * c.BOTslidedynpositive
        print('>>>> Using custom_dynamic_spread {0} computed by custom_dynamic_spread_intensity {1} multiplied by slidedynpositive {2}'.format(d.custom_dynamic_spread, custom_dynamic_spread_intensity, c.BOTslidedynpositive))
    elif custom_dynamic_spread_intensity < 0:
        d.custom_dynamic_spread = abs(custom_dynamic_spread_intensity) * c.BOTslidedynnegative
        print('>>>> Using custom_dynamic_spread {0} computed by custom_dynamic_spread_intensity {1} multiplied by slidedynnegative {2}'.format(d.custom_dynamic_spread, custom_dynamic_spread_intensity, c.BOTslidedynnegative))
        
    print('>>>> custom_dynamic_spread updated {0}'.format(d.custom_dynamic_spread))
    return d.custom_dynamic_spread

# clear and wait for all virtual-orders and corresponding orders be cleared
def virtual_orders_clear():
    global c, s, d
    print('>>>> Clearing all session virtual orders and waiting for be done...')
    
    # mark all virtual orders as cleared
    for i in range(s.ordersvirtualmax):
        d.ordersvirtual[i]['status'] = 'clear'
    # loop while some orders are opened otherwise break while, do not cancel orders which are in progress
    while 1:
        clearing = int(0)
        ordersopen = dxbottools.getmyordersbymarket(c.BOTsellmarket,c.BOTbuymarket)
        # loop all previously opened virtual orders and try clearing opened
        for i in range(s.ordersvirtualmax):
            # try to find match between session and existing orders and clear it
            for z in ordersopen:
                # clear orders which are opened and match by id
                if z['status'] == "open" and z['id'] == d.ordersvirtual[i]['id']:
                    print('>>>> Clearing virtual order index <{0}> id <{1}> and waiting for be done...'.format(i, z['id']))
                    dxbottools.rpc_connection.dxCancelOrder(z['id'])
                    clearing += 1
        if clearing > 0:
            print('>>>> Sleeping waiting for old orders to be cleared')
            time.sleep(c.BOTdelayinternal)
        else:
            break
        
    # wait for orders which are in progress state (TODO)

def lookup_universal(lookup_data, lookup_name, lookup_id):
    # find my orders, returns order if orderid passed is inside myorders
    for zz in lookup_data:
        if zz[lookup_name] == lookup_id:
            return zz

def lookup_order_id_2(orderid, myorders):
    return lookup_universal(myorders, 'id', orderid)

# check all virtual-orders if there is some finished  
def virtual_orders_check_finished():
    global c, s, d
    print('>>>> Checking all session virtual orders how many orders finished and last time when order was finished...')
    
    ordersopen = dxbottools.getmyordersbymarket(c.BOTsellmarket,c.BOTbuymarket)
    for i in range(s.ordersvirtualmax):
        if d.ordersvirtual[i]['id'] != 0:
            # check how many virtual open orders finished
            order = lookup_order_id_2(d.ordersvirtual[i]['id'], ordersopen)
            print('>>>> Order <{0}> status original <{1}> to actual <{2}>'.format(d.ordersvirtual[i]['id'], d.ordersvirtual[i]['status'], (order['status'] if order else 'no status') ))
            
            # if previous status was not finished and now finished is, count this order as finished
            if d.ordersvirtual[i]['status'] != 'finished' and order and order['status'] == 'finished':
                d.ordersfinished += 1
                d.ordersfinishedtime = time.time()
            # update virtual order status
            if order:
                d.ordersvirtual[i]['status'] = order['status']
            else:
                d.ordersvirtual[i]['status'] = 'clear'
        
# create order and update also corresponding virtual-order
def virtual_orders_create_one(order_id, order_name, price, slide, stageredslide, dynslide, sell_amount):
    global c, s, d
    makermarketpriceslide = float(price) * (slide + stageredslide + dynslide)
    
    buyamount = (float(sell_amount) * float(makermarketpriceslide)) 
    buyamountclean = '%.6f' % buyamount
    
    print('>>>> Placing Order id <{0}> name <{1}> {2}->{3} at price {4} slide {5} staggered-slide {6} dynamic-slide {7} final-price {8} to sell {9} n buy {10}'
          .format(order_id, order_name, c.BOTsellmarket, c.BOTbuymarket, price, slide, stageredslide, dynslide, makermarketpriceslide, sell_amount, buyamountclean))
    
    try:
        results = {}
        results = dxbottools.makeorder(c.BOTsellmarket, str(sell_amount), c.BOTmakeraddress, c.BOTbuymarket, str(buyamountclean), c.BOTtakeraddress)
        print('>>>> Order placed - id: {0}, maker_size: {1}, taker_size: {2}'.format(results['id'], results['maker_size'], results['taker_size']))
        logging.info('Order placed - id: {0}, maker_size: {1}, taker_size: {2}'.format(results['id'], results['maker_size'], results['taker_size']))
    except Exception as err:
        print('ERROR: %s' % err)
    
    if results:
        d.ordersvirtual[order_id] = results

# recompute order tx fee (TODO)
def sell_amount_with_txfee_recompute(sell_amount):
    global c, s, d
    return sell_amount

# check if there is enough balance to create order
def balance_save_is_ok(sell_amount=0):
    global c, s, d
    
    sell_amount = sell_amount_with_txfee_recompute(sell_amount)
    
    #if BOTbalancesavenumber is set and already reached break and sleep and print
    if c.BOTbalancesavenumber != 0 and d.balance_maker_left <= (c.BOTbalancesavenumber + sell_amount):
        print('>>>> balancesavenumber {0} reached {1}/{2} , bot must wait for enough balance'.format(c.BOTbalancesavenumber, sell_amount + c.BOTbalancesavenumber, d.balance_maker_left))
        return False
    #if BOTbalancesavepercent is set and already reached sleep and print
    elif c.BOTbalancesavepercent != 0 and d.balance_maker_left <= ((c.BOTbalancesavepercent * d.balance_maker_total) + sell_amount):
        print('>>>> balancesavepercent {0} of total balance {1} reached {2}/{3} reached, bot must wait for enough balance'.format(c.BOTbalancesavepercent, d.balance_maker_total, ((c.BOTbalancesavepercent * d.balance_maker_total) + sell_amount), d.balance_maker_left))
        return False
    # if there is not enough balance to create order and pay fees sleep and print (TODO)
    elif d.balance_maker_left < sell_amount:
        print('>>>> There is not enough balance {0}/{1} to place order and pay fee, bot must wait for enough balance'.format(sell_amount, d.balance_maker_left))
        return False
    
    return True

# one time needed prepare process before switching into second internal loop 
def virtual_orders_prepare_once():
    global c, s, d
    update_balances()
    d.balance_maker_total = d.balance_maker_left
    
    while update_pricing() == 0:
        print('#### Pricing not available... waiting to restore...')
        time.sleep(c.BOTdelayinternal)
    
    d.reset_on_price_change_start = d.price_maker
    
    update_custom_dynamic_spread()
    
    # how many orders finished reset
    d.ordersfinished = 0
    
    d.time_start_reset_orders = time.time()
    d.ordersfinishedtime = 0
    
    d.time_start_update_pricing = time.time()

# every time main event loop pass, some dynamics should be recomputed
def virtual_orders_prepare_recheck():
    global c, s, d
    # every loop of creating or checking orders maker balance can be changed...
    update_balances()
    
    # every loop of creating or checking orders maker price can be changed...
    if c.BOTdelaycheckprice > 0 and (time.time() - d.time_start_update_pricing) > c.BOTdelaycheckprice:
        d.time_start_update_pricing = time.time()
        while update_pricing() == 0:
            print('#### Pricing not available... waiting to restore...')
            time.sleep(c.BOTdelayinternal)
    
    # get open orders, match them with virtual orders, and check how many finished
    virtual_orders_check_finished()

def events_exit_bot():
    global c, s, d
    
    print('checking for exit bot events')
    
    return False
    
def events_reset_orders():
    global c, s, d
    
    print('checking for reset order events')
    
    # if c.BOTresetonpricechangepositive is set and price has been changed, break and reset orders
    if c.BOTresetonpricechangepositive != 0 and d.price_maker >= (d.reset_on_price_change_start * (1 + c.BOTresetonpricechangepositive)):
        print('>>>> Reset on positive price change {0}% has been reached: price stored / actual {1} / {2}, going to order reset now...'.format(c.BOTresetonpricechangepositive, d.reset_on_price_change_start, d.price_maker))
        return True
        
    # if c.BOTresetonpricechangenegative is set and price has been changed, break and reset orders
    if c.BOTresetonpricechangenegative != 0 and d.price_maker <= (d.reset_on_price_change_start * (1 - c.BOTresetonpricechangenegative)):
        print('>>>> Reset on negative price change {0}% has been reached: price stored / actual {1} / {2}, going to order reset now...'.format(c.BOTresetonpricechangenegative, d.reset_on_price_change_start, d.price_maker))
        return True
    
    # if BOTresetafterdelay is set and reached break and reset orders
    if c.BOTresetafterdelay != 0 and (time.time() - d.time_start_reset_orders) > c.BOTresetafterdelay:
        print('>>>> Maximum orders lifetime {0} / {1} has been reached, going to order reset now...'.format((time.time() - d.time_start_reset_orders), c.BOTresetafterdelay))
        return True
        
    # if BOTresetafterorderfinishnumber is set and already reached break and reset orders
    if c.BOTresetafterorderfinishnumber != 0 and d.ordersfinished >= c.BOTresetafterorderfinishnumber:
        print('>>>> Maximum orders finished {0} / {1} has been reached, going to order reset...'.format(d.ordersfinished, c.BOTresetafterorderfinishnumber))
        return True
        
    #if BOTresetafterorderfinishdelay is set and already reached break and reset orders
    if c.BOTresetafterorderfinishdelay != 0 and d.ordersfinished != 0 and d.ordersfinishedtime != 0 and (time.time() - d.ordersfinishedtime) > c.BOTresetafterorderfinishdelay:
        print('>>>> Maximum orders lifetime {0} / {1} after order finished has been reached, going to order reset now...'.format((time.time() - d.ordersfinishedtime), c.BOTresetafterorderfinishdelay))
        return True
        
    return False
    
def events_wait():
    global c, s, d
    
    print('checking for wait events')
    
    # if there is NOT enough balance to place order and pay fee, do some sleep
    if balance_save_is_ok() == False:
        return True
        
    return False

def sell_amount_recompute(sell_start, sell_end, order_num_all, order_num_actual):
    global c, s, d
    
    sell_amount = float(0)
    
    if c.BOTsellrandom:
        # sell amount old style random
        sell_min = min(sell_start, sell_end)
        sell_max = max(sell_start, sell_end)
        if d.balance_maker_left < sell_max and d.balance_maker_left > sell_min:
            sell_max = d.balance_maker_left
        sell_amount = random.uniform(sell_min, sell_max)
    else:
        # compute staggered sell amount
        sell_amount = sell_start + (( (sell_end - sell_start) / max((order_num_all-1),1) )*order_num_actual)

    sell_amount = float('%.6f' % sell_amount)
    
    return sell_amount
    
def virtual_orders_handle():
    global c, s, d
    
    print('checking for virtual orders to handle')
    
    # loop all virtual orders and try to create em
    
    # staggered orders handling
    for i in range(s.ordersvirtualmax - int(c.BOTslidepumpenabled)):
        if d.ordersvirtual[i]['status'] in s.reopenstatuses:
            update_balances()
            
            sell_amount = sell_amount_recompute(c.BOTsellstart, c.BOTsellend, s.ordersvirtualmax - int(c.BOTslidepumpenabled), i)
                
            if balance_save_is_ok(sell_amount) == False:
                return
                
            # first order is min slide
            if i == 0:
                order_name = 'first staggered order with min-slide'
            # last order is max slide
            elif i == (s.ordersvirtualmax - int(c.BOTslidepumpenabled) -1):
                order_name = 'last staggered order with max-slide'
            # any other orders between min and max slide
            else:
                order_name = 'middle staggered order with computed-slide'
            
            # compute staggered orders slides
            staggeredslide = ((c.BOTslideend - c.BOTslidestart) / max((s.ordersvirtualmax -1 -int(c.BOTslidepumpenabled)),1 ))*i
            
            virtual_orders_create_one(i, order_name, d.price_maker, c.BOTslidestart, staggeredslide, d.custom_dynamic_spread, sell_amount)
            time.sleep(c.BOTdelayinternal)
    
    # special pump/dump order handling
    if c.BOTslidepumpenabled is True and d.ordersvirtual[s.ordersvirtualmax-1]['status'] in s.reopenstatuses:
        update_balances()
        if balance_save_is_ok(c.BOTpumpamount) == True:
            virtual_orders_create_one(s.ordersvirtualmax-1, 'pump/dump', d.price_maker, c.BOTslidemax, c.BOTslidepump, d.custom_dynamic_spread, c.BOTpumpamount)
            time.sleep(c.BOTdelayinternal)
            
# main function
if __name__ == '__main__':
    
    ####################################################################
    # following logic is about:
    # one time needed initialization 
    # one time needed checks
    ####################################################################
    
    start_welcome_message() # some welcome message
    
    global_vars_preconfig_init() # initialization of global variables which are needed by config load or does not need config to be loaded first
    
    load_config() # load configuration from config file if specified than load program arguments with higher priority by replacing config file options
    
    global_vars_postconfig_init() # initialization of global variables which depends on loaded configuration
    
    do_utils_and_exit() # if some utility are planned do them and exit program
    
    check_pricing_works_exit() # check if pricing works
    
    update_balances() # update balances information
    
    while 1:  # primary loop, starting point, after reset-orders-events
        
        ################################################################
        # following logic is about to wait for all session orders to be 
        # canceled and cleared
        ################################################################
        
        virtual_orders_clear()
        
        ################################################################
        # following logic is about to prepare for order placement by:
        # updating balances
        # update pricing
        # update custom dynamic parameters
        # reset counters
        # reset timers
        ################################################################
        
        virtual_orders_prepare_once()
        
        while 1: # secondary loop, starting point for handling events and orders
            
            ############################################################
            # following loop is about to:
            # staggered orders are created 
            # pump/dump order is created
            # finished orders are recreated if needed
            # orders reset on delay/afterfinish/afterfinishdelay...
            ############################################################
        
            virtual_orders_prepare_recheck() # every time main event loop pass, specific dynamic vars should be recomputed
            
            if events_exit_bot() == True: # check for events that forces bot to exit
                sys.exit(0)
            elif events_reset_orders() == True: # check for events that forces bot to reset orders
                break
            elif events_wait() == True: # check for events that forces bot to wait instead of placing orders
                pass
            else:
                virtual_orders_handle() # loop all virtual orders and try to re/create them
            
            time.sleep(c.BOTdelayinternal)
            
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
