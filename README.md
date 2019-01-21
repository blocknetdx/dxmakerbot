# dxbot tools
- example python3 code for placing an order and canceling an order on BlockDX

# env setup
- Install required pip3 packages
- pip3 install -r requirements.txt

# Configuration
- Editing utils/dxsettings.py with block and ltc trading addresses, and blocknetdx RPC creds

# Example
```dxmakerbot.py --maker SYS --taker LTC --sellmin 5 --sellmax 15 --slidemin 1.00111 --slidemax 1.1111```
