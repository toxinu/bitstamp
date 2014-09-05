from __future__ import absolute_import
from __future__ import unicode_literals

try:
    from urllib.request import urlopen
    from urllib.parse import urlparse
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urlparse
    from urlparse import urljoin
    from urllib import urlopen

from requests import Session
from requests import Request

from .resources import Ticker
from .resources import OrderBook
from .resources import Transaction


class Bitstamp(object):
    def __init__(self):
        self.url = 'https://www.bitstamp.net/api/'
        self.session = Session()

    def _send(self, request):
        if not request.url.endswith('/'):
            request.url += '/'

        prepped = request.prepare()
        return self.session.send(prepped, verify=True)

    def get_ticker(self):
        request = Request('GET', urljoin(self.url, 'ticker'))
        response = self._send(request)
        return Ticker(**response.json())

    def get_order_book(self):
        request = Request('GET', urljoin(self.url, 'order_book'))
        response = self._send(request)
        return OrderBook(**response.json())

    def get_transactions(self):
        request = Request('GET', urljoin(self.url, 'transactions'))
        response = self._send(request)
        transactions = []
        for transaction in response.json():
            transactions.append(Transaction(**transaction))
        return transactions
