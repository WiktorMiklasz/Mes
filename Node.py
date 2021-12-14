class Node:
    x = 0
    y = 0
    flag = 0

    def __init__(self, x, y, ):
        self.x = x
        self.y = y

    def __str__(self):
        return f'\nx: {self.x}, y: {self.y}'

    def __repr__(self):
        return f'\nx: {self.x}, y: {self.y}'
