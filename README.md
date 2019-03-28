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
1. [Latest Blocknet wallet installed](https://github.com/BlocknetDX/blocknet/releases/latest).
1. The wallet of any assets you will be trading. See list of [compatible assets](https://docs.blocknet.co/protocol/xbridge/compatibility/#supported-digital-assets).
1. The Blocknet wallet and any other wallet you're trading out of must but fully synced and fully unlocked.
1. The wallets used for trading must be configured. For simple setup, use [Block DX's automated configuration setup wizard](https://docs.blocknet.co/blockdx/configuration/). Having Block DX installed and opened is also useful to visually monitor the market and your open orders.
1. Funds are split into multiple UTXOs. If you have an order for 1 LTC and you only have a single 10 LTC input, all 10 LTC will be locked in this order. Having multiple, preferably smaller, UTXOs will allow a better distribution of funds across orders.
1. Make sure funds are in legacy addresses (Eg. LTC funds should be in a "L" address).



## Installation

#### Linux
1. Install Python 3: ```apt-get install python3```
	* Or update Python 3: ```apt-get upgrade python3```
1. Install pip:```apt-get install python3-pip```
	* Or update pip: ```apt-get upgrade python3-pip```
1. Navigate to your project directory.
1. Download DX Maker Bot: ```git clone https://github.com/BlocknetDX/dxmakerbot```
1. Navigate into *dxmakerbot*: ```cd dxmakerbot```
1. Install required DX Maket Bot packages: ```pip3 install -r requirements.txt```

#### Windows
1. Install Python 3:
	1. Navigate to [https://www.python.org/downloads/](https://www.python.org/downloads/) and select *Download Python 3.7.x*.
	1. Run the installer.
	1. Check off *Add Python 3.7 to PATH*.
	1. Click *Install Now*.
1. Download DX Maker Bot:
	1. Navigate to [https://github.com/BlocknetDX/dxmakerbot](https://github.com/BlocknetDX/dxmakerbot).
	1. Click the green *Clone or download* button and select *Download ZIP* from the dropdown.
	1. Save the file and extract the contents to a folder.
1. Right-click the taskbar *Start* menu and select *Command Prompt (Admin)*.
1. Update pip: ```py -m pip install --upgrade pip```
1. Navigate into *dxmakerbot*: ```cd C:\Users\%USERNAME%\Downloads\dxmakerbot```
1. Install required DX Maket Bot packages: ```pip3 install -r requirements.txt```



## Configuration
1. Open `dxmakerbot/utils/dxsettings.py`.
1. Edit the trading addresses to match the wallet addresses containing funds split into multiple UTXOs.
	* Make sure funds are in legacy addresses (Eg. LTC funds should be in a "L" address).
1. Edit `rpcuser =`, `rpcpassword =`, and `rpcport =` to the same values used in the Blocknet client's `blocknetdx.conf` file.
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

### Maker Bot Usage
* Pricing is based off BTC-XXX market pairs. For example, if running on the LTC-DASH market, the bot pulls the price for BTC-LTC and BTC-DASH then automatically calculates LTC-DASH price. This is how it works for all supported pricing sources:
	* Bittrex: default (no flag)
	* CryptoBridge: `--usecb`
	* CoinGecko: `--usecg`
	* Custom pricing: `--usecustom`

Use the following command format to start the bot:
```
python3 dxmakerbot.py --maker [] --taker [] --sellmin [] --sellmax [] --slidemin [] --slidemax []
```

Flag 			| Default 		| Description
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
