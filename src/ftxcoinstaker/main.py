# src/ftxcoinstaker/main.py

import os
import glob
import yaml
from . import coinstaker
from multiprocessing import Process
from typing import Optional, Dict, Any, List
from pprint import pprint

def main() -> None:
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