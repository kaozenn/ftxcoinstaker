# src/ftxcoinstaker/coinstaker.py

import os
import random
import time
from . import cs_orders_watcher
from . import cs_orders_analyzer
from . import cs_orders_executor
import shelve
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
		time.sleep(self._initial_delay)
		self._orders_watcher = cs_orders_watcher.CsOrdersWatcher(self._pair)
		self._orders_analyzer = cs_orders_analyzer.CsOrdersAnalyzer(self._pair)
		self._orders_executor = cs_orders_executor.CsOrdersExecutor(self._pair)
		s = shelve.open(f"{root}/user_data/db/{self._pair['id']}")
		s['name'] = self._pair['name']
		s['id'] = self._pair['id']
		s.close()

	def exec(self) -> None:
		procs = []
		modules = [self._orders_watcher, self._orders_analyzer, self._orders_executor]
		for module in modules:
			proc = Process(target=module.run)
			procs.append(proc)
			proc.start()
		for proc in procs:
			proc.join()

	def run(self) -> None:
		self.init()
		self.exec()
