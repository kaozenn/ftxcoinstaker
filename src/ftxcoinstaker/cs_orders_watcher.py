# src/ftxcoinstaker/cs_orders_watcher.py

import os
import logging
from pprint import pprint
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


class CsOrdersWatcher:

	def __init__(self, pair) -> None:
		self._pair = pair

	def _init(self) -> None:
		logger.info(f"[{self._pair['name']}] - Init")

	def _exec(self) -> None:
		logger.info(f"[{self._pair['name']}] - Exec")
		# # Do an infinite loop
		# ftx_open_orders = self._get_ftx_open_orders()
		# diff_open_orders = self._diff_open_orders(self._pair['open_orders'], ftx_open_orders)
		# self._set_local_open_orders(ftx_open_orders)

	# def _get_db_open_orders(self) -> List[dict]:
	# 	self._shelve = shelve.open(f"{root}/user_data/db/{self._pair['id']}")
	# 	try:
	# 		open_orders = self._shelve['open_orders']
	# 	except Exception as exc:
	# 		logger.debug(f"[{self._pair['name']}] - No open order stored")
	# 		self._shelve['open_orders'] = []
	# 	else:
	# 		return open_orders
	# 	self._shelve.close()

	# def _set_local_open_orders(self, open_orders) -> None:
	# 	self._shelve = shelve.open(f"{root}/user_data/db/{self._pair['id']}")
	# 	try:
	# 		self._shelve['open_orders'] = open_orders
	# 	except Exception as exc:
	# 		logger.debug(f"[{self._pair['name']}] - {exc}")
	# 	self._shelve.close()
	# 	pprint('test')
	
	# def _get_ftx_open_orders(self) -> List[dict]:
	# 	ftx_open_orders = ftx.get_open_orders(self._pair['name'])
	# 	open_orders = []
	# 	for ftx_open_order in ftx_open_orders:
	# 		open_order = {}
	# 		open_order['id'] = ftx_open_order['id']
	# 		open_order['price'] = ftx_open_order['price']
	# 		open_order['side'] = ftx_open_order['side']
	# 		open_order['size'] = ftx_open_order['size']
	# 		open_order['filledSize'] = ftx_open_order['filledSize']
	# 		open_order['remainingSize'] = ftx_open_order['remainingSize']
	# 		open_order['timestamp'] = utils.ftx_date_to_timestamp(ftx_open_order['createdAt'])
	# 		open_order['order_value'] = ftx_open_order['size'] * ftx_open_order['price']
	# 		open_orders.append(open_order)
	# 	return open_orders

	# def _diff_open_orders(self, local_open_orders, ftx_open_orders)  -> List[dict]:
	# 	delta = []
	# 	for open_order in local_open_orders:
	# 		if open_order not in ftx_open_orders:
	# 			logger.debug(f"[{self._pair['name']}] - {open_order['id']} not present on in FTX open orders")
	# 			delta.append(open_order)
	# 	return delta

	def run(self) -> None:
		self._init()
		self._exec()
