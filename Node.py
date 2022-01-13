class Node:
    x = 0
    y = 0
    flag = 0
    ID = 0

    def __init__(self, x, y, ID=0):
        self.x = x
        self.y = y
        self.ID = ID

    def __str__(self):
        return f'\nx: {self.x}, y: {self.y}'

    def __repr__(self):
        return f'\nx: {self.x}, y: {self.y}'
