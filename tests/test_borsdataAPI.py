from os import getenv
import unittest

from borsdata_sdk.BorsdataAPI import BorsdataAPI


class Test_TestBorsdataAPI(unittest.TestCase):
    def setUp(self):
        self.api = BorsdataAPI(getenv("BORSDATA_API_KEY"))

    # Instrument Meta
    def test_get_markets(self):
        self.assertTrue(len(self.api.get_markets()) > 0)

    def test_get_branches(self):
        self.assertTrue(len(self.api.get_branches()) > 0)

    def test_get_sectors(self):
        self.assertTrue(len(self.api.get_sectors()) > 0)

    def test_get_countries(self):
        countries = self.api.get_countries()

        self.assertTrue(len(countries) > 0)

    def test_get_translation_meta(self):
        translations = self.api.get_translation_meta_data()

        self.assertEqual(translations[0].get("nameEn"), "Financials")
        self.assertEqual(translations[0].get("translationKey"), "L_SECTOR_1")

    # Instruments
    def test_get_instruments(self):
        self.assertTrue(len(self.api.get_instruments()) > 0)

    def test_get_instruments_by_market(self):
        filtered_instruments = self.api.get_instruments(markets=[1, 2])

        self.assertTrue(len(filtered_instruments) == 287)

    def test_get_instruments_last(self):
        updated_instruments = self.api.get_instruments_updated()

        self.assertTrue(len(updated_instruments) > 0)

    # Kpis
    # In progress...

    # StockPrices
    def test_get_instrument_stock_price_all(self):
        self.assertTrue(len(self.api.get_instrument_stock_price(3)) > 0)

    def test_get_instrument_stockprice_from_to(self):
        entries = self.api.get_instrument_stock_price(
            77, "2020-04-22", "2020-04-30"
        )  # ericsson
        self.assertEqual(len(entries), 7)

    def test_get_instrument_stock_price_last(self):
        updates = self.api.get_instrument_stock_price_last()
        self.assertTrue(len(updates) > 0)

    def test_get_instruments_by_date(self):
        instruments = self.api.get_instruments_stock_prices_by_date("2021-04-20")

        self.assertGreater(len(instruments), 0)

    # Reports
    def test_get_instruments_reports(self):
        yearly_reports = self.api.get_instrument_reports(3, "year")
        r12s = self.api.get_instrument_reports(3, "r12")
        quarters = self.api.get_instrument_reports(3, "quarter")

        self.assertTrue(yearly_reports[-1].year == 2010)
        self.assertTrue(r12s[-1].year == 2018)
        self.assertTrue(quarters[-1].year == 2018)

    def test_get_all_instrument_reports(self):
        reports = self.api.get_all_instrument_reports(77)

        instrument_id = reports.get("instrument")

        self.assertTrue(instrument_id == 77)
        self.assertTrue(len(reports) == 4)

    def test_get_instruments_reports_meta_data(self):
        data = self.api.get_instruments_reports_meta_data()

        first = data[0]

        self.assertEqual(first.get("nameSv"), "Brutet räkenskapsår")
        self.assertEqual(first.get("nameEn"), "Broken fiscal year")

    # StockSplits
    def test_get_instrument_stock_split(self):
        splits = self.api.get_stock_splits()

        self.assertEqual(splits[0].instrument_id, 761)
        self.assertEqual(splits[0].split_type, "RS")
        self.assertEqual(splits[0].ratio, "1:100")
        self.assertEqual(splits[0].split_date, "2020-04-30T00:00:00")


if __name__ == "__main__":
    unittest.main()
