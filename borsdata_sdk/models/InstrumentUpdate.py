class InstrumentUpdate:
    insId: int
    updatedAt: str

    def __init__(self, insId, updatedAt):
        self.insId = insId
        self.updatedAt = updatedAt

    def __str__(self):
        return '{}: {}'.format(self.insId, self.updatedAt)

    def __repr__(self):
        return '{}: {}'.format(self.insId, self.updatedAt)
