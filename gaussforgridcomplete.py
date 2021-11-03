import math


class Node:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'\nx: {self.x}, y: {self.y}'

    def __repr__(self):
        return f'\nx: {self.x}, y: {self.y}'


class Element:
    IDn = [0, 0, 0, 0]
    ID = 1

    def __init__(self, IDn, ID=1):
        self.ID = ID
        self.IDn = IDn

    def setup(self, IDn):
        self.IDn = IDn

    def __str__(self):
        return f'rectangle id: {self.ID}\nnodes id:{self.IDn}'

    def __repr__(self):
        return f'rectangle id: {self.ID}\nnodes id:{self.IDn}'


class Grid:
    nodes = []
    nodesCoordinated = []
    elements = []

    def __init__(self, H, B, yH, xB):
        self.H = H
        self.B = B
        self.nH = yH
        self.nB = xB
        self.amount = self.nH * self.nB
        self.nE = (self.nH - 1) * (self.nB - 1)
        self.yH = self.H / (self.nH - 1)
        self.xB = self.B / (self.nB - 1)
        self.createNodes()
        # self.createCoordinatedNodes()
        self.createElements()

    def printGridData(self):
        # debug only
        print(self.H, self.B, self.nH, self.nB, self.nE, self.yH, self.xB)

    def createNodes(self):
        x = 0
        y = 0
        for i in range(self.nH - 1):
            self.nodes.append(Node(x * self.xB, y * self.yH))
            for j in range(self.nB):
                y += 1
                self.nodes.append(Node(x * self.xB, y * self.yH))
            x += 1
            y = 0

    def createCoordinatedNodes(self):
        x = 0
        y = 0
        # creating second list of objects but with x y coordinates
        for i in range(self.nH - 1):
            self.nodesCoordinated.append(Node(x, y))
            for j in range(self.nB):
                y += 1
                self.nodesCoordinated.append(Node(x, y))
            x += 1
            y = 0

    def createElements(self):
        ID = 1
        a = 0
        for i in range(self.nE):
            ID1 = ID + a
            ID2 = ID1 + self.nH
            ID3 = ID2 + 1
            ID4 = ID1 + 1
            if (ID1 % self.nH == 0):
                ID1 += 1
                ID2 += 1
                ID3 += 1
                ID4 += 1
                a += 1  # to jest inkrement w zależności od tego w której kolumnie tworzone są elementy
            IDn = [ID1, ID2, ID3, ID4]
            self.elements.append(Element(IDn, ID))
            ID += 1

    def printElements(self):
        for i in self.elements:
            print(i)


def wynikPochodnej():
    points = [[-1 / math.sqrt(3), -1 / math.sqrt(3)], [1 / math.sqrt(3), -1 / math.sqrt(3)],
              [1 / math.sqrt(3), 1 / math.sqrt(3)], [-1 / math.sqrt(3), 1 / math.sqrt(3)]]
    ksi = [[0, 0, 0, 0],
           [0, 0, 0, 0],
           [0, 0, 0, 0],
           [0, 0, 0, 0]]
    eta = [[0, 0, 0, 0],
           [0, 0, 0, 0],
           [0, 0, 0, 0],
           [0, 0, 0, 0]]
    col = len(ksi[0])
    for i in range(0, col):
        ksi[i][0] = -1 / 4 * (1 - points[i][1])
        ksi[i][1] = 1 / 4 * (1 - points[i][1])
        ksi[i][2] = 1 / 4 * (1 + points[i][1])
        ksi[i][3] = -1 / 4 * (1 + points[i][1])

        eta[i][0] = -1 / 4 * (1 - points[i][0])
        eta[i][1] = -1 / 4 * (1 + points[i][0])
        eta[i][2] = 1 / 4 * (1 + points[i][0])
        eta[i][3] = 1 / 4 * (1 - points[i][0])
    print(ksi)
    print(eta)
    return ksi, eta


def calculateMatrix(ksi, eta, grid):
    for i in range(0, grid.nE):
        for j in range(0, 4):
            print("\nNumer elementu:", i, " Punkt calkowania:", j, "\n")
            matrix, matrixInv = jakobian(i, j, ksi, eta, grid)
            print("----------------------------------------------------------------\n", matrix, "\n",
                  "----------------------------------------------------------------\n", matrixInv,
                  "\n----------------------------------------------------------------")


def jakobian(i, j, ksi, eta, grid):
    matrix = [[0, 0],
              [0, 0]]
    matrixInv = [[0, 0],
                 [0, 0]]
    node1 = grid.elements[i].IDn[0]
    node2 = grid.elements[i].IDn[1]
    node3 = grid.elements[i].IDn[2]
    node4 = grid.elements[i].IDn[3]
    print("ID wierzcholkow:")
    print("/////////////////\n", node1, node2, node3, node4, "\n/////////////////\n")

    # 0 0 to pochodna x po ksi
    matrix[0][0] = ksi[j][0] * grid.nodes[node1 - 1].x + ksi[j][1] * grid.nodes[node2 - 1].x + ksi[j][2] * grid.nodes[
        node3 - 1].x + ksi[j][3] * grid.nodes[node4 - 1].x

    # 0 1 to pochodna y po ksi
    matrix[0][1] = ksi[j][0] * grid.nodes[node1 - 1].y + ksi[j][1] * grid.nodes[node2 - 1].y + ksi[j][2] * grid.nodes[
        node3 - 1].y + ksi[j][3] * grid.nodes[node4 - 1].y

    # 1 0 to pochodna x po eta
    matrix[1][0] = eta[j][0] * grid.nodes[node1 - 1].x + eta[j][1] * grid.nodes[node2 - 1].x + eta[j][2] * grid.nodes[
        node3 - 1].x + eta[j][3] * grid.nodes[node4 - 1].x

    # 1 1 to pochodna y po eta
    matrix[1][1] = eta[j][0] * grid.nodes[node1 - 1].y + eta[j][1] * grid.nodes[node2 - 1].y + eta[j][2] * grid.nodes[
        node3 - 1].y + eta[j][3] * grid.nodes[node4 - 1].y
    matrixInv[0][0] = matrix[1][1]
    matrixInv[0][1] = (-1) * matrix[0][1]
    matrixInv[1][0] = (-1) * matrix[1][0]
    matrixInv[1][1] = matrix[0][0]

    detJ = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    matrixInv[0][0] *= 1 / detJ
    matrixInv[0][1] *= 1 / detJ
    matrixInv[1][0] *= 1 / detJ
    matrixInv[1][1] *= 1 / detJ
    return matrix, matrixInv


def main():
    c = Grid(0.5, 0.1, 5, 4)
    # c.printGridData()
    print(c.nodes)
    # print(c.nodesCoordinated)
    c.printElements()
    ksi, eta = wynikPochodnej()
    calculateMatrix(ksi, eta, c)


if __name__ == '__main__':
    main()
