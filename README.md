# DX Maker Bot
A market making bot for Blocknet's decentralized exchange protocol, built with the [XBridge API](https://api.blocknet.co).

* [Prerequisites](#prerequisites)
* [Installation](#installation)
	* [Linux](#linux)
	* [Windows](#windows)
* [Configuration](#configuration)
	* [Custom Pricing](#custom-pricing)
* [Running the Bot](#running-the-bot)
	* [Maker Bot](#maker-bot-usage)

[Website](https://blocknet.co) | [Blocknet API](https://api.blocknet.co) | [Blocknet Docs](https://docs.blocknet.co) | [Discord](https://discord.gg/2e6s7H8)
-------------|-------------|-------------|-------------


## Prerequisites
1. [Latest Blocknet wallet installed](https://github.com/blocknetdx/blocknet/releases/latest).
1. The wallet of any assets you will be trading. See list of [compatible assets](https://docs.blocknet.co/protocol/xbridge/compatibility/#supported-digital-assets).
1. The Blocknet wallet and any other wallet you're trading out of must but fully synced and fully unlocked.
1. The wallets used for trading must be configured. For simple setup, use [Block DX's automated configuration setup wizard](https://docs.blocknet.co/blockdx/configuration/). Having Block DX installed and opened is also useful to visually monitor the market and your open orders.
1. Make sure funds are split into multiple UTXOs. If you have an order for 1 LTC and you only have a single 10 LTC input, all 10 LTC will be locked in this order. Having multiple, preferably smaller, UTXOs will allow a better distribution of funds across orders.
1. Make sure funds are in legacy addresses (Eg. LTC funds should be in a "L" address).



## Installation

#### Linux
1. Open the command line terminal to enter the following commands
1. Install Python 3: ```apt-get install python3```
	* Or upgrade Python 3: ```apt-get upgrade python3```
1. Install pip (Python's package manager): ```apt-get install python3-pip```
	* Or upgrade pip: ```apt-get upgrade python3-pip```
1. Download DX Maker Bot
	* Download via Git: 
		1. Navigate to your project directory
			* Example: ```cd ~/projects/```
		1. Download DX Maker Bot: ```git clone https://github.com/blocknetdx/dxmakerbot```
	* Download via Github:
		1. Navigate to [https://github.com/blocknetdx/dxmakerbot](https://github.com/blocknetdx/dxmakerbot)
		1. Click the green *Clone or download* button and select *Download ZIP* from the dropdown
		1. Save the file and (if necessary) extract the contents to a folder
1. Navigate into the *dxmakerbot* folder
	* Example: ```cd ~/projects/dxmakerbot```
1. Install the required DX Maket Bot packages: ```pip3 install -r requirements.txt```
	* If that command does not work: ```pip install -r requirements.txt```

#### MacOS
1. Open Terminal to enter the following commands
1. Install XCode: ```xcode-select --install```
1. Install Homebrew (MacOS package manager): ```/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"```
1. Install Python 3: ```brew install python3```
1. Upgrade pip (Python's package manager): ```pip3 install -U pip```
1. Download DX Maker Bot
	* Download via Git: 
		1. Navigate to your project directory
			* Example: ```cd ~/Documents/projects/```
		1. Download DX Maker Bot: ```git clone https://github.com/blocknetdx/dxmakerbot```
	* Download via Github:
		1. Navigate to [https://github.com/blocknetdx/dxmakerbot](https://github.com/blocknetdx/dxmakerbot)
		1. Click the green *Clone or download* button and select *Download ZIP* from the dropdown
		1. Save the file and (if necessary) extract the contents to a folder
1. Navigate into the *dxmakerbot* folder
	* Example: ```cd ~/Documents/dxmakerbot```
1. Install the required DX Maket Bot packages: ```pip3 install -r requirements.txt```

#### Windows
1. Install Python 3:
	1. Navigate to [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/) and select *Download Python 3.7.x*
	1. Run the installer
	1. Check off *Add Python 3.7 to PATH*
	1. Click *Install Now*
1. Right-click the taskbar *Start* menu and select *Command Prompt (Admin)*
1. Upgrade pip (Python's package manager): ```py -m pip install --upgrade pip```
1. Download DX Maker Bot
	* Download via Git: 
		1. Navigate to your project directory
			* Example: ```cd ~/projects/```
		1. Download DX Maker Bot: ```git clone https://github.com/blocknetdx/dxmakerbot```
	* Download via Github:
		1. Navigate to [https://github.com/blocknetdx/dxmakerbot](https://github.com/blocknetdx/dxmakerbot)
		1. Click the green *Clone or download* button and select *Download ZIP* from the dropdown
		1. Save the file and (if necessary) extract the contents to a folder
1. Navigate into the *dxmakerbot* folder
	* Example: ```cd C:\Users\%USERNAME%\Downloads\dxmakerbot```
1. Install the required DX Maket Bot packages: ```pip3 install -r requirements.txt```
	* If that command does not work: ```pip install -r requirements.txt```



## Configuration
1. Open `dxmakerbot/utils/dxsettings.py`.
1. Edit the trading addresses to match the wallet addresses containing funds split into multiple UTXOs.
	* Make sure funds are in legacy addresses (Eg. LTC funds should be in a "L" address).
1. Edit `rpcuser =`, `rpcpassword =`, and `rpcport =` to the same values used in the Blocknet client's `blocknet.conf` file.
1. Save and close the file. 

Example `dxsettings.py` file:

```
tradingaddress = {}
tradingaddress['SYS'] = "SbaRDo3taq1zmAba2Ak54fRxAz8Z9rkyPw"
tradingaddress['LTC'] = "LZdTPLFqQzxuoSfyRioUSMyPvlsrnpGVWR"
tradingaddress['BLOCK'] = "B2cBqpuEXu4tVS5prBd5zyeqvBTSi6g398"
tradingaddress['DGB'] = "D3F4pdn7CGZ4kxFUvdMbflyJ8cRqfwsurj"
rpcport = 41414
rpcuser = 'blocknetbot'
rpcpassword = 'blocknetbot123'
```

### Custom Pricing
The bot supports pricing from Bittrex, CryptoBridge, CoinGecko, or custom price sources. If using custom price sources:
1. Add a price source to be used for each asset that will be traded.
	* Example: `apiendpoint['__asset__'] = '_url_'`
1. Custom price source endpoints must return BTC price.
	* The default function `getprice()` in `utils/custompricing.py` expects only a value to be returned.
		* Example: *0.0150147175974065* or *4.03393625609417E-6*
1. If the price source returns json: 
	* Add the asset to one of the existing custom request lists or create a new one.
		* Example: `customrequest1 = ['_asset1_', '_asset2_']`
		* Each list will use a different custom exception to target the json (see next).
	* Create a custom exception in `getprice()` in `utils/custompricing.py`, using existing *customrequest1* as guide.

Example custom price settings:
```
apiendpoint = {}
apiendpoint['SYS'] = 'https://chainz.cryptoid.info/sys/api.dws?q=ticker.btc'
apiendpoint['BLOCK'] = 'https://chainz.cryptoid.info/block/api.dws?q=ticker.btc'
apiendpoint['LTC'] = 'https://chainz.cryptoid.info/ltc/api.dws?q=ticker.btc'
apiendpoint['MUE'] = 'https://api.cryptonator.com/api/full/mue-btc'

customrequest1 = ['MUE']
customrequest2 = []
customrequest3 = []
```



## Running the Bot
1. Run the wallets of any assets being traded (fully synced, unlocked).
1. Run the Blocknet wallet (fully synced, unlocked).
1. *Optional*: Run [Block DX](https://docs.blocknet.co/blockdx/setup) for visual reference that the bot is working.
	* At this stage it would be a good idea to test making/taking an order without using the bot to ensure everything is setup properly.
1. Navigate to the *dxmakerbot* directory in the terminal.

### Common Maker Bot Usage
* Pricing is based off BTC-XXX market pairs. For example, if running on the LTC-DASH market, the bot pulls the price for BTC-LTC and BTC-DASH then automatically calculates LTC-DASH price. This is how it works for all supported pricing sources:
	* Bittrex: default (no flag)
	* CryptoBridge: `--usecb`
	* CoinGecko: `--usecg`
	* Custom pricing: `--usecustom`

### Maker Bot Usage By Version:
* [Maker Bot Usage Version V1](#maker-bot-usage-version-v1)
* [Maker Bot Usage Version V2](#maker-bot-usage-version-v2)

### Maker Bot Usage Version V1

Use the following command format to start the bot:
```
python3 dxmakerbot.py --maker [] --taker [] --sellmin [] --sellmax [] --slidemin [] --slidemax []
```

Flag            | Default       | Description
----------------|---------------|------------
--maker         | BLOCK         | Asset being sold
--taker         | LTC           | Asset being bought
--sellmin       | 0.001         | Min maker sell order size
--sellmax       | 1             | Max maker sell order size
--slidemin      | 1.000001      | Min order price multiplier: Min order price = slidemin * price source quote
--slidemax      | 1.019999      | Max order price multiplier: Min order price = slidemax * price source quote
--delay         | 3             | Sleep delay between loops to place/cancel orders (seconds)
--maxloop       | 7             | Number of loops before canceling the oldest order
--maxopen       | 5             | Max amount of orders to have open at any given time
--minbalance    | 10            | Min balance you want to maintain of the asset being sold
--usecb*        | *disabled*    | Use CryptoBridge prices (both assets must be listed on CryptoBridge)
--usecg*        | *disabled*    | Use CoinGecko prices (both assets must be listed on CoinGecko)
--usecustom*    | *disabled*    | Use custom price sources from *utils/dxsettings.py*
--cancelall*    |               | Cancel all orders and exit program
--cancelmarket* |               | Cancel all orders in a given market

`*` = optional

Example command:
```
python3 dxmakerbot.py --maker SYS --taker LTC --sellmin 5 --sellmax 115 --slidemin 1.00111 --slidemax 1.1111 --usecustom
```

### Maker Bot Usage Version V2

### Use the following command to learn more about dxmakerbot version 2 usage
```
python3 dxmakerbot_v2.py -h
```

### main configuration arguments
-----------------------------
Flag            | Description
----------------|------------
--maker         | asset being sold (default=BLOCK)
--taker         | asset being bought (default=LTC)
--makeraddress  | trading address of asset being sold (default=None)
--takeraddress  | trading address of asset being bought (default=None)

### basic configuration arguments
-----------------------------------
Flag                  | Description
----------------------|------------
--sellstart           | size of first order or random from range sellstart and sellend (default=0.001)
--sellstartmin        | minimum acceptable size of first order. If this is configured and there is not enough balance to create first order at <sellstart> size, order will be created at maximum possible size between <sellstart> and <sellstartmin>. (default=0 disabled)
--sellend             | size of last order or random from range sellstart and sellend  (default=0.001)
--sellendmin          | minimum acceptable size of last order. If this is configured and there is not enough balance to create last order at <sellend> size, order will be created at maximum possible size between <sellend> and <sellendmin>. (default=0 disabled)
--sellrandom          | orders size will be random number between sellstart and sellend, otherwise orders size sequence starting by sellstart amount and ending with sellend amount
--slidestart          | price of first order will be equal to slidestart * price source quote(default=1.01 means +1%)
--slideend            | price of last order will be equal to slideend * price source quote(default=1.021 means +2.1%)
--maxopen             | Max amount of orders to have open at any given time. Placing orders sequence: first placed order is at slidestart(price slide),sellstart(amount) up to slideend(price slide),sellend(amount), last order placed is slidepump if configured, is not counted into this number (default=5)
--reopenfinishednum   | reopen finished orders after specific number of filled orders(default=0 means disabled)
--reopenfinisheddelay | reopen finished orders after specific delay of last filled order(default=0 means disabled)
--balancesavenumber   | min taker balance you want to save and do not use for making orders specified by number (default=0)
--balancesavepercent  | min taker balance you want to save and do not use for making orders specified by percent of maker+taker balance (default=0.05 means 5%)

### takerbot configuration arguments
----------------------------------
Flag                 | Description
---------------------|------------
--takerbot           | keep checking for possible partial orders which meets requirements(size, price) and accept that orders.(default=0 disabled) For more details please read dxmakerbot --help

### advanced configuration arguments - dynamic values, special pump/dump order
----------------------------------
Flag                 | Description
---------------------|------------
--slidedyntype       | maker*price:taker ratio when dynamic slide intensity is 0. Or static value in maker when dynamic slide intensity is 0 (default=ratio). For more details please read dxmakerbot --help
--slidedynzero       | specify when dynamic slide intensity is 0%. For more details please read dxmakerbot --help
--slidedynpositive   | dynamic price slide increase positive, applied if maker price goes up, range between 0 and slidedynpositive, dynamically computed by assets ratio (default=0, 0.5 means maximum at +50% of price)
--slidedynnegative   | dynamic price slide increase negative, applied if maker price goes down, range between 0 and slidedynnegative, dynamically computed by assets ratio (default=0, 0.1 means maximum at +10% of price)
--slidedynzoneignore | dynamic price slide increase ignore is zone when dynamic slide is not activated(default=0.05 means 5% of balance)
--slidedynzonemax    | percentage when dynamic order price slide increase gonna reach maximum(default=0.9 means at 90%)
--slidepump          | if slide pump is non zero a special order out of slidemax is set, this order will be filled when pump happen(default=0, 0.5 means order will be placed +50% out of maximum slide)
--pumpamount         | pump order size, otherwise sellend is used(default=--sellend)

### boundary limits, exit/wait cancel/nocancel orders configuration arguments
-------------------------------------
Flag                    | Description
------------------------|------------
--boundary_asset_maker  | boundary measurement asset, for example BTC (default= --maker)', default=None)
--boundary_asset_taker  | boundary measurement asset, for example asset_maker is BTC and boundary_asset_taker is USDT, so boundary min max can be 5000-9000 (default= --taker)
--boundary_max_relative | maximum acceptable price of maker payed by taker which bot will work with, price is relative to price when bot started,i.e.: Start price:100, config value:3, so bot will work up to 100*3 = 300 price, (default=0 disabled)
--boundary_min_relative | minimum acceptable price of maker payed by taker which bot will work with, price is relative to price when bot started,i.e.: Start price:100, config value:0.8, so bot will sell at least for 100*0.8 = 80 price, (default=0 disabled)
--boundary_max_static   | maximum acceptable price which bot will work with(default=0 disabled)
--boundary_min_static   | minimum acceptable price which bot will work with(default=0 disabled)
--boundary_max_nocancel | do not cancel orders, default is to cancel orders (default cancel orders)
--boundary_max_noexit   | wait instead of exit program, default is to exit program (default exit bot)
--boundary_min_nocancel | do not cancel orders, default is to cancel orders (default cancel orders)
--boundary_min_noexit   | wait instead of exit program, default is to exit program (default exit bot)

### reset orders configuration arguments
-------------------------------------------
Flag                          | Description
------------------------------|------------
--resetonpricechangepositive  | percentual price positive change(you can buy more) when reset all orders (default=0, 0.05 means reset at +5% change)
--resetonpricechangenegative  | percentual price negative change(you can buy less) when reset all orders (default=0, 0.05 means reset at -5% change)
--resetafterdelay             | delay before resetting all orders in seconds (default=0 means disabled)
--resetafterorderfinishnumber | number of orders to be finished before resetting orders (default=0 means not set)
--resetafterorderfinishdelay  | delay after finishing last order before resetting orders in seconds (default=0 not set)

### internal configuration aguments
-------------------------------
Flag              | Description
------------------|------------
--delayinternal      | sleep delay, in seconds, between place/cancel orders or other internal operations(can be used ie. case of bad internet connection...) (default=2.3)
--delayinternalerror | sleep delay, in seconds, when error happen to try again. (default=10)
--delayinternalcycle | sleep delay, in seconds, between main loops to process all things to handle. (default=8)
--delaycheckprice    | sleep delay, in seconds to check again pricing (default=180)

### pricing source configuration arguments
-----------------------------------------
Flag        | Default       | Description
------------|---------------|------------
--usecb     | *disabled*    | enable cryptobridge pricing
--usecg     | *disabled*    | enable coingecko pricing
--usecustom | *disabled*    | enable custom pricing

### utility arguments
-----------------------------------------
Flag           | Description
---------------|-------------------------
--cancelall    | Cancel all orders and exit program
--cancelmarket | Cancel all orders in a given market

`*` = optional

### Example situation no. 1 and corresponding command:
- Let say, user is running Blocknet wallet with address blck0123456789blck and all his staked and masternode rewards coins go to this address.
- Let say, user want to automatically sell all staked Blocknet coins for Litecoin which wallet is using address lite0123456789lite.
- So user uses dxmakerbor config like this:
```
--maker BLOCK --makeraddress blck0123456789blck --taker LTC --takeraddress lite0123456789lite
```

- Let say, most effective to sell Blocknet is at minimum amount of 10 block because of high fees on Litecoin. So bot needs to be configured to open orders of minimum at 10 Blocknet coins.
- Let say, user know that time to time blocknet price goes about 22% up and down and he wants to cover whole pricing by using staggered orders.
- Let say, user also wants to staggered orders been in valley mode, means placing small orders with 10BLOCK nearest to center-price at +3% up to last order at 100BLOCK at +22%
- Let say, user wants always place higher orders first for the case of insufficient funds.
- So used uses dxmakerbot config like this:
```
--sellstart 100 --sellend 10 --slidestart 1.22 --slideend 1.03
```

- Let say, user wants to have opened maximum 5 orders between that 22% and 3%
```
--maxopen 5
```

- Let say, user know that price time to time goes to pump at +40% so he wants to cover that case by one order at +38%
```
--slidepump 0.38
```

- Let say, user rather wait for 2 staggered orders to be finished than reopen low price one order
- Let say, but if not multiple orders will finish at time of 10 minutes, all orders goes to reset
```
--reopenfinishednum 0 --resetafterorderfinishnumber 2 --resetafterorderfinishdelay 600
```

- Let say, user always wants to have some little 2 blocknets save on his wallet
```
--balancesavenumber 2 --balancesavepercent 0
```

- Let say, user always wants to check of price changes and reset all orders at +3% of price change.
- But if price goes down, he knows its only correction, and price downtrend must be followed by at least 8% dump.
```
--resetonpricechangepositive 0.03 --resetonpricechangenegative 0.08
```

- Let say, user is running multiple bots and have low internet connection, so he decide to give all internal operation time 15 seconds
```
--delayinternal 15
```

- Let say, rechecking price source very often will cause client dxmakerbot been banned for a few minutes, so user decide to check price only once per 2 minutes
```
--delaycheckprice 120
```

Corresponding command for example situation no. 1:
```
python3 dxmakerbot_v2.py --maker BLOCK --makeraddress blck0123456789blck --taker LTC --takeraddress lite0123456789lite --sellstart 100 --sellend 10 --slidestart 1.22 --slideend 1.03 --maxopen 5 --reopenfinishednum 0 --balancesavenumber 2 --balancesavepercent 0 --slidedynpositive 0.0 --slidedynnegative 0.0 --slidedynzoneignore 0.05 --slidedynzonemax 0.9 --slidepump 0.38 --resetonpricechangepositive 0.03 --resetonpricechangenegative 0.08 --resetafterdelay 0 --resetafterorderfinishnumber 2 --resetafterorderfinishdelay 600 --delayinternal 15 --delaycheckprice 120
```

