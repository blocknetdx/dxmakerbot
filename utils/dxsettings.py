# REQUIRED
tradingaddress = {}
tradingaddress['SYS'] = '_address_'
tradingaddress['LTC'] = '_address_'
tradingaddress['BLOCK'] = '_address_' 
tradingaddress['MUE'] = '_address_'
rpcport = 41414
rpcuser = '_rpcuser_'
rpcpassword = '_rpcpassword_'
cryptobridgeURL = 'https://api.crypto-bridge.org/api/v1/ticker' # required if using the --usecb flag


# Custom price settings:
#	- Required if using the --usecustom flag.
#	- The custom price option lets you use custom price sources. This is useful for:
#		- Trading uncommon market pairs that do not exist on exchanges
#		- Trading market pairs where both assets are not supported by another pricing flags (--usecg, --usecb, etc)
#	- Custom price source endpoints must return BTC price or use custom functions (see next)
#		- The function getprice() in utils/custompricing.py expects only a value to be returned 
#			(eg. 0.0150147175974065 or 4.03393625609417E-6)
#	- If the price source returns json: 
#		- Create a custom exception in getprice() in utils/custompricing.py, use existing customrequest1 as guide
apiendpoint = {}
apiendpoint['BTC'] = '1' # pricing in BTC, endpoint not needed
apiendpoint['SYS'] = 'https://chainz.cryptoid.info/sys/api.dws?q=ticker.btc'
apiendpoint['LTC'] = 'https://api.cryptonator.com/api/full/ltc-btc'
apiendpoint['BLOCK'] = '_url_'
apiendpoint['MUE'] = '_url_'

customrequest1 = ['LTC']
customrequest2 = ['_asset1_', '_asset2_']
customrequest3 = ['_asset3_', '_asset4_']

