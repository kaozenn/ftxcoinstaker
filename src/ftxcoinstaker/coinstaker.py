# src/ftxcoinstaker/coinstaker.py
import os
import random
import time
from . import ftx_client
from . import utils
from pprint import pprint


class CoinStaker:

    def __init__(self, pair) -> None:
        self._pair = pair
        self._initial_delay = random.randint(0,1)
        self._clock = 60
        self._ftx = {}
        self._tracker = {}

    def _get_sr_zones(self):
        self._tracker['sr_zones'] = self._pair['sr_zones']

    def _get_market_data(self):
        market = self._ftx.market(self._pair['name'])
        self._tracker['price'] = market['price']
        self._tracker['minProvideSize'] = market['minProvideSize']
        self._tracker['name'] = self._pair['name']

    def _get_open_orders(self):
        self._tracker['openOrders'] = self._ftx.get_open_orders(self._pair['name'])

    def initialise(self) -> None:
        time.sleep(self._initial_delay)
        self._ftx = ftx_client.FtxClient(
            api_key=os.getenv('FTX_API_KEY'),
            api_secret=os.getenv('FTX_API_SECRET'),
            subaccount_name=os.getenv('FTX_SUBACCOUNT_NAME'),
        )
        pprint(f"Loading {self._pair['name']}")
        self._get_sr_zones()
        self._get_market_data()
        self._get_open_orders()
        pprint(self._tracker)

    # def execute(self) -> None:
        # Get open orders

    def run(self) -> None:
        self.initialise()
        # self.execute()


        