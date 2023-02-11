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

    def timestamp():
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