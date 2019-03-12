# dxmaker bot
- python3 maker bot for blocknets DX

# env setup
- linux: ```apt-get install python3 python3-pip```
- Install required pip3 packages
- ```pip3 install -r requirements.txt```

# Configuration
- Editing utils/dxsettings.py with block and ltc trading addresses, and blocknetdx RPC creds

# Example
```dxmakerbot.py --maker SYS --taker LTC --sellmin 5 --sellmax 15 --slidemin 1.00111 --slidemax 1.1111```
