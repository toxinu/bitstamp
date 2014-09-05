from __future__ import absolute_import
from __future__ import unicode_literals

from . import Resource
from . import TimestampResource


class OrderBook(Resource, TimestampResource):
    def __init__(self, **kwargs):
        self._types_map = {
            'timestamp': int
        }
        self._type_data(kwargs)

        # Convert list of list of two string _to_ tuple of tuple of two float
        self.bids = tuple(tuple((float(x[0]), float(x[1]))) for x in self.bids)
