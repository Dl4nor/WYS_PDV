'''
from ..services.Pagbank_API import Pagbank_account_API
import webbrowser

class homeController():
    def __init__(self):
        self.pbaAPI = Pagbank_account_API()

    def open_pagbank_login(self):
        # Abrir login no site da pagbank para
        # Autorização do app

        auth_link = self.pbaAPI.get_auth_link_to_oauth2()

        webbrowser.open(auth_link)
'''