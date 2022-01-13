class Element:
    IDn = [0 for _ in range(4)]
    ID = 1
    H = [[0 for _ in range(4)] for _ in range(4)]
    Hbc = [[0 for _ in range(4)] for _ in range(4)]
    aggrH = [[0 for _ in range(4)] for _ in range(4)]
    P = [0 for _ in range(4)]
    C = [0 for _ in range(4)]
    #dla trojpunktowego c bedzie 9 na 4

    def __init__(self, IDn, ID=1):
        self.ID = ID
        self.IDn = IDn

    def setup(self, IDn):
        self.IDn = IDn

    def __str__(self):
        return f'\nrectangle id: {self.ID} nodes id:{self.IDn}'

    def __repr__(self):
        return f'\nrectangle id: {self.ID} nodes id:{self.IDn}'
