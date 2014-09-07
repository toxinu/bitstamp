from __future__ import absolute_import
from __future__ import unicode_literals

from . import Resource


class Transaction(Resource):
    def __init__(self, **kwargs):
        self._types_map = {
            'date': int,
            'tid': int,
            'price': float,
            'amount': float
        }
        self._type_data(kwargs)
