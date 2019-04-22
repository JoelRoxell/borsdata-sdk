from requests import get
from json import loads
from time import sleep


RATE_LIMIT = 429


class BorsdataAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self._params = {'authKey': self.api_key}
        self._uri = 'https://apiservice.borsdata.se'
        self._version = 'v1'
        self._root = '{host}/{version}/'.format(host=self._uri, version=self._version)

    def get_markets(self):
        return self.get_data('markets')

    def get_branches(self):
        return self.get_data('branches')

    def get_sectors(self):
        return self.get_data('sectors')

    def get_instruments(self):
        return self.get_data('instruments')

    def get_instrument_stockprice(self, ins_id, start=None, end=None):
        while True:
            if start and end:
                self._params.update({ 'from': start, 'to': end })

            res = get(self._root + 'instruments/{}/stockprices'.format(ins_id), params=self._params, verify=False)

            if res.status_code != 200 and not res.status_code == RATE_LIMIT:
                raise IOError('Failed to communicate with the borsdata api')

            if res.status_code == 200:
                break

        entries = loads(res.content).get('stockPricesList')

        return entries

    def get_data(self, data_type):
        while True:
            # TODO: consider multiprocess reqs dut to GIL.
            res = get(self._root + data_type, self._params, verify=False)

            if res.status_code != RATE_LIMIT:
                break

            sleep(1)

        data = loads(res.content)

        return data.get(data_type)
