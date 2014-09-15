from __future__ import absolute_import
from __future__ import unicode_literals

import datetime


class Resource(object):
    def _type_data(self, data):
        for key, value in data.items():
            _type = self._types_map.get(key, None)
            if _type:
                setattr(self, key, _type(value))
            else:
                setattr(self, key, value)


class TimestampResource(object):
    def __init__(self):
        if not hasattr(self, '_timestamp_attr'):
            self._timestamp_attr = 'timestamp'

        setattr(
            self,
            '%s_as_datetime' % self._timestamp_attr,
            lambda: datetime.datetime.fromtimestamp(
                getattr(self, self._timestamp_attr)))

    def __eq__(self, other):
        if hasattr(other, '%s_as_datetime' % self._timestamp_attr):
            if getattr(
                other, '%s_as_datetime' % other._timestamp_attr)() == getattr(
                    self, '%s_as_datetime' % self._timestamp_attr)():
                return True
        return False

    def __lt__(self, other):
        if hasattr(other, '%s_as_datetime' % self._timestamp_attr):
            if getattr(
                other, '%s_as_datetime' % other._timestamp_attr)() < getattr(
                    self, '%s_as_datetime' % self._timestamp_attr)():
                return True
        return False

from .ticker import Ticker
from .order_book import OrderBook
from .transaction import Transaction
from .conversion_rate import ConversionRate

from .account_balance import AccountBalance
