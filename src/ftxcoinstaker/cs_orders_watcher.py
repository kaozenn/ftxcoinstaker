# src/ftxcoinstaker/cs_orders_watcher.py

import os
import logging
import sqlite3
from slack_sdk.webhook import WebhookClient
from pprint import pprint
from datetime import datetime
import time
from . import ftx_client
from . import utils
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)
logging.basicConfig(level=os.getenv('CS_LOGGING_LEVEL'))

ftx = ftx_client.FtxClient(
			api_key=os.getenv('FTX_API_KEY'),
			api_secret=os.getenv('FTX_API_SECRET'),
			subaccount_name=os.getenv('FTX_SUBACCOUNT_NAME'),
		)

root = os.path.dirname(__file__)

slack = WebhookClient(os.getenv('CS_SLACK_WEBHOOK_URL'))


class CsOrdersWatcher:

	def __init__(self, pair) -> None:
		self._pair = pair
		self._clock = 10

	def _init(self) -> None:
		logger.info(f"[{self._pair['name']}] - Init")

	def _exec(self) -> None:
		while(True):
			# Monitor new ftx open orders
			self._monitor_new_ftx_open_orders()
			self._monitor_recent_ftx_closed_orders()
			time.sleep(self._clock)

	def _get_db_open_orders(self) -> List[dict]:
		open_orders = []
		c = sqlite3.connect(f"{root}/user_data/db/{self._pair['id']}.db")
		sql = '''
			SELECT id, createdAtTs, createdAtDate, side, price,
				   size, filledSize, remainingSize, orderValue, status
			FROM orders
			WHERE status = 'open'
			;'''
		results = c.execute(sql)
		rows = results.fetchall()
		c.close()

		for row in rows:
			open_order = {}
			open_order['id'] = row[0]
			open_order['createdAtTs'] = row[1]
			open_order['createdAtDate'] = row[2]
			open_order['side'] = row[3]
			open_order['price'] = row[4]
			open_order['size'] = row[5]
			open_order['filledSize'] = row[6]
			open_order['remainingSize'] = row[7]
			open_order['orderValue'] = row[8]
			open_order['status'] = row[9]
			open_orders.append(open_order)
		return open_orders

	def _set_db_open_orders(self, open_orders) -> None:
		c = sqlite3.connect(f"{root}/user_data/db/{self._pair['id']}.db")
		for open_order in open_orders:
			sql = f"""
				INSERT INTO orders (
					id, createdAtTs, createdAtDate, side, price,
					size, filledSize, remainingSize, orderValue, status
				)
				VALUES (
					{open_order['id']},
					{open_order['createdAtTs']},
					"{open_order['createdAtDate']}",
					"{open_order['side']}",
					{open_order['price']},
					{open_order['size']},
					{open_order['filledSize']},
					{open_order['remainingSize']},
					{open_order['orderValue']},
					"{open_order['status']}"				
				)
				;"""
			results = c.execute(sql)
		c.commit()
		c.close()

	def _update_db_orders_status(self, orders, status) -> None:
		c = sqlite3.connect(f"{root}/user_data/db/{self._pair['id']}.db")
		dt = datetime.now()
		for order in orders:
			sql = f"""
				UPDATE orders
				SET status = 'closed',
					updatedAtTs = {datetime.timestamp(dt)}			
				WHERE id = {order['id']}
				;"""
			results = c.execute(sql)
		c.commit()
		c.close()

	def _get_ftx_open_orders(self) -> List[dict]:
		ftx_open_orders = ftx.get_open_orders(self._pair['name'])
		open_orders = []
		for ftx_open_order in ftx_open_orders:
			open_order = {}
			open_order['id'] = ftx_open_order['id']
			open_order['createdAtTs'] = utils.ftx_date_to_timestamp(ftx_open_order['createdAt'])
			open_order['createdAtDate'] = ftx_open_order['createdAt']
			open_order['side'] = ftx_open_order['side']
			open_order['price'] = ftx_open_order['price']
			open_order['size'] = ftx_open_order['size']
			open_order['filledSize'] = ftx_open_order['filledSize']
			open_order['remainingSize'] = ftx_open_order['remainingSize']
			open_order['orderValue'] = ftx_open_order['size'] * ftx_open_order['price']
			open_order['status'] = ftx_open_order['status']
			open_orders.append(open_order)
		return open_orders

	def _diff_orders(self, list_a, list_b)  -> List[dict]:
		# Return list of objects in list_a that do not exist in list_b
		delta = []
		for order in list_a:
			if order not in list_b:
				logger.debug(f"[{self._pair['name']}] - Adding order id {order['id']}")
				delta.append(order)
		return delta

	def _monitor_new_ftx_open_orders(self) -> None:
		# Compare FTX open orders and add them in local DB if they don't exist
		db_open_orders = self._get_db_open_orders()
		ftx_open_orders = self._get_ftx_open_orders()
		new_open_orders = self._diff_orders(ftx_open_orders,db_open_orders)
		if len(new_open_orders) > 0:
			# Add new orders to db
			self._set_db_open_orders(new_open_orders)
			logger.info(f"[{self._pair['name']}] - Adding orders {new_open_orders} to local database")
			slack_response = slack.send(text=f"[{self._pair['name']}] - Adding orders {new_open_orders} to local database")

	def _monitor_recent_ftx_closed_orders(self) -> None:
		# Check local open orders and compare them with existing FTX open orders
		# If They are not present on the exchange, set orders in local database to closed
		db_open_orders = self._get_db_open_orders()
		ftx_open_orders = self._get_ftx_open_orders()
		new_closed_orders = self._diff_orders(db_open_orders, ftx_open_orders)
		if len(new_closed_orders) > 0:
			self._update_db_orders_status(new_closed_orders,'closed')
			logger.info(f"[{self._pair['name']}] - New closed order: {new_closed_orders}")
			slack_response = slack.send(text=f"[{self._pair['name']}] - New closed order: {new_closed_orders}")

	def run(self) -> None:
		self._init()
		self._exec()
