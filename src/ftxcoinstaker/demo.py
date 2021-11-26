# src/ftxcoinstaker/demo.py

import os
import shelve
import glob
from pprint import pprint
import logging

# from slack_sdk.webhook import WebhookClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():

	logger.info('Start reading database')
	# read database here
	records = {'john': 55, 'tom': 66}
	logger.debug('Records: %s', records)
	logger.info('Updating records ...')
	# update records here
	logger.info('Finish updating records')

	# root = os.path.dirname(__file__)
	# datafile = glob.glob(f"{root}/config/btc_usd.kv")

	# s = shelve.open("test")
	# s['name'] = "Ajay"
	# s['age'] = 23
	# s['marks'] = 75
	# s.close()

	# s = shelve.open("test")
	# items = s.items()
	# pprint(list(items))
	# s.close()



	# Webhook Demo
	# SLACK_WEBHOOK_URL=os.getenv('SLACK_WEBHOOK_URL')


	# slack = WebhookClient(SLACK_WEBHOOK_URL)
	# response = slack.send(text="Hello!")
	# assert response.status_code == 200
	# assert response.body == "ok"