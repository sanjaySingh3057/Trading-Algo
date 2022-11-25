from ast import Global, List, While
from asyncio.windows_events import NULL
from cmd import IDENTCHARS
from email import utils
from math import ceil
from optparse import Values
from turtle import pos
from kiteconnect import KiteConnect
import time
from threading import Thread 
from datetime import datetime
import math
from dateutil.relativedelta import relativedelta, TH

t=time.time()
key = "ul1bsdsnl3z4ii5c"
secret = "vcutkjm8z1rhduxfx32mgzq3gko21xpo"
kite = KiteConnect(api_key=key)

f=open("acctkn.txt","r")

acc_tkn=f.readline()
print(acc_tkn)



kite.set_access_token(acc_tkn)


def f():
    global symbol_ce
    global symbol_pe
    global atm_strike
    global thurs
    global strike_ce
    global strikece2
    global strike_pe
    global strikepe2
    global ceprice
    global peprice
    global pe2price
    global ce2price
    global entry_ce
    global entry_pe
    global sl_ce
    global sl_pe
    global tr_ce
    global tr_pe
    global idslce
    global idslpe
    global qtyce
    global qtype

f()

def place_order2(self,variety,exchange,tradingsymbol,transaction_type,quantity,product,order_type,price=None,validity=None,disclosed_quantity=None,trigger_price=None,squareoff=None,stoploss=None,trailing_stoploss=None,tag=None):
    
    params = locals()
    del(params["self"])
    for k in list(params.keys()):
        if params[k] is None:
            del(params[k])
    return self._post("order.place", url_args={"variety": variety}, params=params)["order_id"]

def cancel_order(self, variety, order_id, parent_order_id=None):
    
    return self._delete("order.cancel",
                        url_args={"variety": variety, "order_id": order_id},
                        params={"parent_order_id": parent_order_id})["order_id"]

def positions(self):
    return self._get("portfolio.positions")

def holdings(self):
    return self._get("portfolio.holdings")
    
def modify_order(self,variety,order_id,parent_order_id=None,quantity=None,price=None,order_type=None,trigger_price=None,validity=None,disclosed_quantity=None):
    params = locals()
    del(params["self"])
    for k in list(params.keys()):
        if params[k] is None:
            del(params[k])
    return self._put("order.modify",url_args={"variety": variety, "order_id": order_id},params=params)["order_id"]

def getCMP(tradingSymbol):
    quote = kite.quote(tradingSymbol)
    if quote:
        return quote[tradingSymbol]['last_price']
    else:
        return 0

def get_symbols(expiry, name, strike, ins_type):
    global instrumentsList

    
    instrumentsList = kite.instruments('NFO')

    lst_b = [num for num in instrumentsList if num['expiry'] == expiry and num['strike'] == strike
             and num['instrument_type'] == ins_type and num['name'] == name]
    return lst_b[0]['tradingsymbol']

def order_history(self, order_id):
    return self._format_response(self._get("order.info", url_args={"order_id": order_id}))





atm_strike = round(getCMP('NSE:NIFTY 50'), -2)
strike_ce=atm_strike+300
strike_pe=atm_strike-300
print("atm strike price=  ",atm_strike,"\n\n")
next_thursday_expiry = datetime.today() + relativedelta(weekday=TH(1))
thurs = next_thursday_expiry.date()
symbol_ce = get_symbols(thurs , 'NIFTY', strike_ce, 'CE')
symbol_pe = get_symbols(thurs , 'NIFTY', strike_pe, 'PE')












ceprice= getCMP("NFO:"+symbol_ce)
peprice= getCMP("NFO:"+symbol_pe)
while( ceprice < 100 ) :  #caclulates strikeprice whose premium is just above 100 both for ce and pe
    strike_ce=strike_ce-50.0
    symbol_ce = get_symbols(thurs, 'NIFTY', strike_ce, 'CE')
    ceprice = getCMP("NFO:"+symbol_ce) 
while(  peprice < 100 ) :  #caclulates strikeprice whose premium is just above 100 both for ce and pe
    strike_pe=strike_pe+50.0
    symbol_pe = get_symbols(thurs, 'NIFTY', strike_pe, 'PE')
    peprice= getCMP("NFO:"+symbol_pe)
strikece2=strike_ce+50
strikepe2=strike_pe-50
ce2price=getCMP("NFO:"+get_symbols(thurs, 'NIFTY', strikece2, 'CE'))
pe2price=getCMP("NFO:"+get_symbols(thurs, 'NIFTY', strikepe2, 'PE'))


    
if ( abs(100-ceprice ) > abs(100-ce2price )) :
     symbol_ce = get_symbols(thurs, 'NIFTY', strikece2, 'CE')
