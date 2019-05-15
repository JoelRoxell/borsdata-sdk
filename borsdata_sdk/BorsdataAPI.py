from json import loads
from time import sleep
from typing import List

from requests import get

from borsdata_sdk.models.Branch import Branch
from borsdata_sdk.models.Instrument import Instrument
from borsdata_sdk.models.Market import Market
from borsdata_sdk.models.Sector import Sector
from borsdata_sdk.models.StockPrice import StockPrice

RATE_LIMIT = 429


class BorsdataAPI:
    _markets: List[Market]
    _instruments: List[Instrument]

    def __init__(self, api_key):
        self.api_key = api_key
        self._params = {'authKey': self.api_key}
        self._uri = 'https://apiservice.borsdata.se'
        self._version = 'v1'
        self._root = '{host}/{version}/'.format(host=self._uri, version=self._version)
        self._markets = None
        self._instruments = None

    @property
    def markets(self) -> List[Market]:
        if self._markets is None:
            self._markets = self.get_markets()

        return self._markets

    def get_markets(self) -> List[Market]:
        self._markets = [Market(**market) for market in self._get_data_object('markets')]

        return self._markets

    def get_branches(self):
        return [Branch(**branch) for branch in self._get_data_object('branches')]

    def get_sectors(self):
        return [Sector(**sector) for sector in self._get_data_object('sectors')]

    def get_instruments(self, markets=None) -> List[Instrument]:
        instruments = [Instrument(**instrument) for instrument in self._get_data_object('instruments')]

        if markets is None:
            return instruments

        filtered_instruments = []

        for instrument in instruments:
            if instrument.marketId in markets:
                filtered_instruments.append(instrument)

        return filtered_instruments

    def get_instrument_stock_price(self, ins_id, start=None, end=None):
        params = self._params.copy()

        while True:
            if start and end:
                params.update({'from': start, 'to': end})

            res = get(self._root + 'instruments/{}/stockprices'.format(ins_id), params=params, verify=False)

            if res.status_code != 200 and not res.status_code == RATE_LIMIT:
                raise IOError('Failed to communicate with the borsdata api')

            if res.status_code == 200:
                break

            sleep(0.3)

        entries = [StockPrice(**entry) for entry in loads(res.content).get('stockPricesList')]

        return entries

    def get_instrument_stock_price_last(self) -> List[StockPrice]:
        """ Returns Last StockPrices for all instruments.
        """
        status, data = self._get('instruments/stockprices/last')

        return [StockPrice(**entry) for entry in data.get('stockPricesList', [])]

    def _get_data_object(self, data_type):
        status, data = self._get(data_type)

        if status != 200:
            raise IOError(f'Failed to communicate with {self._root}{data_type} status: {status}')

        return data.get(data_type)

    def _get(self, endpoint):
        while True:
            res = get(self._root + endpoint, self._params, verify=False)

            if res.status_code != RATE_LIMIT:
                break

            sleep(0.3)

        return res.status_code, res.json()
