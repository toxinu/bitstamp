from __future__ import absolute_import
from __future__ import unicode_literals

import time
import hmac
import hashlib

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
from .exceptions import MissingCredentials


class Bitstamp(object):
    """
        This class is Bitstamp API module, you have to use it to access every
        resources of Bitstamp.

        Basic Usage::

            >>> from bitstamp import Bitstamp
            >>> api = Bitstamp('client_id', 'api_key', 'secret_key')
    """
    def __init__(self, client_id=None, api_key=None, secret_key=None):
        """
            :param client_id: (optionnal) Client id
            :param api_key: (optionnal) API key
            :param secret_key: (optionnal) Secret API key
            :type client_id: str
            :type api_key: str
            :type secret_key: str
        """
        self.url = 'https://www.bitstamp.net/api/'
        self.client_id = client_id
        self.api_key = api_key
        self.secret_key = secret_key
        self.session = Session()

    def _send(self, request, is_auth=False):
        if not request.url.endswith('/'):
            request.url += '/'

        if is_auth:
            if not self.client_id or not self.api_key or not self.secret_key:
                raise MissingCredentials(
                    'Add credentials with "auth" method or at instanciation.')

            nonce = str(int(time.time()))
            message = '%s%s%s' % (nonce, self.client_id, self.api_key)
            signature = hmac.new(
                self.secret_key,
                msg=message,
                digestmod=hashlib.sha256).hexdigest().upper()
            request.params.update(
                {'key': self.api_key, 'signature': signature, 'nonce': nonce})

        prepped = request.prepare()
        return self.session.send(prepped, verify=True)

    def auth(self, client_id, api_key, secret_key):
        """
            Allow you to set authentication informations after
            Bitstamp class instanciation.

            :param client_id: Client id
            :param api_key: API key
            :param secret_key: Secret API key
            :type client_id: str
            :type api_key: str
            :type secret_key: str

            :Example:

            >>> from bitstamp import Bitstamp
            >>> api = Bitstamp()
            >>> api.auth('client_id', 'api_key', 'secret_key')
        """
        self.api_key = api_key
        self.client_id = client_id
        self.secret_key = secret_key

    def get_ticker(self):
        """ Return a :class:`Ticker` """
        request = Request('GET', urljoin(self.url, 'ticker'))
        response = self._send(request)
        return Ticker(**response.json())

    def get_order_book(self, group=True):
        """
            Return a :class:`OrderBook`

            :param group: Group orders with the same price
            :type group: bool
        """
        if group not in [True, False]:
            raise ParametersError('"group" parameter must be a boolean.')
        group = 1 if group else 0

        request = Request(
            'GET', urljoin(self.url, 'order_book'), params={'group': group})
        response = self._send(request)
        return OrderBook(**response.json())

    def get_transactions(self, time="hour"):
        """
            Return a list of :class:`Transaction`

            :param time: Time frame for transactions.
                         It could be 'minute' or 'hour'.
            :type time: str
        """
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
        """
            Return a :class:`ConversionRate`

            :param src: Currency source
            :param dst: Currency destination
            :type src: str
            :type dst: str
        """
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
