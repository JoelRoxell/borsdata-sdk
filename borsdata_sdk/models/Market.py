class Market:
    id: int
    name: str
    countryId: int
    isIndex: bool
    exchangeName: str

    def __init__(self, id, name, countryId, isIndex, exchangeName):
        self.id = id
        self.name = name
        self.countryId = countryId
        self.isIndex = isIndex
        self.exchangeName = exchangeName
