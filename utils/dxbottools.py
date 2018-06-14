#!/usr/bin/python3
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import flask.json
import decimal
import time
from utils import dxsettings

rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:41414"%(dxsettings.rpcuser, dxsettings.rpcpass))

class MyJSONEncoder(flask.json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            # Convert decimal instances to strings.
            return str(obj)
        return super(MyJSONEncoder, self).default(obj)


def lookup_order_id(orderid, myorders):
  # find my orders, returns order if orderid passed is inside myorders
  return [zz for zz in myorders if zz['id'] == orderid]

def cancelallorders():
  # cancel all my orders
  myorders = rpc_connection.dxGetMyOrders()
  for z in myorders:
    results = rpc_connection.dxCancelOrder(z['id'])
    print (results)
  return

def showorders():
    print ('### Getting balances >>>')
    mybalances = rpc_connection.dxGetTokenBalances()
    print (mybalances)
    print ('### Getting my orders >>>')
    myorders = rpc_connection.dxGetMyOrders()
    for z in myorders:
      print (z['status'], z['id'], z['maker'], z['maker_size'], z['taker'],z['taker_size'], float(z['taker_size'])/float(z['maker_size']))

    allorders = rpc_connection.dxGetOrders()
    print ('#############################################################')
    for z in allorders:
      #lets see if order is ours
      if lookup_order_id(z['id'], myorders):
        ismyorder = "True"
      else:
        ismyorder = "False"
      print (z['status'], z['id'], ismyorder, z['maker'], z['maker_size'], z['taker'],z['taker_size'], float(z['taker_size'])/float(z['maker_size']))
