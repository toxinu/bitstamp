from __future__ import absolute_import
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
    def timestamp_as_datetime(self):
        return datetime.datetime.fromtimestamp(self.timestamp)

    def __eq__(self, other):
        if hasattr(other, 'timestamp_as_datetime'):
            if other.timestamp_as_datetime() == self.timestamp_as_datetime():
                return True
        return False

    def __lt__(self, other):
        if hasattr(other, 'timestamp_as_datetime'):
            if other.timestamp_as_datetime() < self.timestamp_as_datetime():
                return True
        return False

from .ticker import Ticker
from .order_book import OrderBook
from .transaction import Transaction
