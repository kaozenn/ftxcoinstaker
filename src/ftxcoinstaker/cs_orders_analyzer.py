# src/ftxcoinstaker/cs_orders_analyzer.py

import os
import logging
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)
logging.basicConfig(level=os.getenv('CS_LOGGING_LEVEL'))

class CsOrdersAnalyzer:

	def __init__(self, pair) -> None:
		self._pair = pair

	def init(self) -> None:
		logger.info(f"[{self._pair['name']}] - ini")

	def exec(self) -> None:
		logger.info(f"[{self._pair['name']}] - exec")

	def run(self) -> None:
		self.init()
		self.exec()
