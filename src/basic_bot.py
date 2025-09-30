import time, hmac, hashlib
import requests
from urllib.parse import urlencode

class BasicBot:
    def __init__(self, api_key: str, api_secret: str, testnet: bool = True, recv_window: int = 5000, dry_run: bool = False):
        self.api_key = api_key
        self.api_secret = api_secret.encode('utf-8') if api_secret else None
        self.testnet = testnet
        self.recv_window = recv_window
        self.dry_run = dry_run
        self.base_url = 'https://testnet.binancefuture.com' if testnet else 'https://fapi.binance.com'
        self.session = requests.Session()
        if api_key:
            self.session.headers.update({'X-MBX-APIKEY': api_key})

    def _timestamp(self):
        return int(time.time() * 1000)

    def _sign(self, params: dict):
        query = urlencode(params)
        signature = hmac.new(self.api_secret, query.encode('utf-8'), hashlib.sha256).hexdigest()
        return f"{query}&signature={signature}"

    def _send_signed_request(self, method: str, path: str, params: dict):
        params = params or {}
        params.update({"timestamp": self._timestamp(), "recvWindow": self.recv_window})
        if not self.api_secret:
            raise ValueError('API secret not provided for a signed request.')
        query_string = self._sign(params)
        url = self.base_url + path + '?' + query_string
        if self.dry_run:
            # In dry run mode, do not actually call Binance. Return simulated response.
            return {'mock': True, 'url': url, 'method': method, 'params': params}
        resp = self.session.request(method, url, timeout=10)
        try:
            data = resp.json()
        except Exception:
            data = resp.text
        if not resp.ok:
            raise Exception(f"API request failed: {resp.status_code} {data}")
        return data

    def place_order(self, symbol: str, side: str, order_type: str, quantity: float, price: float = None, stopPrice: float = None, timeInForce: str = 'GTC', reduceOnly: bool = False, closePosition: bool = False):
        path = '/fapi/v1/order'
        side = side.upper()
        order_type = order_type.upper()

        params = {
            'symbol': symbol.upper(),
            'side': side,
            'type': order_type,
            'quantity': quantity,
            'reduceOnly': str(reduceOnly).lower(),
        }

        if order_type == 'LIMIT':
            if price is None:
                raise ValueError('Price is required for LIMIT orders')
            params.update({'price': price, 'timeInForce': timeInForce})
        if order_type in ('STOP', 'STOP_MARKET', 'TAKE_PROFIT', 'TAKE_PROFIT_MARKET'):
            if stopPrice is None:
                raise ValueError('stopPrice is required for conditional orders (STOP / TAKE_PROFIT variants)')
            params.update({'stopPrice': stopPrice})
            if closePosition:
                params.update({'closePosition': 'true'})

        return self._send_signed_request('POST', path, params)
