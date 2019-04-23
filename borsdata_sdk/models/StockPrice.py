class StockPrice:
    i: int
    d: str
    h: int
    l: int
    c: int
    o: int
    v: int

    def __init__(self, d, h, l, c, o, v, i=None):
        self.i = i
        self.d = d
        self.h = h
        self.l = l
        self.c = c
        self.o = o
        self.v = v
