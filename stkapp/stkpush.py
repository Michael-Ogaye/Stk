import requests
import base64
from requests.auth import HTTPBasicAuth
from datetime import datetime
import json

class StkPush:
    def __init__(self,consumer_key,consumer_secret,pass_key):
        self.consumer_secret=consumer_secret
        self.consumer_key=consumer_key
        self.pass_key=pass_key

    def auth_token(self):
        authm=HTTPBasicAuth(self.consumer_key,self.consumer_secret)
        
        url_auth='https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
        try:

           res=requests.get(url_auth,auth=authm)

        except:
            res=requests.get(url_auth,auth=authm,verify=False)

        return res.json()['access_token']