# src/ftxcoinstaker/coinstaker.py

import os
import random
import time
import sqlite3
from . import cs_orders_watcher
from . import cs_orders_analyzer
from . import cs_orders_executor
from multiprocessing import Process
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=os.getenv('CS_LOGGING_LEVEL'))
root = os.path.dirname(__file__)

class CoinStaker:

	def __init__(self, pair) -> None:
		self._pair = pair
		self._initial_delay = random.randint(0,1)
		self._orders_watcher = {}
		self._orders_analyzer = {}
		self._orders_executor = {}

	def init(self) -> None:
		# time.sleep(self._initial_delay)
		self._orders_watcher = cs_orders_watcher.CsOrdersWatcher(self._pair)
		self._orders_analyzer = cs_orders_analyzer.CsOrdersAnalyzer(self._pair)
		self._orders_executor = cs_orders_executor.CsOrdersExecutor(self._pair)
		self.init_orders_db()

	def exec(self) -> None:
		procs = []
		# modules = [self._orders_watcher, self._orders_analyzer, self._orders_executor]
		modules = [self._orders_watcher]
		for module in modules:
			proc = Process(target=module.run)
			procs.append(proc)
			proc.start()
		for proc in procs:
			proc.join()

	def init_orders_db(self) -> None:
		sql = '''
			CREATE TABLE IF NOT EXISTS orders(
				id						INT PRIMARY KEY		NOT NULL,
				createdAtTs				INT					NOT NULL,
				createdAtDate			CHAR(32)			NOT NULL,
				side					CHAR(4)				NOT NULL,
				price					FLOAT				NOT NULL,
				size					FLOAT				NOT NULL,
				filledSize				FLOAT				NOT NULL,
				remainingSize			FLOAT				NOT NULL,
				orderValue				FLOAT				NOT NULL,
				status					FLOAT				NOT NULL,
				updatedAtDate			CHAR(32),
				updatedAtTs				INT,
				consolidatedOrderId		INT
			);
			'''
		conn = sqlite3.connect(f"{root}/user_data/db/{self._pair['id']}.db")
		conn.execute(sql)
		conn.close()
		logger.info(f"[{self._pair['name']}] - database {self._pair['id']} initialised successfuly")


	def run(self) -> None:
		self.init()
		self.exec()
