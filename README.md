# Borsdata python SKD

> unofficial

python SDK for the [Börsdata API](https://github.com/Borsdata-Sweden/API). Note that all endpoints are not yet implemented -> [API](https://apidoc.borsdata.se/swagger/index.html).

## Install
`pip install borsdata-sdk`

## Usage

```python
from borsdata_sdk import BorsdataAPI

borsdata = BorsdataAPI('<api_key>')

markets = borsdata.get_markets()
branches = borsdata.get_branches()
sectors = borsdata.get_sectors()
instruments = borsdata.get_instruments()
entries = borsdata.get_instrument_stock_price(3)
entries_from_to = borsdata.get_instrument_stock_price(3, '2009-04-22', '2009-04-25')
list_of_updated_instruments = borsdata.get_instrument_stock_price_last()
```
