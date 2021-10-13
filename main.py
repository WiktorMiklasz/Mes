class Node:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'\nx value is {self.x},y value is {self.y}'

    def __repr__(self):
        return f'\nx value is {self.x}, y value is {self.y}'


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
    H = 0.2
    B = 0.1
    nH = 5
    nB = 4
    nodes = []
    nodesCoordinated = []
    elements = []

    def __init__(self, H, B, nH, nB):
        self.H = H
        self.B = B
        self.nH = nH
        self.nB = nB
        self.amount = self.nH * self.nB
        self.nE = (self.nH - 1) * (self.nB - 1)
        self.xH = self.H / (self.nH - 1)
        self.yB = self.B / (self.nB - 1)
        self.createNodes()
        self.createCoordinatedNodes()
        #not needed, resetting it twice in methods anyway
        #self.x = 0
        #self.y = 0
        self.createElements()

    def printGridData(self):
        #debug only
        print(self.H, self.B, self.nH, self.nB, self.nE, self.xH, self.yB)

    def createNodes(self):
        self.x=0
        self.y=0
        for i in range(self.nH - 1):
            self.nodes.append(Node(self.x * self.xH, self.y * self.yB))
            for j in range(self.nB):
                self.y += 1
                self.nodes.append(Node(self.x * self.xH, self.y * self.yB))
            self.x += 1
            self.y = 0

    def createCoordinatedNodes(self):
        self.x = 0
        self.y = 0
        #creating second list of objects but with x y coordinates
        for i in range(self.nH - 1):
            self.nodesCoordinated.append(Node(self.x, self.y))
            for j in range(self.nB):
                self.y += 1
                self.nodesCoordinated.append(Node(self.x, self.y))
            self.x += 1
            self.y = 0

    def createElements(self):
        ID=1
        a=0
        for i in range(self.nE):

            ID1 = ID + a
            ID2 = ID1 + self.nH
            ID3 = ID2 + 1
            ID4 = ID1 + 1
            if (ID1 % self.nH == 0):
                ID1+=1
                ID2+=1
                ID3+=1
                ID4+=1
                a+=1 #to jest inkrement w zależności od tego w której kolumnie tworzone są elementy
            IDn = [ID1, ID2, ID3, ID4]
            self.elements.append(Element(IDn, ID))
            ID += 1
    def printElements(self):
        for i in self.elements:
            print(i)


def main():
    c = Grid(0.2, 0.1, 5, 4)
    # c.printGridData()
    print(c.nodes)
    print(c.nodesCoordinated)
    c.printElements()


# ZROBIONE WYSWIETLANIE NODOW, ZOSTAJA ELEMENTY I PRZEKONWERTOWANIE NODOW NA FAKTYCZNY DYSTANS
# do dupy zrobione, nie chciałem w dwóch osobnych metodach to robić ale już chuj
# trzy razy x i y resetuję, też robota godna indyjskiego helpdesku ale w sumie to działa
if __name__ == '__main__':
    main()
