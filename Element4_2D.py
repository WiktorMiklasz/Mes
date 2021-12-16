import math


class Element4_2D:
    ksi = []
    eta = []
    left = []
    right = []
    top = []
    bottom = []
    N = []

    def __init__(self):
        self.ksi = [[0 for _ in range(4)] for _ in range(4)]
        self.eta = [[0 for _ in range(4)] for _ in range(4)]
        self.top = [[0 for _ in range(4)] for _ in range(4)]
        self.left = [[0 for _ in range(4)] for _ in range(4)]
        self.right = [[0 for _ in range(4)] for _ in range(4)]
        self.bottom = [[0 for _ in range(4)] for _ in range(4)]
        self.N = [[0 for _ in range(4)] for _ in range(4)]

        self.points = [[-1 / math.sqrt(3), -1 / math.sqrt(3)], [1 / math.sqrt(3), -1 / math.sqrt(3)],
                       [1 / math.sqrt(3), 1 / math.sqrt(3)], [-1 / math.sqrt(3), 1 / math.sqrt(3)]]
        self.points2 = [-1 / math.sqrt(3), 1 / math.sqrt(3)]
        self.calculateDeriatives()
        self.calculateNforC()
        print("north:", self.top)
        print("south:", self.bottom)
        print("west:", self.left)
        print("east:", self.right)

    def calculateNforC(self):
        for i in range(4):
            #wykorzystanie punktow calkowania i liczenie funkcji ksztaltu dla tych punktow, nie pochodnych
            self.N[i][0] = 0.25 * (1 - self.points[i][0]) * (1 - self.points[i][1])
            self.N[i][1] = 0.25 * (1 + self.points[i][0]) * (1 - self.points[i][1])
            self.N[i][2] = 0.25 * (1 + self.points[i][0]) * (1 + self.points[i][1])
            self.N[i][3] = 0.25 * (1 - self.points[i][0]) * (1 + self.points[i][1])

    def calculateDeriatives(self):
        col = len(self.ksi[0])
        for i in range(0, col):
            self.ksi[i][0] = -1 / 4 * (1 - self.points[i][1])
            self.ksi[i][1] = 1 / 4 * (1 - self.points[i][1])
            self.ksi[i][2] = 1 / 4 * (1 + self.points[i][1])
            self.ksi[i][3] = -1 / 4 * (1 + self.points[i][1])

            self.eta[i][0] = -1 / 4 * (1 - self.points[i][0])
            self.eta[i][1] = -1 / 4 * (1 + self.points[i][0])
            self.eta[i][2] = 1 / 4 * (1 + self.points[i][0])
            self.eta[i][3] = 1 / 4 * (1 - self.points[i][0])

        print(self.ksi)
        print(self.eta)
        for i in range(2):  # 2 bo tyle punktow calkowania

            ksiLeft = -1
            ksiRight = 1
            etaTop = 1
            etaBottom = -1

            # obliczanie sumy wartosci funkcji ksztaltu dla scian
            self.top[i][0] = 0.25 * (1.0 - self.points2[i]) * (1.0 - etaTop)
            self.top[i][1] = 0.25 * (1.0 + self.points2[i]) * (1.0 - etaTop)
            self.top[i][2] = 0.25 * (1.0 + self.points2[i]) * (1.0 + etaTop)
            self.top[i][3] = 0.25 * (1.0 - self.points2[i]) * (1.0 + etaTop)

            self.bottom[i][0] = 0.25 * (1.0 - self.points2[i]) * (1.0 - etaBottom)
            self.bottom[i][1] = 0.25 * (1.0 + self.points2[i]) * (1.0 - etaBottom)
            self.bottom[i][2] = 0.25 * (1.0 + self.points2[i]) * (1.0 + etaBottom)
            self.bottom[i][3] = 0.25 * (1.0 - self.points2[i]) * (1.0 + etaBottom)

            self.right[i][0] = 0.25 * (1.0 - self.points2[i]) * (1.0 - ksiRight)
            self.right[i][1] = 0.25 * (1.0 - self.points2[i]) * (1.0 + ksiRight)
            self.right[i][2] = 0.25 * (1.0 + self.points2[i]) * (1.0 + ksiRight)
            self.right[i][3] = 0.25 * (1.0 + self.points2[i]) * (1.0 - ksiRight)

            self.left[i][0] = 0.25 * (1.0 - self.points2[i]) * (1.0 - ksiLeft)
            self.left[i][1] = 0.25 * (1.0 - self.points2[i]) * (1.0 + ksiLeft)
            self.left[i][2] = 0.25 * (1.0 + self.points2[i]) * (1.0 + ksiLeft)
            self.left[i][3] = 0.25 * (1.0 + self.points2[i]) * (1.0 - ksiLeft)
