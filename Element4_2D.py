import math


class Element4_2D:
    ksi = []
    eta = []
    west = []
    east = []
    north = []
    south = []

    def __init__(self):
        self.ksi = [[0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]]
        self.eta = [[0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]]
        self.north = [[0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]]
        self.west = [[0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0]]
        self.east = [[0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0]]
        self.south = [[0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]]
        self.points = [[-1 / math.sqrt(3), -1 / math.sqrt(3)], [1 / math.sqrt(3), -1 / math.sqrt(3)],
                       [1 / math.sqrt(3), 1 / math.sqrt(3)], [-1 / math.sqrt(3), 1 / math.sqrt(3)]]
        self.points2 = [-1 / math.sqrt(3), 1 / math.sqrt(3)]
        self.calculateDeriatives()
        print("north:", self.north)
        print("south:", self.south)
        print("west:", self.west)
        print("east:", self.east)

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

            ksiWest = -1
            ksiEast = 1
            etaNorth = 1
            etaSouth = -1

            # obliczanie sumy wartosci funkcji ksztaltu dla scian
            self.north[i][0] = 0.25 * (1.0 - self.points2[i]) * (1.0 - etaNorth)
            self.north[i][1] = 0.25 * (1.0 + self.points2[i]) * (1.0 - etaNorth)
            self.north[i][2] = 0.25 * (1.0 + self.points2[i]) * (1.0 + etaNorth)
            self.north[i][3] = 0.25 * (1.0 - self.points2[i]) * (1.0 + etaNorth)

            self.south[i][0] = 0.25 * (1.0 - self.points2[i]) * (1.0 - etaSouth)
            self.south[i][1] = 0.25 * (1.0 + self.points2[i]) * (1.0 - etaSouth)
            self.south[i][2] = 0.25 * (1.0 + self.points2[i]) * (1.0 + etaSouth)
            self.south[i][3] = 0.25 * (1.0 - self.points2[i]) * (1.0 + etaSouth)

            self.east[i][0] = 0.25 * (1.0 - self.points2[i]) * (1.0 - ksiEast)
            self.east[i][1] = 0.25 * (1.0 - self.points2[i]) * (1.0 + ksiEast)
            self.east[i][2] = 0.25 * (1.0 + self.points2[i]) * (1.0 + ksiEast)
            self.east[i][3] = 0.25 * (1.0 + self.points2[i]) * (1.0 - ksiEast)

            self.west[i][0] = 0.25 * (1.0 - self.points2[i]) * (1.0 - ksiWest)
            self.west[i][1] = 0.25 * (1.0 - self.points2[i]) * (1.0 + ksiWest)
            self.west[i][2] = 0.25 * (1.0 + self.points2[i]) * (1.0 + ksiWest)
            self.west[i][3] = 0.25 * (1.0 + self.points2[i]) * (1.0 - ksiWest)