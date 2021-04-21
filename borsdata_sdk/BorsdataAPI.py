from time import sleep
from typing import List, Tuple
from http import HTTPStatus
from requests import get
import logging

from .models.Branch import Branch
from .models.Instrument import Instrument
from .models.InstrumentUpdate import InstrumentUpdate
from .models.Market import Market
from .models.Sector import Sector
from .models.StockPrice import StockPrice
from .models.Country import Country
from .models.StockSplit import StockSplit
from .models.Report import Report
from .APIError import APIError
from .utils.transform import transform_dict_props_to_lower

RATE_LIMIT = 429
RATE_WAIT = 0.3
UPDATED = True


class BorsdataAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self._params = {"authKey": self.api_key}
        self._uri = "https://apiservice.borsdata.se"
        self._version = "v1"
        self._root = "{host}/{version}".format(host=self._uri, version=self._version)

    def get_instrument_reports(
        self, instrument_id: int, type="quarter"
    ) -> List[Report]:
        """Get reports for provided instrument

        Args:
            insId (str): instrument id
            type (str, optional): report type, one of year|quarter|r12. Defaults to 'quarter'.

        Raises:
            APIError: generic com. error

        Returns:
            List[Report]: list of Reports
        """

        status, data = self._get(f"/instruments/{instrument_id}/reports/{type}")

        if status != HTTPStatus.OK:
            raise APIError

        return [
            Report(**transform_dict_props_to_lower(report))
            for report in data.get("reports", [])
        ]

    def get_all_instrument_reports(
        self, instrument_id: int, max_year_count=10, max_r12q_count=10
    ) -> dict:
        """Returns reports for instrument. All reports type included (year, r12, quarter).
        Note the returned type is not tranformed to a python object.

        Args:
            instrument_id (int): instrument
            max_year_count (int, optional): # reports limit. Defaults to 10.
            max_r12q_count (int, optional): # reports limit. Defaults to 10.

        Returns:
            dict: containing all reports for instrument
        """
        _, data = self._get(
            f"/instruments/{instrument_id}/reports",
            {"mayYearCount": max_year_count, "maxR12QCount": max_r12q_count},
        )

        return data

    def get_instruments_reports_meta_data(self) -> List[dict]:
        _, data = self._get("/instruments/reports/metadata")

        return data.get("reportMetadatas")

    def get_markets(self) -> List[Market]:
        """Returns all markets.

        Returns:
            List[Market] -- List of markets.
        """

        return [Market(**market) for market in self._get_data_object("markets")]

    def get_branches(self) -> List[Branch]:
        return [Branch(**branch) for branch in self._get_data_object("branches")]

    def get_sectors(self) -> List[Sector]:
        """Returns all sectors.

        Returns:
            List[Sector] -- List of sectors.
        """

        return [Sector(**sector) for sector in self._get_data_object("sectors")]

    def get_countries(self) -> List[Country]:
        """Return all countries.

        Returns:
            List[Country] -- Lost of countires.
        """

        return [Country(**country) for country in self._get_data_object("countries")]

    def get_translation_meta_data(self):
        translations = self._get_data_object("translationMetadata")

        return translations.get("translationMetadatas")

    def get_instruments(self, markets: List[int] = None) -> List[Instrument]:
        """Returns all instruments.

        Keyword Arguments:
            markets {int[]} -- Id list of markets used to filter
            the resulting list (default: {None}).

        Returns:
            List[Instrument] -- List of instruments.
        """

        instruments = [
            Instrument(**instrument)
            for instrument in self._get_data_object("instruments")
        ]

        if markets is None:
            return instruments

        filtered_instruments = []

        for instrument in instruments:
            if instrument.marketId in markets:
                filtered_instruments.append(instrument)

        return filtered_instruments

    def get_instruments_updated(self) -> List[InstrumentUpdate]:
        """Returns all updated instruments.

        Returns:
            List[InstrumentUpdate] -- List of all updated instruments.
        """

        _, data = self._get("/instruments/updated")

        return [
            InstrumentUpdate(**instrument) for instrument in data.get("instruments")
        ]

    def get_instrument_stock_price(
        self, ins_id: str, start: str = None, end: str = None, count: int = 20
    ):
        """Returns stockprices for an instrument (ins_id),
           it is possible to determine the timespan using start and end.
           Max 10 years, if no time filters provided.

        Arguments:
            ins_id {int} -- Instrument id.

        Keyword Arguments:
            start {str} --  Determines from which day to start the collection,
                ex: '2009-04-22' (default: {None})
            end {str} --  Determines the collection limit, ex:'2009-04-25',
                (default: {None})

        Raises:
            APIError: Thrown if the API responds with anything other than 200.

        Returns:
            List[StockPrice] -- List of the collected stockprices.
        """

        self._params.update({"from": start, "to": end, "maxCount": count})
        status, data = self._get(f"/instruments/{ins_id}/stockprices")

        if status != HTTPStatus.OK:
            raise APIError(f"api returned status: {status}")

        entries = [
            StockPrice(**transform_dict_props_to_lower(entry))
            for entry in data.get("stockPricesList")
        ]

        return entries

    def get_instrument_stock_price_last(self) -> List[StockPrice]:
        """Returns Last StockPrices for all instruments.

        Returns:
            List[StockPrice] -- List of all last updated price.
        """

        _, data = self._get("/instruments/stockprices/last")

        return [
            StockPrice(**transform_dict_props_to_lower(entry))
            for entry in data.get("stockPricesList", [])
        ]

    def get_instruments_stock_prices_by_date(self, date: str) -> List[StockPrice]:
        """Returns one stockprice for each instrument for the given date

        Args:
            date (str): day

        Returns:
            List[StockPrice]: stockprices
        """
        _, data = self._get("/instruments/stockprices/date", {"date": date})

        return [
            StockPrice(**transform_dict_props_to_lower(entry))
            for entry in data.get("stockPricesList", [])
        ]

    def get_stock_splits(self) -> List[StockSplit]:
        """Returns Stock Splits for all Instruments. Max 1 Year.

        Returns:
            List[StockSplit] --
        """
        _, data = self._get("/instruments/StockSplits")

        return [
            StockSplit(**transform_dict_props_to_lower(split))
            for split in data.get("stockSplitList")
        ]

    def _get_data_object(self, data_type: str):
        """Gets the specified datatype from the remote API.
        Transformes it to a proper data object if possible,
        otherwise the entire response payload is returned.

        Arguments:
            data_type {str} -- Datatype.

        Raises:
            APIError: Thrown if the API responds with anything other than 200.

        Returns:
            List[T] - List of the passed type.
        """
        _, data = self._get(f"/{data_type}")

        inner_data = data.get(data_type)

        if not inner_data:
            return data

        return inner_data

    def _get(self, endpoint, query_params={}) -> Tuple[int, dict]:
        """Perform a remote request to the API and retries on rate limit responses, returns json payload on success.

        Arguments:
            endpoint {str} -- endpoint to access, ex: `instruments/StockSplits`.

        Returns:
            (int, dict) -- The first entry, holds the status code of the response; the second, holds the response content parsed from json.
        """

        while True:
            target = self._root + endpoint

            logging.info(f"requesting resource: {target}")

            _query_params = self._params.copy()
            _query_params.update(query_params)

            res = get(target, _query_params, verify=False)
            status = res.status_code

            if status == HTTPStatus.OK:
                return res.status_code, res.json()

            if status != RATE_LIMIT:
                raise APIError(f"borsdata api responded with {res}")

            sleep(RATE_WAIT)
