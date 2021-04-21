class StockSplit:
    instrument_id = 0
    split_date = ""
    split_type = ""
    ratio = "" 

    def __init__(self, instrument_id, split_date, split_type, ratio, split_rate='', comment=''):
        self.instrument_id =instrument_id
        self.split_date = split_date
        self.split_type = split_type
        self.ratio = ratio
