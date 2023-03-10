import requests
import base64
from requests.auth import HTTPBasicAuth
from datetime import datetime
import json
from django.conf import settings

class StkPush:
    def __init__(self):
        self.consumer_secret=settings.CONSUMER_SECRET
        self.consumer_key=settings.CONSUMER_KEY
        self.pass_key=settings.PASS_KEY
        self.shortCode=settings.SHORT_CODE

    def auth_token(self):
        print(self.consumer_secret,self.shortCode)
        authm=HTTPBasicAuth(self.consumer_key,self.consumer_secret)
        
        url_auth='https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
        # try:

        #    res=requests.get(url_auth,auth=authm)

        # except:
        res=requests.get(url_auth,auth=authm)

        return res.json()['access_token']


    def timestamp(self):
      unformatted_time = datetime.now()
      formatted_time = unformatted_time.strftime("%Y%m%d%H%M%S")

      
      return formatted_time
    
    def generate_password(self):
        f_time=self.timestamp()
        data_to_encode = (
        self.shortCode + self.pass_key +f_time
        )

        encoded_string = base64.b64encode(data_to_encode.encode())
    
        decoded_password = encoded_string.decode("utf-8")

        return decoded_password

    def lNM(self,amount,phone):
        
        access_token=self.auth_token()
       
        timstamp=self.timestamp()
        print(access_token,timstamp)
        passwrd=self.generate_password()
        lpm_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"


        headers = {"Authorization": "Bearer %s" % access_token}

        req = {
            "BusinessShortCode": int(self.shortCode),
            "Password": passwrd,
            "Timestamp": timstamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(amount),
            "PartyA": int(phone),
            "PartyB": int(self.shortCode),
            "PhoneNumber":int(phone),
            "CallBackURL":"https://stkdemo.up.railway.app/lnm/",
            "AccountReference": "sasakazi",
            "TransactionDesc": "Pay for product",
    }

        res= requests.post(lpm_url, json=req, headers=headers)
        print(res.text)

    

