# src/ftxcoinstaker/coinStaker.py
import os
import sys
import time
import random
from pprint import pprint
from .myFtx import MyFtxClient

class CoinStaker:
    def __init__(self, subaccount_name=None, base_coin_symbol=None, pair_coin_symbol='USD', base_coin_bal=0.00, pair_coin_bal=0.00, side='sell'):
        self.subaccount_name = subaccount_name if subaccount_name is not None else f'{base_coin_symbol}-{pair_coin_symbol}'.upper()
        self.ftx_client = MyFtxClient()
        self.ftx_api_key = ''
        self.ftx_api_secret = ''
        self.base_coin_symbol = base_coin_symbol
        self.base_coin_bal = base_coin_bal
        self.pair_coin_symbol = pair_coin_symbol
        self.pair_coin_bal = pair_coin_bal
        self.side = side

    def _isSubaccountExist(self, nickname):
        client = MyFtxClient(
            api_key=self.ftx_api_key,
            api_secret=self.ftx_api_secret,
            )  
        subaccounts = client.get_subaccounts()
        subaccount_names = []
        for subaccount in subaccounts:
            subaccount_names.append(subaccount['nickname'])
        if nickname not in subaccount_names:
            print(f'Subaccount {nickname} does not exist, create it or select a different one')
            sys.exit(1)
        else:
            return True

    def _initSubaccountBalances(self):
        balances = self.ftx_client.get_subaccounts_balance(self.subaccount_name)
        for balance in balances:
            coin = balance['coin']
            balance = balance['free']
            if (coin == self.base_coin_symbol and self.base_coin_bal == 0.00 ):
                self.base_coin_bal = balance
            elif (coin == self.pair_coin_symbol and self.pair_coin_bal == 0.00 ):
                self.pair_coin_bal = balance
        
        if (self.base_coin_bal == 0 and self.pair_coin_bal == 0 ):
            print(f'{self.base_coin_symbol} and {self.pair_coin_symbol} balance is 0. Add some {self.base_coin_symbol} or {self.pair_coin_symbol} funds to {self.subaccount_name} to start trading')
            sys.exit(1)

        print(f'{self.subaccount_name} [ {self.base_coin_symbol} ({self.base_coin_bal}) -> {self.pair_coin_symbol} ({self.pair_coin_bal}) Side: {self.side}] => ✓')

    def _initCoinStaker(self):
        try:
            self.ftx_api_key=os.environ['FTX_API_KEY']
            self.ftx_api_secret=os.environ['FTX_API_SECRET']
        except:
            raise Exception('Environment Variables FTX_API_KEY or FTX_API_SECRET are missing.')

        if (self._isSubaccountExist(self.subaccount_name)):

            self.ftx_client = MyFtxClient(
                api_key=self.ftx_api_key,
                api_secret=self.ftx_api_secret,
                subaccount_name=self.subaccount_name,
                )

            self._initSubaccountBalances()

    def _runCoinStaker(self):
        diff = -1.00
        random_int = random.randint(1, 1200)
        if (self.side == 'sell'):
            fromCoin = self.base_coin_symbol
            toCoin = self.pair_coin_symbol
            size = self.base_coin_bal
            previousSize = self.pair_coin_bal
        elif (self.side == 'buy'):
            fromCoin = self.pair_coin_symbol
            toCoin = self.base_coin_symbol
            size = self.pair_coin_bal
            previousSize = self.base_coin_bal
        while ( diff < 0 ):
            quote = self._getQuote(fromCoin, toCoin, size)
            diff = quote['proceeds'] - previousSize
            print(f"[{self._getLocalTime()}] [{self.base_coin_symbol} {self._getSideASCIISymbol()} {self.pair_coin_symbol}] New Quote: {quote['fromCoin']} {quote['cost']} -> {quote['toCoin']} {quote['proceeds']} (was {previousSize} => {diff})")
            time.sleep(random_int)
            if ( diff > 0 ):
                print(f"[{self._getLocalTime()}] [{self.base_coin_symbol} {self._getSideASCIISymbol()} {self.pair_coin_symbol}] Accepting Quote: {quote['fromCoin']} {quote['cost']} -> {quote['toCoin']} {quote['proceeds']} (was {previousSize} => {diff})")
                self._acceptQuote(quote['id'])
                if (self.side == 'sell'):
                    self.side = 'buy'
                    self.pair_coin_bal = quote['proceeds']
                    self.base_coin_bal = quote['proceeds']
                elif (self.side == 'buy'):
                    self.side = 'sell'
                    self.base_coin_bal = quote['proceeds']
                self._runCoinStaker()

    def startCoinStaker(self):
        self._initCoinStaker()
        self._runCoinStaker()

    def _getQuote(self, fromCoin, toCoin, size):
        quote = self.ftx_client.request_quote(fromCoin, toCoin, size)
        quote_id = quote['quoteId']
        quoteStatus = self.ftx_client.get_quote_status(quote_id)
        return quoteStatus

    def _acceptQuote(self, quote_id):
        result = self.ftx_client.accept_quote(quote_id)
        pprint(result)
        return True

    def _getLocalTime(self):
        struct_time = time.localtime() # get struct_time
        time_string = time.strftime("%m/%d/%Y, %H:%M:%S", struct_time)
        return time_string
    
    def _getSideASCIISymbol(self):
        symbol_string = ''
        if (self.side == 'sell'):
            symbol_string = '->'
        elif (self.side == 'buy'):
            symbol_string = '<-'
        return symbol_string

        