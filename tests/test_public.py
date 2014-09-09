from __future__ import absolute_import
from __future__ import unicode_literals
import os
import datetime
import unittest

import vcr
import requests

from __init__ import FIXTURES_PATH

from bitstamp import Bitstamp

from bitstamp.resources import Ticker
from bitstamp.resources import OrderBook
from bitstamp.resources import Transaction
from bitstamp.resources import ConversionRate

from bitstamp.exceptions import ParametersError


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

        self.assertTrue(ticker_01 > ticker_02)
        self.assertTrue(ticker_02 < ticker_01)
        self.assertFalse(ticker_02 < ticker_02)
        self.assertFalse(ticker_01 > ticker_01)

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

    def test_order_book_group(self):
        with vcr.use_cassette(os.path.join(FIXTURES_PATH, 'orders_book.yaml')):
            order_book_01 = self.api.get_order_book()

        with vcr.use_cassette(os.path.join(FIXTURES_PATH, 'orders_book.yaml')):
            order_book_02 = self.api.get_order_book(group=True)
            self.assertEqual(order_book_01, order_book_02)

            order_book_03 = self.api.get_order_book(group=False)
            self.assertNotEqual(
                len(order_book_01.bids), len(order_book_03.bids))
            self.assertLess(len(order_book_01.bids), len(order_book_03.bids))

    def test_order_book_bad_group(self):
        self.assertRaises(
            ParametersError, self.api.get_order_book, group='yeah')
        self.assertRaises(
            ParametersError, self.api.get_order_book, group=[1, 2])

    def test_transaction_get(self):
        with vcr.use_cassette(os.path.join(FIXTURES_PATH, 'transaction.yaml')):
            transactions = self.api.get_transactions()
            self.assertIsInstance(transactions, list)
            self.assertTrue(
                all(isinstance(t, Transaction) for t in transactions))

    def test_transaction_time(self):
        with vcr.use_cassette(os.path.join(FIXTURES_PATH, 'transaction.yaml')):
            transactions_01 = self.api.get_transactions()

        with vcr.use_cassette(os.path.join(FIXTURES_PATH, 'transaction.yaml')):
            transactions_02 = self.api.get_transactions(time="hour")
            self.assertEqual(len(transactions_01), len(transactions_02))

            transactions_03 = self.api.get_transactions(time="minute")
            self.assertNotEqual(
                len(transactions_01), len(transactions_03))

    def test_transaction_bad_time(self):
        self.assertRaises(
            ParametersError, self.api.get_transactions, time='yeah')
        self.assertRaises(
            ParametersError, self.api.get_transactions, time=[1, 2])

    def test_conversion_rate_get(self):
        with vcr.use_cassette(
                os.path.join(FIXTURES_PATH, 'conversion_rate.yaml')):
            conversion_rate = self.api.get_conversion_rate()
            self.assertIsInstance(conversion_rate, ConversionRate)
            self.assertEqual(conversion_rate.currencies, ('eur', 'usd'))

    def test_conversion_rate_bad_src(self):
        self.assertRaises(
            ParametersError, self.api.get_conversion_rate, src='yeah')

    def test_conversion_rate_bad_dst(self):
        self.assertRaises(
            ParametersError, self.api.get_conversion_rate, dst='yeah')
