from Element import Element
from Node import Node


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
        self.checkFlag()
        # self.createCoordinatedNodes()
        self.createElements()

    def createNodes(self):
        for i in range(self.nB):
            # self.nodes.append(Node(i * self.xB, j * self.yH))
            for j in range(self.nH):
                self.nodes.append(Node(i * self.xB, j * self.yH))

    def createCoordinatedNodes(self):
        for i in range(self.nB):
            for j in range(self.nH):
                self.nodes.append(Node(i, j))

    def createElements(self):
        ID = 1
        a = 0
        for i in range(self.nE):
            ID1 = ID + a
            ID2 = ID1 + self.nH
            ID3 = ID2 + 1
            ID4 = ID1 + 1
            if ID1 % self.nH == 0:
                ID1 += 1
                ID2 += 1
                ID3 += 1
                ID4 += 1
                a += 1  # to jest inkrement w zaleznosci od tego w której kolumnie tworzone sa elementy
            IDn = [ID1, ID2, ID3, ID4]
            self.elements.append(Element(IDn, ID))
            ID += 1

    def checkFlag(self):
        for i in range(len(self.nodes)):
            if self.nodes[i].x == 0 or self.nodes[i].y == 0 or self.nodes[i].y == self.H or self.nodes[i].x == self.H:
                self.nodes[i].flag = 1

    def printElements(self):
        for element in self.elements:
            print(element)

    def printFlag(self):
        for i in range(len(self.nodes)):
            print("number of node:", i, self.nodes[i].flag)

