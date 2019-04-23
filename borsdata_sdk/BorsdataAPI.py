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
        self._markets = [Market(**market) for market in self.get_data('markets')]

        return self._markets

    def get_branches(self):
        return [Branch(**branch) for branch in self.get_data('branches')]

    def get_sectors(self):
        return [Sector(**sector) for sector in self.get_data('sectors')]

    def get_instruments(self, markets=None) -> List[Instrument]:
        instruments = [Instrument(**instrument) for instrument in self.get_data('instruments')]

        if markets is None:
            return instruments

        filtered_instruments = []

        for instrument in instruments:
            if instrument.marketId in markets:
                filtered_instruments.append(instrument)

        return filtered_instruments

    def get_instrument_stockprice(self, ins_id, start=None, end=None):
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

    def get_data(self, data_type):
        while True:
            # TODO: consider multiprocess reqs dut to GIL.d
            res = get(self._root + data_type, self._params, verify=False)

            if res.status_code != RATE_LIMIT:
                break

            sleep(0.3)

        data = loads(res.content)

        return data.get(data_type)
