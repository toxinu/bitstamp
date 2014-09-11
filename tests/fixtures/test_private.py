from __future__ import absolute_import
from __future__ import unicode_literals
import unitttest

import vcr
import requests

from __init__ import FIXTURES_PATH

from bitstamp import Bitstamp

from bitstamp.exceptions import MissingCredentials


class PrivateTestCase(unittest.TestCase):
    def setUp(self):
        requests.packages.urllib3.disable_warnings()
        self.api = Bitstamp()

    # TODO
    def test_private_with_credentials(self):
        pass

    def test_private_without_credentials(self):
        api = Bitstamp()
        self.assertRaises(MissingCredentials, api.get_account_balance)
