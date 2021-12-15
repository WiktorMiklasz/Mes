class Element:
    IDn = [0 for _ in range(4)]
    ID = 1
    H = [[0 for _ in range(4)] for _ in range(4)]
    Hbc = [[0 for _ in range(4)] for _ in range(4)]
    aggrH = [[0 for _ in range(4)] for _ in range(4)]
    P = [0 for _ in range(4)]

    def __init__(self, IDn, ID=1):
        self.ID = ID
        self.IDn = IDn

    def setup(self, IDn):
        self.IDn = IDn

    def __str__(self):
        return f'rectangle id: {self.ID}\nnodes id:{self.IDn}'

    def __repr__(self):
        return f'rectangle id: {self.ID}\nnodes id:{self.IDn}'
