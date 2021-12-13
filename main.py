from Element4_2D import Element4_2D
from Grid import Grid


def calculate(ksi, eta, grid, element):
    # GLOWNA FUNKCJA OBLICZENIOWA
    # dla niegenerowania siatki mozna sama macierz inv wklepac +detJ gotowe
    # matrixInv=[[80,0],[0,80]]
    global matrixInv, matrix, detJ
    H1 = []
    H2 = []
    a = [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]]
    for i in range(0, grid.nE):
        for j in range(0, 4):
            # print("\nNumer elementu:", i, " Punkt calkowania:", j, "\n")
            matrixInv, detJ = jakobian(i, j, ksi, eta, grid)
            # detJ wykorzystywane w macierzy H
            dNdX, dNdY = calculatePC(ksi, eta, matrixInv)
            H1, H2 = calculateMatrixHforPC(dNdX[j], dNdY[j], H1, H2)
        grid.elements[i].H = calculateH(H1, H2, detJ)
        pc1, pc2 = calculateHbc(grid, element, i)
        for j in range(4):
            for k in range(4):
                a[j][k] = 300 * (pc1[j][k] + pc2[j][k])
        print(a)


def jakobian(i, j, ksi, eta, grid):
    matrix = [[0, 0],
              [0, 0]]
    matrixInv = [[0, 0],
                 [0, 0]]
    node1 = grid.elements[i].IDn[0]
    node2 = grid.elements[i].IDn[1]
    node3 = grid.elements[i].IDn[2]
    node4 = grid.elements[i].IDn[3]
    # print("ID wierzcholkow:")
    # print("/////////////////\n", node1, node2, node3, node4, "\n/////////////////\n")

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

    detJ = matrix[0][0] * matrix[1][1] - (matrix[0][1] * matrix[1][0])
    matrixInv[0][0] *= 1 / detJ
    matrixInv[0][1] *= 1 / detJ
    matrixInv[1][0] *= 1 / detJ
    matrixInv[1][1] *= 1 / detJ
    return matrixInv, detJ


def calculatePC(ksi, eta, matrixInv):
    dNdX = [[0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]]
    dNdY = [[0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]]
    for i in range(0, 4):
        dNdX[i][0] = matrixInv[0][0] * ksi[i][0] + matrixInv[0][1] * eta[i][0]
        dNdX[i][1] = matrixInv[0][0] * ksi[i][1] + matrixInv[0][1] * eta[i][1]
        dNdX[i][2] = matrixInv[0][0] * ksi[i][2] + matrixInv[0][1] * eta[i][2]
        dNdX[i][3] = matrixInv[0][0] * ksi[i][3] + matrixInv[0][1] * eta[i][3]

        dNdY[i][0] = matrixInv[1][0] * ksi[i][0] + matrixInv[1][1] * eta[i][0]
        dNdY[i][1] = matrixInv[1][0] * ksi[i][1] + matrixInv[1][1] * eta[i][1]
        dNdY[i][2] = matrixInv[1][0] * ksi[i][2] + matrixInv[1][1] * eta[i][2]
        dNdY[i][3] = matrixInv[1][0] * ksi[i][3] + matrixInv[1][1] * eta[i][3]
    return dNdX, dNdY


def calculateMatrixHforPC(dNdX, dNdY, H1, H2):
    HX = [[0, 0, 0, 0],
          [0, 0, 0, 0],
          [0, 0, 0, 0],
          [0, 0, 0, 0]]
    HY = [[0, 0, 0, 0],
          [0, 0, 0, 0],
          [0, 0, 0, 0],
          [0, 0, 0, 0]]

    for i in range(0, 4):
        for j in range(0, 4):
            HX[i][j] = dNdX[j] * dNdX[i]
            HY[i][j] = dNdY[j] * dNdY[i]
    H1 += HX
    H2 += HY

    return H1, H2


# def calculateHBC():


def calculateH(H1, H2, detJ):
    H = [[0 for _ in range(4)] for _ in range(16)]
    result = [[0 for _ in range(4)] for _ in range(4)]
    for i in range(0, 16):
        for j in range(0, 4):
            H[i][j] = 30 * (H1[i][j] + H2[i][j]) * detJ
            # 0.000156 dla zadania z zajec zamiast detJ

    for i in range(0, 4):
        for j in range(0, 4):
            result[i][j] = H[i][j] + H[i + 4][j] + H[i + 8][j] + H[i + 12][j]
    # print(result, "\n")
    return result


def calculateHbc(grid, element, i):
    pc1 = [[0, 0, 0, 0],
           [0, 0, 0, 0],
           [0, 0, 0, 0],
           [0, 0, 0, 0]]
    pc2 = [[0, 0, 0, 0],
           [0, 0, 0, 0],
           [0, 0, 0, 0],
           [0, 0, 0, 0]]
    node1 = grid.elements[i].IDn[0]
    node2 = grid.elements[i].IDn[1]
    node3 = grid.elements[i].IDn[2]
    node4 = grid.elements[i].IDn[3]
    # przemnazam juz tutaj macierze przez detJ, na wypadek jakby w elemencie byly dwa warunki brzegowe
    if grid.nodes[node1 - 1].flag == 1 and grid.nodes[node2 - 1].flag == 1:
        # dolna sciana
        # print("Number of element:", i)
        # print("\nnode 1 and 2\n")
        for j in range(4):
            for k in range(4):
                dJ = grid.xB / 2
                pc1[j][k] += element.south[0][k] * element.south[0][j] * dJ
                pc2[j][k] += element.south[1][k] * element.south[1][j] * dJ
    if grid.nodes[node1 - 1].flag == 1 and grid.nodes[node4 - 1].flag == 1:
        # lewa sciana
        # print("Number of element:", i)
        # print("\nnode 1 and 4")
        for j in range(4):
            for k in range(4):
                dJ = grid.yH / 2
                pc1[j][k] += element.west[0][k] * element.west[0][j] * dJ
                pc2[j][k] += element.west[1][k] * element.west[1][j] * dJ
    if grid.nodes[node2 - 1].flag == 1 and grid.nodes[node3 - 1].flag == 1:
        # prawa sciana
        # print("Number of element:", i)
        # print("\nnode 2 and 3")
        for j in range(4):
            for k in range(4):
                dJ = grid.yH / 2
                pc1[j][k] += element.east[0][k] * element.east[0][j] * dJ
                pc2[j][k] += element.east[1][k] * element.east[1][j] * dJ
    if grid.nodes[node3 - 1].flag == 1 and grid.nodes[node4 - 1].flag == 1:
        # gorna sciana
        # print("Number of element:", i)
        # print("\nnode 3 and 4")
        for j in range(4):
            for k in range(4):
                dJ = grid.xB / 2
                pc1[j][k] += element.north[0][k] * element.north[0][j] * dJ
                pc2[j][k] += element.north[1][k] * element.north[1][j] * dJ
    return pc1, pc2




def main():
    c = Grid(0.1, 0.1, 4, 4)
    print(c.nodes)
    c.printFlag()
    c.printElements()
    element = Element4_2D()
    calculate(element.ksi, element.eta, c, element)


if __name__ == '__main__':
    main()
    # left to do: walls, vector p, aggregation
    # no 3 point integration yet