else :
     symbol_ce = get_symbols(thurs, 'NIFTY', strike_ce, 'CE')
    
print("call strike to sell=  ",symbol_ce , getCMP("NFO:"+symbol_ce))
    


if ( abs(100-peprice ) > abs(100-pe2price)) :
    symbol_pe = get_symbols(thurs, 'NIFTY', strikepe2, 'PE')
else :
     symbol_pe = get_symbols(thurs, 'NIFTY', strike_pe, 'PE')
    

print("put strike to sell=   ",symbol_pe , getCMP("NFO:"+symbol_pe),"\n\n")
    










entry_ce=getCMP("NFO:"+symbol_ce)
entry_ce= math.floor(entry_ce)

idce=place_order2(self= kite ,  variety=kite.VARIETY_REGULAR,   exchange=KiteConnect.EXCHANGE_NFO,  tradingsymbol=symbol_ce,  order_type=KiteConnect.ORDER_TYPE_LIMIT , transaction_type=KiteConnect.TRANSACTION_TYPE_SELL,  product=KiteConnect.PRODUCT_NRML,   quantity=50,price=entry_ce-1)

entry_pe=getCMP("NFO:"+symbol_pe)
entry_pe= math.floor(entry_pe)

idpe=place_order2(self= kite ,price=entry_pe-1,  variety=kite.VARIETY_REGULAR,   exchange=KiteConnect.EXCHANGE_NFO,  tradingsymbol=symbol_pe,  order_type=KiteConnect.ORDER_TYPE_LIMIT , transaction_type=KiteConnect.TRANSACTION_TYPE_SELL,  product=KiteConnect.PRODUCT_NRML,   quantity=50)

f=1
qty1=0
qty2=0
while(f==1):
    x=positions(kite)['net']

  
    for j in x :
        b=j['tradingsymbol']
        if b==symbol_ce :
            qty1=j['quantity']  
        if b==symbol_pe :
            qty2=j['quantity']
            
    if(qty1==-50):
        if(qty2==-50):
         f=0
        else :
         f=1
    else :
     f=1

     
    print("waiting for entry ")

        
       
        















sl_ce=entry_ce+10.1
sl_pe=entry_pe+10.1
tr_ce=entry_ce+10
tr_pe=entry_pe+10


idslce=place_order2(self= kite ,  variety=kite.VARIETY_REGULAR,   exchange=KiteConnect.EXCHANGE_NFO,  tradingsymbol=symbol_ce,  order_type=KiteConnect.ORDER_TYPE_SL  , transaction_type=KiteConnect.TRANSACTION_TYPE_BUY,  product=KiteConnect.PRODUCT_NRML,   quantity=50, price=sl_ce,  trigger_price=tr_ce)

idslpe=place_order2(self= kite ,  variety=kite.VARIETY_REGULAR,   exchange=KiteConnect.EXCHANGE_NFO,  tradingsymbol=symbol_pe,  order_type=KiteConnect.ORDER_TYPE_SL  , transaction_type=KiteConnect.TRANSACTION_TYPE_BUY,  product=KiteConnect.PRODUCT_NRML,   quantity=50, price=sl_pe,  trigger_price=tr_pe)












def trailsell(self,id,symbol,entryprice):
    x=positions(self)['net']
    
    for j in x :
        b=j['tradingsymbol']
        if b==symbol:
            qty=j['quantity']  

    mlt5=0
    tr=entryprice+10
    while (qty!=0) :
       ltp=getCMP(tradingSymbol="NFO:"+symbol)
       if (int)((entryprice-ltp)/5) > mlt5 :
            mlt5=(int)((entryprice-ltp)/5)
            tr=entryprice+10-(2*mlt5)
                
            id=modify_order(self, variety=kite.VARIETY_REGULAR, order_id=id, quantity=50, price=tr+0.1, trigger_price=tr,  order_type=KiteConnect.ORDER_TYPE_SL) 
            print(symbol,"  price=",ltp,"  SLTRIGGER=",tr)

       
       x=positions(self)['net']
       for j in x :
          b=j['tradingsymbol']
          if b==symbol:
            qty=j['quantity']

       time.sleep(0.5)
            
            
thrd=Thread(target=trailsell,args=(kite,idslce,symbol_ce,entry_ce))
thrd.start()
trailsell(self=kite,id=idslpe,symbol=symbol_pe,entryprice=entry_pe)
thrd.join()

