# src/ftxcoinstaker/console.py

import os
from . import client

def main():

	FTX_API_KEY=os.getenv('FTX_API_KEY')
	FTX_API_SECRET=os.getenv('FTX_API_SECRET')

	ftx = client.FtxClient(FTX_API_KEY, FTX_API_SECRET)

	response = ftx.create_subaccount("test")

	# balance = ftx.get_subaccounts()
	# print(balance)
