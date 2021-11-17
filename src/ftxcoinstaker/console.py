# src/ftxcoinstaker/console.py

import os
from . import client
from pprint import pprint
from slack_sdk.webhook import WebhookClient

def main():

	FTX_API_KEY=os.getenv('FTX_API_KEY')
	FTX_API_SECRET=os.getenv('FTX_API_SECRET')
	FTX_SUBACCOUNT_NAME=os.getenv('FTX_SUBACCOUNT_NAME')

	ftx = client.FtxClient(api_key=FTX_API_KEY, api_secret=FTX_API_SECRET, subaccount_name=FTX_SUBACCOUNT_NAME)

	SLACK_WEBHOOK_URL=os.getenv('SLACK_WEBHOOK_URL')
	# balance = ftx.get_balances()

	slack = WebhookClient(SLACK_WEBHOOK_URL)
	response = slack.send(text="Hello!")
	assert response.status_code == 200
	assert response.body == "ok"