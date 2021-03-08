#!/usr/bin/env python3
# src/ftxcoinstaker/main.py
import time
from .coinStaker import CoinStaker
from pprint import pprint
from concurrent.futures import ThreadPoolExecutor, as_completed


def main():

    eth_usd = CoinStaker(
        base_coin_symbol = 'ETH',
        pair_coin_symbol = 'USD',
        base_coin_bal = 0.005867,
        side = 'buy',
        )

    ray_eth=CoinStaker(
        base_coin_symbol = 'RAY',
        pair_coin_symbol = 'ETH',
        base_coin_bal = 0.89356931,
        side = 'buy',
        )

    doge_eth = CoinStaker(
        base_coin_symbol = 'DOGE',
        pair_coin_symbol = 'ETH',
        base_coin_bal = 163.02683961,
        side = 'buy',
        )

    with ThreadPoolExecutor(max_workers=5) as executor:
        toExecute = [
            eth_usd.startCoinStaker,
            ray_eth.startCoinStaker,
            doge_eth.startCoinStaker,
        ]
        futures = []
        for te in toExecute:
            futures.append(executor.submit(te))
        for future in as_completed(futures):
            future.result()

if __name__ == '__main__':
    main()
