#!/usr/bin/env python3
import requests
from utils import dxsettings

# default request function
def baserequest(url):
  try:
    return requests.get(url).json()
  except:
    print('ERROR: Unable to retrieve price, check custom price URL:\n\t{}'.format(url))

# custom price functions
def getprice(asset, endpoint):
    assetprice = 0
    try:
        if asset in dxsettings.customrequest1:
            # edit for custom json targeting for assets in customrequest1
            assetprice = baserequest(endpoint)['ticker']['price']
        elif asset in dxsettings.customrequest2:
            # edit for custom json targeting for assets in customrequest2
            assetprice = baserequest(endpoint)
        elif asset in dxsettings.customrequest3:
            # edit for custom json targeting for assets in customrequest3
            assetprice = baserequest(endpoint)
        else:
            # default request for all other assets
            assetprice = baserequest(endpoint)
    except Exception as e:
        raise RuntimeError(e)
    return assetprice


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
