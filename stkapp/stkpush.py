import requests

class StkPush:
    def __init__(self,consumer_key,consumer_secret,pass_key):
        self.consumer_secret=consumer_secret
        self.consumer_key=consumer_key
        self.pass_key=pass_key

    def auth_token: