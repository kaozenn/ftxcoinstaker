# src/ftxcoinstaker/cs_orders_analyzer.py

import os
import logging
import shelve
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)
logging.basicConfig(level=os.getenv('CS_LOGGING_LEVEL'))
root = os.path.dirname(__file__)

class CsOrdersAnalyzer:

	def __init__(self, pair) -> None:
		self._pair = pair

	def init(self) -> None:
		s = shelve.open(f"{root}/user_data/db/{self._pair['id']}")
		logger.info(f"[{self._pair['name']}] - {s.get('name')}")
		s.close()

	def exec(self) -> None:
		logger.info(f"[{self._pair['name']}] - exec")

	def run(self) -> None:
		self.init()
		self.exec()
