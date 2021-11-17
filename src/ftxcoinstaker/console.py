# src/ftxcoinstaker/console.py

import os
from . import client
from pprint import pprint

def main():

	FTX_API_KEY=os.getenv('FTX_API_KEY')
	FTX_API_SECRET=os.getenv('FTX_API_SECRET')
	FTX_SUBACCOUNT_NAME=os.getenv('FTX_SUBACCOUNT_NAME')

	ftx = client.FtxClient(api_key=FTX_API_KEY, api_secret=FTX_API_SECRET, subaccount_name=FTX_SUBACCOUNT_NAME)

	#response = ftx.create_subaccount("test")

	balance = ftx.get_balances()
	pprint(balance)
