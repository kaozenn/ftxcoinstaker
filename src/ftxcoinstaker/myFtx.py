# src/ftxcoinstaker/myFtx.py
import ftx
from typing import Optional, Dict, Any, List

class MyFtxClient(ftx.FtxClient):

    @ftx.FtxClient.authentication_required
    def get_quote_status(self, quote_id) -> List[dict]:
        return self._get(f'otc/quotes/{quote_id}')

    @ftx.FtxClient.authentication_required
    def accept_quote(self, quote_id) -> List[dict]:
        return self._post(f'otc/quotes/{quote_id}/accept')