from __future__ import absolute_import
from __future__ import unicode_literals

from . import Resource


class ConversionRate(Resource):
    ALL_SRC = ('eur', )
    ALL_DST = ('usd', )

    def __init__(self, src, dst, **kwargs):
        self.currencies = (src, dst)

        self._types_map = {
            'buy': float,
            'sell': float
        }
        self._type_data(kwargs)
