#!/usr/bin/env python3

import subprocess

# ~ MIT License

# ~ Copyright (c) 2020 FAZER

# ~ Permission is hereby granted, free of charge, to any person obtaining a copy
# ~ of this software and associated documentation files (the "Software"), to deal
# ~ in the Software without restriction, including without limitation the rights
# ~ to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# ~ copies of the Software, and to permit persons to whom the Software is
# ~ furnished to do so, subject to the following conditions:

# ~ The above copyright notice and this permission notice shall be included in all
# ~ copies or substantial portions of the Software.

# ~ THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# ~ IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# ~ FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# ~ AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# ~ LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# ~ OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# ~ SOFTWARE.


botconfig = str(
#bot is configured to sell(maker) Blocknet for Litecoin
    "--maker BLOCK"
    "--taker LTC"

#your addresses
    "--makeraddress blocknet_addr_is_missing_here"
    "--takeraddress litecoin_addr_is_missing_here"

#do not save any maker balance
    "--balancesavenumber 0 --balancesavepercent 0"
  
#bot will try to create orders with dynamic size if there is no balance available to create order at maximum. but only between <value, min value>
#also takerbot is accepting at least order with size in range between <value, min value>
    #first placed order at maker size min 15 up to max 100 by available balance
        "--sellstart 100.0 --sellstartmin 15.0"
    #last placed order at maker size min 15 up to max 50 by available balance
        "--sellend 50.0 --sellendmin 15.0"

#configure bot to have 3 orders opened.
#all other orders between first and last order are automatically recomputed by number of orders and linearly distributed between <sellstart, sellstartmin> and <sellend, sellendmin>
#so if bot have order size from <1> up to <6> and max number of orders is 3 middle will be 3.5, so orders will be <1> <3.5> <6>
    "--maxopen 3"
   
#first order at price slide to 104%(if price is 1 USD final is 1.04 USD), second order with price slide 102% and last order with price slide to 101%
    "--slidestart 1.03 --slideend 1.01"

#no pump order. pump and dump orders are very useful, in case of pump you can buy back more and cheap.
    "--slidepump 0 --pumpamount 0 --pumpamountmin 0"

#enabled dynamic slide based on maker amount. Dynamic slide -1 means autoconfigured to value 0 at bot start with actual amount when bot started
    "--slidedyntype static --slidedynzero -1"
    #dynamic slide is ignored(not applied) when maker balance change -+0.2%. dynamic slide will reach max at +-80%
        "--slidedynzoneignore 0.02 --slidedynzonemax 0.8"
    #in case when selling more and more maker than opposite bot(if any), so balance of maker is less and less, means interest for maker is more and more, so prediction of maker price is will go up.
    #so order price can be increated more and more, so final price of last order can possibly reach value = price*(1.01+0.20)
        "--slidedynpositive 0.20"
    #in case when selling less and less maker than opposite bot(if any), so balance of maker is more and more, means interest for maker is less and less, so prediction of maker price is will go down.
    #handling #1 if this situation is, bot can be configured as expectation that price will go back. so bot will increase price in spite of interest of maker is going down.
        "--slidedynnegative 0.15"
    #handling #2 of this situation is, bot can be configured to slightly decrease final price of maker order.
        # ~ "--slidedynnegative -0.01 --imreallysurewhatimdoing"

#recreate order when 2 orders are accepted
    "--reopenfinishednum 2"
#recreate orders by 600seconds timeout of last taken/accepted order
    "--reopenfinisheddelay 600"

#reset all orders on positive +0.1% price change, but on negative price change, reset only when will reach -0.5% price change
    "--resetonpricechangepositive 0.01 --resetonpricechangenegative 0.05"

#do not reset all orders at timer, reset all orders when 3 orders are taken/accepted, do not reset orders on timer when some order is accepted
    "--resetafterdelay 0 --resetafterorderfinishnumber 3 --resetafterorderfinishdelay 0"
   
#set maxium and minimum bot price boundary at 105% and 95% of price when bot was started
    "--boundary_max_relative 1.05 --boundary_min_relative 0.95"
    #do not exit bot when boundary reached, cancel orders on max boundary, do not cancel orders on min boundary
        "--boundary_max_noexit --boundary_min_noexit --boundary_min_nocancel"

#alternative boundary configuration, set maximum and minimum bot price boundary at static values relative to bitcoin
    # ~ "--boundary_asset_taker BTC"
    # ~ "--boundary_max_static 0.00020015 --boundary_min_static 0.00013715"

#takerbot act like limit orders on your actually created orders, its also taking whole range of dynamic size and multiple orders
    #enabled takerbot feature to check orders to take on 10 second interval
        "--takerbot 10"
   
#delay between internal operations 2.3s
    "--delayinternal 2.3"
#check price every 60 seconds
    "--delaycheckprice 60"
#sleep delay, in seconds, when error happen to try again. (default=10)
    "--delayinternalerror 10"
#sleep delay, in seconds, between main loops to process all things to handle
    "--delayinternalcycle 8"

)

botconfig = botconfig.replace(" --", "--")
botconfig = botconfig.replace("--", " --")

subprocess.run("python3 dxmakerbot_v2.py" + botconfig, shell=True)
