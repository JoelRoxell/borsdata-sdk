from unittest import TestCase
from os import getenv

from borsdata_sdk.BorsdataAPI import BorsdataAPI


class TestBorsdataAPI(TestCase):
    def setUp(self):
        self.api = BorsdataAPI(getenv('BORSDATA_API_KEY'))

    def test_get_markets(self):
        self.assertTrue(len(self.api.get_markets()) > 0)

    def test_get_branches(self):
        self.assertTrue(len(self.api.get_branches()) > 0)

    def test_get_sectors(self):
        self.assertTrue(len(self.api.get_sectors()) > 0)

    def test_get_instruments(self):
        self.assertTrue(len(self.api.get_instruments()) > 0)

    def test_get_instrument_stockprice_all(self):
        entries = self.api.get_instrument_stockprice(3)

        self.assertTrue(len(entries) > 0)
        self.assertTrue(entries[0].get('d') == '2009-04-22')

    def test_get_instrument_stockprice_from_to(self):
        entries = self.api.get_instrument_stockprice(3, '2009-04-22', '2009-04-25')

        self.assertTrue(len(entries) == 3)