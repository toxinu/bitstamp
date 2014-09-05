from __future__ import absolute_import
from __future__ import unicode_literals

from . import Resource
from . import TimestampResource


class Transaction(Resource, TimestampResource):
    def __init__(self, **kwargs):
        self._types_map = {}
        self._type_data(kwargs)
