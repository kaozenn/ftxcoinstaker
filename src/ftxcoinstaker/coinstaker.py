# src/ftxcoinstaker/coinstaker.py
import random
import time
from pprint import pprint

class CoinStaker:

    def __init__(self, pair) -> None:
        self._pair = pair
        self._initial_delay = random.randint(0,3)

    def run(self) -> None:
        time.sleep(self._initial_delay)
        pprint(self._pair)

