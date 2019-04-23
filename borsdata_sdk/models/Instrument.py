class Instrument:
    insId: int
    name: str
    urlName: str
    instrument: int
    isin: str
    ticker: str
    yahoo: str
    sectorId: int
    marketId: int
    branchId: int
    countryId: int
    listingDate: str

    def __init__(self, insId, name, urlName, instrument, isin, ticker, yahoo, sectorId, marketId, branchId, countryId,
                 listingDate):
        self.insId = insId
        self.name = name
        self.urlName = urlName
        self.instrument = instrument
        self.isin = isin
        self.ticker = ticker
        self.yahoo = yahoo
        self.sectorId = sectorId
        self.marketId = marketId
        self.branchId = branchId
        self.countryId = countryId
        self.listingDate = listingDate

    def __str__(self):
        return '{}: {}'.format(self.insId, self.name)

    def __repr__(self):
        return '{}: {}'.format(self.insId, self.name)
