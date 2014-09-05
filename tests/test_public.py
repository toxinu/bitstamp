from __future__ import absolute_import
from __future__ import unicode_literals
import os
import sys
import datetime
import unittest

import vcr
import requests

sys.path.append("../bitstamp")

from __init__ import FIXTURES_PATH
from bitstamp import Bitstamp
from bitstamp.resources import Ticker
from bitstamp.resources import OrderBook
from bitstamp.resources import Transaction


class PublicTestCase(unittest.TestCase):
    def setUp(self):
        requests.packages.urllib3.disable_warnings()
        self.api = Bitstamp()

    def test_timestamp_resource_compare(self):
        with vcr.use_cassette(os.path.join(FIXTURES_PATH, 'ticker_01.yaml')):
            ticker_01 = self.api.get_ticker()
        with vcr.use_cassette(os.path.join(FIXTURES_PATH, 'ticker_02.yaml')):
            ticker_02 = self.api.get_ticker()

        self.assertNotEqual(ticker_01, ticker_02)
        self.assertGreater(ticker_01, ticker_02)
        self.assertLess(ticker_02, ticker_01)

    def test_ticker_get(self):
        with vcr.use_cassette(os.path.join(FIXTURES_PATH, 'ticker_01.yaml')):
            ticker = self.api.get_ticker()
            self.assertIsInstance(ticker, Ticker)
            self.assertIsInstance(
                ticker.timestamp_as_datetime(), datetime.datetime)

    def test_order_book_get(self):
        with vcr.use_cassette(os.path.join(FIXTURES_PATH, 'orders_book.yaml')):
            order_book = self.api.get_order_book()
            self.assertIsInstance(order_book, OrderBook)

    def test_transaction_get(self):
        with vcr.use_cassette(os.path.join(FIXTURES_PATH, 'transaction.yaml')):
            transactions = self.api.get_transactions()
            import ipdb; ipdb.set_trace()
            self.assertIsInstance(transactions, list)

