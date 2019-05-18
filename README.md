# Borsdata python SKD

[![Build Status](https://travis-ci.com/JoelRoxell/borsdata-sdk.svg?branch=master)](https://travis-ci.com/JoelRoxell/borsdata-sdk)

> unofficial

python SDK for the [Börsdata API](https://github.com/Borsdata-Sweden/API). Note that all endpoints are not yet implemented -> [API](https://apidoc.borsdata.se/swagger/index.html).

## Install

`pip install borsdata-sdk`

## Usage

```python
from borsdata_sdk import BorsdataAPI

borsdata = BorsdataAPI('<api_key>')

# Meta
markets = borsdata.get_markets()
branches = borsdata.get_branches()
countries = borsdata.get_countries()
sectors = borsdata.get_sectors()

# All stocks
instruments = borsdata.get_instruments()

# Entries for stock with insId == 3
entries = borsdata.get_instrument_stock_price(3)
entries_from_to = borsdata.get_instrument_stock_price(3, '2009-04-22', '2009-04-25')

# Updated instruments
updated_instruments = borsdata.get_instruments_updated()

# Last entries of updated instruments
list_of_updated_instruments = borsdata.get_instrument_stock_price_last()

# Reports
yearly_reports = borsdata.get_instrument_reports(3, 'year')
r12s = borsdata.get_instrument_reports(3, 'r12')
quarters = borsdata.get_instrument_reports(3, 'quarter')
```
