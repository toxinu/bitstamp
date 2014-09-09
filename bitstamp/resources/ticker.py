from __future__ import absolute_import
from __future__ import unicode_literals

from . import Resource
from . import TimestampResource


class Ticker(Resource, TimestampResource):
    def __init__(self, **kwargs):
        self._types_map = {
            'last': float,
            'high': float,
            'low': float,
            'vwap': float,
            'volume': float,
            'bid': float,
            'ask': float,
            'timestamp': int
        }
        self._type_data(kwargs)

        super(Ticker, self).__init__()
