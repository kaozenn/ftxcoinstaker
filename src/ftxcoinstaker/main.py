# src/ftxcoinstaker/main.py

import os
import glob
import yaml
from . import coinstaker
from . import ftx_client
from multiprocessing import Process
from typing import Optional, Dict, Any, List
from pprint import pprint


def main() -> None:
	check_exchange_connectivity()
	pairs = load_pairs_config()
	procs = []
	for pair in pairs:
		proc = Process(target=pair.run)
		procs.append(proc)
		proc.start()
	for proc in procs:
		proc.join()

def load_pairs_config() -> List[dict]:
	pairs_config = []
	root = os.path.dirname(__file__)
	pairs = glob.glob(f"{root}/config/pairs/*.yaml")
	for pair in pairs:
		with open(pair, "r") as pair:
			try:
				pair = yaml.safe_load(pair)
				cs = coinstaker.CoinStaker(pair)
				pairs_config.append(cs)
			except yaml.YAMLError as exc:
				pprint(exc)
	return pairs_config

def check_exchange_connectivity() -> None:
	ftx = ftx_client.FtxClient(
		api_key=os.getenv('FTX_API_KEY'),
		api_secret=os.getenv('FTX_API_SECRET'),
		subaccount_name=os.getenv('FTX_SUBACCOUNT_NAME'),
	)
	try:
		# Get account_info to test connectivity
		account_info = ftx.get_account_info()
	except Exception as exc:
		pprint(f"Unable to authenticate to FTX, ensure credentials are set correct, or check internet connectivity")	