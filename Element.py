class Element:
    IDn = [0, 0, 0, 0]
    ID = 1
    H = [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]]
    Hbc = [[0, 0, 0, 0],
           [0, 0, 0, 0],
           [0, 0, 0, 0],
           [0, 0, 0, 0]]

    def __init__(self, IDn, ID=1):
        self.ID = ID
        self.IDn = IDn

    def setup(self, IDn):
        self.IDn = IDn

    def __str__(self):
        return f'rectangle id: {self.ID}\nnodes id:{self.IDn}'

    def __repr__(self):
        return f'rectangle id: {self.ID}\nnodes id:{self.IDn}'