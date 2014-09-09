from __future__ import absolute_import
from __future__ import unicode_literals

try:
    from urllib.request import urlopen  # pragma: no cover
    from urllib.parse import urlparse   # pragma: no cover
    from urllib.parse import urljoin    # pragma: no cover
except ImportError:                     # pragma: no cover
    from urlparse import urlparse       # pragma: no cover
    from urlparse import urljoin        # pragma: no cover
    from urllib import urlopen          # pragma: no cover

from requests import Session
from requests import Request

from .resources import Ticker
from .resources import OrderBook
from .resources import Transaction
from .resources import ConversionRate

from .exceptions import ParametersError


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

    def get_order_book(self, group=True):
        if group not in [True, False]:
            raise ParametersError('"group" parameter must be a boolean.')
        group = 1 if group else 0

        request = Request(
            'GET', urljoin(self.url, 'order_book'), params={'group': group})
        response = self._send(request)
        return OrderBook(**response.json())

    def get_transactions(self, time="hour"):
        if time not in ["hour", "minute"]:
            raise ParametersError(
                '"time" parameter must be "hour" or "minute".')

        request = Request(
            'GET', urljoin(self.url, 'transactions'), params={'time': time})
        response = self._send(request)
        transactions = []
        for transaction in response.json():
            transactions.append(Transaction(**transaction))
        return transactions

    def get_conversion_rate(self, src="eur", dst="usd"):
        src = src.lower()
        dst = dst.lower()

        if src not in ConversionRate.ALL_SRC:
            raise ParametersError(
                '"src" parameter must be one of "%s"' % ','.join(
                    ConversionRate.ALL_SRC))
        if dst not in ConversionRate.ALL_DST:
            raise ParametersError(
                '"dst" parameter must be one of "%s"' % ','.join(
                    ConversionRate.ALL_DST))

        request = Request('GET', urljoin(self.url, '%s_%s' % (src, dst)))
        response = self._send(request)
        return ConversionRate(src, dst, **response.json())
