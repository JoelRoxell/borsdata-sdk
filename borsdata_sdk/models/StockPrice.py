class StockPrice:
    i = 0.0
    d = ""
    h = 0.0
    l = 0.0
    c = 0.0
    o = 0.0
    v = 0.0

    def __init__(self, d, h, l, c, o, v, i=None):
        self.i = i
        self.d = d
        self.h = h
        self.l = l
        self.c = c
        self.o = o
        self.v = v
