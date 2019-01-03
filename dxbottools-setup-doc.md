**This guide will follow a Windows installation of the DXBot Tool coded by Dan (atcsecure):**

**PREREQUISITES:**

* Make sure funds are split into multiple UTXO's

* Make sure funds are in legacy addresses (Eg. LTC funds should be in a "L" address)
---
# Python Installation

* Install latest Python

	* Navigate to [https://www.python.org/downloads/](https://www.python.org/downloads/) >> Download the latest Python (3.7.1 was latest)
	* Run the installer
	* Check off 'Add Python 3.7 to PATH'
	* Click 'Install Now'

* Ensure pip3 is working

	* Open Command Prompt >> Type `pip3` (if it worked you should see `pip3 <commands> [options]` and the options below it)

* Check/Update pip version

	* Open Command Prompt >> Type: `py -m pip install --upgrade pip`
---
# DXBot Tool Installation

* Download DXBot Tool

	* Navigate to: [https://github.com/atcsecure/dxbottools](https://github.com/atcsecure/dxbottools)
	* Click the green 'Clone or download' button >> Hit 'Download ZIP'
	* Save the file >> Extract contents to a folder

* Install the required DXBot pip3 packages

	* Open Command Prompt
	* Navigate to the DXBot directory (Eg. `cd c:\dxbot`)
	* Once in the DXBot directory type `pip3 install -r requirements.txt` and let the packages install
---
# Configure Local Settings for DXBot

* Edit `dxsettings.py`

	* Navigate to the DXBot directory >> Open the 'utils' folder
	* Right-click `dxsettings.py` >> 'Edit with IDLE'
	* Edit trading addresses to match the wallet addresses containing funds split into multiple UTXO's 
	* Change `rpcuser =` and `rpcpass =` to rpc user/pass in the Blocknet client `blocknetdx.conf`
	* Leave `rpcport =` to the default 41414, or change it to suit local settings 
	* Save >> Exit
	* Eg:
	```
	tradingaddress = {}
	tradingaddress['SYS'] = "SbaRDT3taq1zmAba2Ak54fRxAR8Z9rkyPw"
	tradingaddress['LTC'] = "LZdTPLFpQzxuoSfyRmoUSMyPvssrnpGVWR"
	tradingaddress['BLOCK'] = "BmcBqpuEXu4tVS5krBd5zyeqvBTSi6g338"
	rpcport = 41414
	rpcuser = 'blocknetbot'
	rpcpassword = 'blocknetbot123'
	```
---
# Running the DXBot

* Run trading wallets (fully synced, unlocked)
* Run BlocknetDX client (fully synced, unlocked)
* Optional: Run Block DX UI (visual reference that the bot is working)
	* At this stage it would be a good idea to test making/taking an order without using the bot to ensure everything is setup properly

* Open Command Prompt >> Navigate to you DXBot directory
* Type: `dxmakerbot.py` to run the default BLOCK/LTC pairing (if the bot isn't setup for BLOCK/LTC; see next step)
	
* At the moment this bot supports pairing of all Bittrex tradable coins supported on Blocknet 
	* `dxmakerbot.py --maker [] --taker [] --sellmin [] --sellmax [] --slidemin [] --slidemax []`
	* `--maker` = asset being sold
	* `--taker` = asset being bought
	* `--sellmin` = minimum amount to sell
	* `--sellmax` = maximum amount to sell
	* `--slidemin` = minimum slide value 
	* `--slidemax` = maximum slide value
		 
	* Eg. SYS/LTC pairing
		* `dxmakerbot.py --maker SYS --taker LTC --sellmin 5 --sellmax 15 --slidemin 1.00111 --slidemax 1.1111` 
