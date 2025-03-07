import webbrowser
from services.Pagbank_API import Pagbank_account_API

class homeController():
    def __init__(self):
        self.pbaAPI = Pagbank_account_API()

    def open_pagbank_login(self):
        # Abrir login no site da pagbank para
        # Autorização do app

        auth_link = f"{self.pbaAPI.AUTH_URL}?response_type=code&client_id={self.pbaAPI.CLIENT_ID}&redirect_uri={self.pbaAPI.REDIRECT_URI}&scope=payments"

        webbrowser.open(auth_link)