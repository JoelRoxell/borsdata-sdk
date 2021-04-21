# Borsdata python SKD

[![Build Status](https://travis-ci.com/JoelRoxell/borsdata-sdk.svg?branch=master)](https://travis-ci.com/JoelRoxell/borsdata-sdk)

> unofficial

python SDK for the [Börsdata API](https://github.com/Borsdata-Sweden/API), [detailed docs](https://apidoc.borsdata.se/swagger/index.html).

## Install

`pip install borsdata-sdk`

## Usage

A simple example can be found [here](demo/stock-list-ex.ipynb).

```python
from borsdata_sdk import BorsdataAPI

borsdata = BorsdataAPI('<api_key>')

# Instrument Meta
markets = borsdata.get_markets()
branches = borsdata.get_branches()
sectors = borsdata.get_sectors()
countries = borsdata.get_countries()
translations = borsdata.get_translation_meta_data()

# Instruments
instruments = borsdata.get_instruments()
instruments = borsdata.get_instruments_by_market(markets=[1, 2])
updates =  borsdata.get_instruments_updated()

# KPIs
# In progress

# StockPrices
entries = borsdata.get_instrument_stock_price(3)
entries_from_to = borsdata.get_instrument_stock_price(3, '2009-04-22', '2009-04-25')
updates = borsdata.get_instrument_stock_price_last()
updates = borsdata.get_instruments_stock_prices_by_date("2021-04-20")

# Reports
yearly_reports = borsdata.get_instrument_reports(3, 'year')
r12s = borsdata.get_instrument_reports(3, 'r12')
quarters = borsdata.get_instrument_reports(3, 'quarter')
all_reports = borsdata.get_all_instrument_reports(77)
meta = borsdata.api.get_instruments_reports_meta_data()

# StockSplits
splits = borsdata.api.get_stock_splits()

```
