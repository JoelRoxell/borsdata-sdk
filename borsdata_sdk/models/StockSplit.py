class StockSplit:
    instrumentId: int
    splitRate: int
    comment: str
    splitDate: str
    splitType: str
    ratio: str

    def __init__(self, instrumentId, splitDate, splitType, ratio, splitRate='', comment=''):
        self.instrumentId = instrumentId
        self.splitRate = splitRate
        self.comment = comment
        self.splitDate = splitDate
        self.splitType = splitType
        self.ratio = ratio
