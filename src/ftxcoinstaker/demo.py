# src/ftxcoinstaker/demo.py

import os
import glob
# import re
import yaml
# from . import ftx_client
from . import coinstaker
# from . import ws_client
from pprint import pprint
# from slack_sdk.webhook import WebhookClient

def main():

	# FTX_API_KEY=os.getenv('FTX_API_KEY')
	# FTX_API_SECRET=os.getenv('FTX_API_SECRET')
	# FTX_SUBACCOUNT_NAME=os.getenv('FTX_SUBACCOUNT_NAME')

	# root = os.path.dirname(__file__)
	# pprint(glob.glob(f"{root}/config/pairs/*.yaml"))

	# REST API
	# ftx = rest_client.FtxClient(api_key=FTX_API_KEY, api_secret=FTX_API_SECRET, subaccount_name=FTX_SUBACCOUNT_NAME)
	# Get single market
	# market = ftx.market('BTC/USD')
	# pprint(market)

	# Get all markets
	# markets = ftx.list_markets()
	# pprint(markets)

	# for	market in markets:
	# 	deriv = re.search(r'(BEAR|BULL|HEDGE|HALF|PERP|\d{4}|USDT)', market['name'])
	# 	usd = re.search(r'(\/USD)', market['name'])

	# 	if market['type'] == 'spot' and usd and not deriv:
	# 		minProvideSize = market['minProvideSize']
	# 		price = market['price']
	# 		print(f"{market['name']}	{minProvideSize * price}")

	# Place Order
	# market='BTC/USD'
	# price=23000
	# stake=20
	# side='buy'
	# size=(stake/price)
	# order_type='limit'

	# place_order=ftx.place_order(
	# 	market=market,
	# 	side=side,
	# 	price=price,
	# 	size=size,
	# 	type=order_type,
	# )

	# pprint(place_order)

	# get_open_orders=ftx.get_open_orders(
	# 	market=market
	# )
	# pprint(get_open_orders[0]['id'])

	# stake=10
	# modify_order=ftx.modify_order(
	# 	existing_order_id=get_open_orders[0]['id'],
	# 	size=(stake/price),
	# )
	# pprint(modify_order)




	#YAML DEMO
	# with open("/home/kaozn/Workspace/ftxcoinstaker/src/ftxcoinstaker/config.yaml", "r") as stream:
	# 	try:
	# 		config = yaml.safe_load(stream)
	# 	except yaml.YAMLError as exc:
	# 		pprint(exc)

	# price_frame_ratio=config['price_frame_ratio']
	# bottom_price_ref=config['bottom_price_ref']
	# top_price_ref=config['top_price_ref']
	# decimal=config['decimal']

	# price=bottom_price_ref
	# matrix = []
	# while price < top_price_ref:
	# 	matrix.append(format(price, f'.{decimal}f'))
	# 	price = price + ((price + price_frame_ratio)/100)

	# pprint(matrix) 


	# Webhook Demo
	# SLACK_WEBHOOK_URL=os.getenv('SLACK_WEBHOOK_URL')


	# slack = WebhookClient(SLACK_WEBHOOK_URL)
	# response = slack.send(text="Hello!")
	# assert response.status_code == 200
	# assert response.body == "ok"