#!/usr/bin/python3
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import flask.json
import decimal
import time
import calendar
import dateutil
from dateutil import parser
from utils import dxsettings

rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:%s"%(dxsettings.rpcuser, dxsettings.rpcpassword, dxsettings.rpcport))

class MyJSONEncoder(flask.json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            # Convert decimal instances to strings.
            return str(obj)
        return super(MyJSONEncoder, self).default(obj)


def lookup_order_id(orderid, myorders):
  # find my orders, returns order if orderid passed is inside myorders
  return [zz for zz in myorders if zz['id'] == orderid]

def canceloldestorder():
  myorders = getopenorders()
  oldestepoch = 3539451969
  currentepoch = 0
  epochlist = 0
  oldestorderid = 0
  for z in myorders:
    if z['status'] == "open":
      createdat = z['created_at']
      currentepoch = getepochtime((z['created_at']))
      if oldestepoch > currentepoch:
        oldestorderid = z['id']
        oldestepoch = currentepoch
      if oldestorderid != 0:
        rpc_connection.dxCancelOrder(oldestorderid)  
  return oldestorderid, oldestepoch

def cancelallorders():
  # cancel all my open orders
  myorders = rpc_connection.dxGetMyOrders()
  for z in myorders:
    if z['status'] == "open":
      results = rpc_connection.dxCancelOrder(z['id'])
      time.sleep(3.5)
      print (results)
  return

def getopenorders():
    # return open orders
    myorders = rpc_connection.dxGetMyOrders()
    return [zz for zz in myorders if zz['status'] == "open"] 

def getepochtime(created):
    # converts created to epoch
    return calendar.timegm(dateutil.parser.parse(created).timetuple())
   
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
