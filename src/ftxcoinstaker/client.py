# src/ftxcoinstaker/client.py

import time
import urllib.parse

from requests import Request, Session, Response
import hmac

class FtxClient:

	_ENDPOINT = 'https://ftx.com/api/'

	def __init__(self, api_key=None, api_secret=None, subaccount_name=None):
		self._session = Session()
		self._api_key = api_key
		self._api_secret = api_secret
		self._subaccount_name = subaccount_name

	def _get(self, path: str, params=None):
		return self._request('GET', path, params=params)

	def _post(self, path: str, params=None):
		return self._request('POST', path, params=params)

	def _delete(self, path: str, params=None):
		return self._request('DELETE', path, json=params)

	def _request(self, method: str, path: str, **kwargs):
		request = Request(method, self._ENDPOINT + path, **kwargs)
		self._sign_request(request)
		final = request.prepare()
		final.params = dict(nickname="test")
		print(vars(final))
		response = self._session.send(final)
		return self._process_response(response)

	def _sign_request(self, request: Request):
		ts = int(time.time() * 1000)
		prepared = request.prepare()
		signature_payload = f'{ts}{prepared.method}{prepared.path_url}'.encode()
		if prepared.body:
			signature_payload += prepared.body
		signature = hmac.new(self._api_secret.encode(), signature_payload, 'sha256').hexdigest()
		request.headers['FTX-KEY'] = self._api_key
		request.headers['FTX-SIGN'] = signature
		request.headers['FTX-TS'] = str(ts)
		if self._subaccount_name:
			request.headers['FTX-SUBACCOUNT'] = urllib.parse.quote(self._subaccount_name)

	def _process_response(self, response: Response):
		try:
			data = response.json()
			print('---')
			print(data)
			print('---')
		except ValueError:
			response.raise_for_status()
			raise
		else:
			if not data['success']:
				raise Exception(data['error'])
			return data['result']

	def get_account_info(self):
		return self._get(f'account')

	def get_wallet_balances(self):
		return self._get('wallet/balances')

	def get_wallet_all_balances(self):
		return self._get('wallet/all_balances')

	# SUBACCOUNTS

	def get_subaccounts(self):
		return self._get('subaccounts')

	def update_subaccount_name(self, nickname: str, newNickname: str):
		return self._post('subaccounts/update_name', {"nickname": nickname,
													  "newNickname": newNickname
													 })

	def create_subaccount(self, nickname: str):
		return self._post('subaccounts', {"nickname": nickname})
