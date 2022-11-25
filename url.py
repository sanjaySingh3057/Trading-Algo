
from kiteconnect import KiteConnect
import os

key = "ul1bsdsnl3z4ii5c"
secret = "vcutkjm8z1rhduxfx32mgzq3gko21xpo"
kite = KiteConnect(api_key=key)
print(kite.login_url())


req_tkn= input("enter req token\n")
gen_ssn=kite.generate_session(request_token=req_tkn, api_secret=secret)
acc_tkn = gen_ssn['access_token']

myfile=open("acctkn.txt","w+")

myfile.write(acc_tkn)





            
            