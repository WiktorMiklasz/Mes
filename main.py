from Element4_2D import Element4_2D
from Grid import Grid
import numpy as np


def calculate(ksi, eta, grid, element, t0):
    # GLOWNA FUNKCJA OBLICZENIOWA
    # dla niegenerowania siatki mozna sama macierz inv wklepac +detJ gotowe
    # matrixInv=[[80,0],[0,80]]
    global matrixInv, detJ, PGlobal, HGlobal, CGlobal, sumHC
    # HC to zagregowane H i C, CP to zagregowane C i P
    H1 = []
    H2 = []
    Hbc = [[0 for _ in range(4)] for _ in range(4)]
    Hlocal = [[0 for _ in range(4)] for _ in range(4)]
    Plocal = [0 for _ in range(4)]
    PGlobal = [0 for _ in range(grid.amount)]
    HGlobal = [[0 for _ in range(grid.amount)] for _ in range(grid.amount)]
    CGlobal = [[0 for _ in range(grid.amount)] for _ in range(grid.amount)]
    sumHC = [[0 for _ in range(grid.amount)] for _ in range(grid.amount)]
    for i in range(grid.nE):
        CLocal = [[0 for _ in range(4)] for _ in range(4)]
        for j in range(4):
            # print("\nNumer elementu:", i, " Punkt calkowania:", j, "\n")
            matrixInv, detJ = jakobian(i, j, ksi, eta, grid)
            # detJ wykorzystywane w macierzy H
            dNdX, dNdY = calculatePC(ksi, eta)
            H1, H2 = calculateMatrixHforPC(dNdX[j], dNdY[j], H1, H2)
            calculateC(j, element, CLocal)
        grid.elements[i].H = calculateH(H1, H2)
        pc1, pc2, p1, p2 = calculateHbcAndP(grid, element, i)
        for j in range(4):
            for k in range(4):
                Hbc[j][k] = alpha * (pc1[j][k] + pc2[j][k])
                Hlocal[j][k] = Hbc[j][k] + grid.elements[i].H[j][k]
            Plocal[j] = p1[j] + p2[j]
        grid.elements[i].Hbc = Hbc
        grid.elements[i].aggrH = Hlocal
        grid.elements[i].P = Plocal
        grid.elements[i].C = CLocal
        print("Number of element ", i + 1)
        print("\nHbc:\n", Hbc)
        print("\naggregatedH:\n", Hlocal)
        print("\nWektor P:\n", Plocal)
        aggregationGlobal(grid, i)
        print("\nMacierz C lokalna:\n", CLocal)
    sumHandC()
    #sumCP = PGlobal.copy()
    sumCandP(t0)
    iteration(grid, t0)


def jakobian(i, j, ksi, eta, grid):
    matrix = [[0 for _ in range(2)] for _ in range(2)]
    matrixInv = [[0 for _ in range(2)] for _ in range(2)]
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


def calculatePC(ksi, eta):
    dNdX = [[0 for _ in range(4)] for _ in range(4)]
    dNdY = [[0 for _ in range(4)] for _ in range(4)]

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
    HX = [[0 for _ in range(4)] for _ in range(4)]
    HY = [[0 for _ in range(4)] for _ in range(4)]

    for i in range(0, 4):
        for j in range(0, 4):
            HX[i][j] = dNdX[j] * dNdX[i]
            HY[i][j] = dNdY[j] * dNdY[i]
    H1 += HX
    H2 += HY

    return H1, H2


# def calculateHBC():


def calculateH(H1, H2):
    H = [[0 for _ in range(4)] for _ in range(16)]
    result = [[0 for _ in range(4)] for _ in range(4)]
    for i in range(0, 16):
        for j in range(0, 4):
            H[i][j] = con * (H1[i][j] + H2[i][j]) * detJ
            # 0.000156 dla zadania z zajec zamiast detJ

    for i in range(0, 4):
        for j in range(0, 4):
            result[i][j] = H[i][j] + H[i + 4][j] + H[i + 8][j] + H[i + 12][j]
    # print(result, "\n")
    return result


def calculateHbcAndP(grid, element, i):
    pc1 = [[0 for _ in range(4)] for _ in range(4)]
    pc2 = [[0 for _ in range(4)] for _ in range(4)]
    p1 = [0 for _ in range(4)]
    p2 = [0 for _ in range(4)]
    node1 = grid.elements[i].IDn[0]
    node2 = grid.elements[i].IDn[1]
    node3 = grid.elements[i].IDn[2]
    node4 = grid.elements[i].IDn[3]
    # przemnazam juz tutaj macierze przez detJ, na wypadek jakby w elemencie byly dwa warunki brzegowe
    if grid.nodes[node1 - 1].flag == 1 and grid.nodes[node2 - 1].flag == 1:
        # dolna sciana
        # print("Number of element:", i)
        # print("\n node 1 and 2\n")
        for j in range(4):
            for k in range(4):
                dJ = grid.xB / 2
                pc1[j][k] += element.bottom[0][k] * element.bottom[0][j] * dJ
                pc2[j][k] += element.bottom[1][k] * element.bottom[1][j] * dJ
            p1[j] += element.bottom[0][j] * t * dJ * alpha
            p2[j] += element.bottom[1][j] * t * dJ * alpha

    if grid.nodes[node1 - 1].flag == 1 and grid.nodes[node4 - 1].flag == 1:
        # lewa sciana
        # print("Number of element:", i)
        # print("\nnode 1 and 4")
        for j in range(4):
            for k in range(4):
                dJ = grid.yH / 2
                pc1[j][k] += element.left[0][k] * element.left[0][j] * dJ
                pc2[j][k] += element.left[1][k] * element.left[1][j] * dJ
            p1[j] += element.left[0][j] * t * dJ * alpha
            p2[j] += element.left[1][j] * t * dJ * alpha
    if grid.nodes[node2 - 1].flag == 1 and grid.nodes[node3 - 1].flag == 1:
        # prawa sciana
        # print("Number of element:", i)
        # print("\nnode 2 and 3")
        for j in range(4):
            for k in range(4):
                dJ = grid.yH / 2
                pc1[j][k] += element.right[0][k] * element.right[0][j] * dJ
                pc2[j][k] += element.right[1][k] * element.right[1][j] * dJ
            p1[j] += element.right[0][j] * t * dJ * alpha
            p2[j] += element.right[1][j] * t * dJ * alpha
    if grid.nodes[node3 - 1].flag == 1 and grid.nodes[node4 - 1].flag == 1:
        # gorna sciana
        # print("Number of element:", i)
        # print("\nnode 3 and 4")
        for j in range(4):
            for k in range(4):
                dJ = grid.xB / 2
                pc1[j][k] += element.top[0][k] * element.top[0][j] * dJ
                pc2[j][k] += element.top[1][k] * element.top[1][j] * dJ
            p1[j] += element.top[0][j] * t * dJ * alpha
            p2[j] += element.top[1][j] * t * dJ * alpha
    return pc1, pc2, p1, p2


def calculateC(j, element, CLocal):
    # J - Punkt calkowania
    # K - przechodzenie po kolumnach
    # l - przechodzenie po wierszach
    for k in range(4):
        for l in range(4):
            CLocal[k][l] += c * ro * detJ * element.N[j][k] * element.N[j][l]
    return CLocal


def aggregationGlobal(grid, i):
    for j in range(4):
        for k in range(4):
            HGlobal[grid.elements[i].IDn[j] - 1][grid.elements[i].IDn[k] - 1] += grid.elements[i].aggrH[j][k]
            CGlobal[grid.elements[i].IDn[j] - 1][grid.elements[i].IDn[k] - 1] += grid.elements[i].C[j][k]
        PGlobal[grid.elements[i].IDn[j] - 1] += grid.elements[i].P[j]


def sumHandC():
    for i in range(len(HGlobal)):
        for j in range(len(HGlobal)):
            sumHC[i][j] = HGlobal[i][j] + CGlobal[i][j] / dt


def sumCandP(t0):
    sumCP = PGlobal.copy()
    for i in range(len(PGlobal)):
        for j in range(len(PGlobal)):
            sumCP[i] += CGlobal[i][j] / dt * t0[j]
    return sumCP


def iteration(grid, t0):
    sumCP = sumCandP(t0)
    t0 = np.linalg.solve(sumHC, sumCP)
    print(f'Minimum: {min(t0)}, Max: {max(t0)},\n')
    iterations = int(time / dt)
    for i in range(iterations - 1):
       # for j in range(grid.nE):
           # aggregationGlobal(grid, j)  # na zajeciach to olewamy, ja tez tak postapie. Jak pan Jezus powiedzial.
        sumHandC()
        print(f't0: {t0} \n')
        sumCP = sumCandP(t0)
        print(f'wartosc wektora cp: {sumCP} ')
        t0 = np.linalg.solve(sumHC, sumCP)
        print(f'Numer iteracji: {i+1}, Minimum: {min(t0)}, Max: {max(t0)},\n')



def main():
    global t, alpha, c, ro, dt, time, con
    # zmienne globalne to gowno a python ssie chujA
    grid = Grid(0.1, 0.1, 4, 4)
    c = 700  # cieplo wlasciwe
    ro = 7800  # gęstosc
    alpha = 300  # wspolczynnik przewodzenia ciepla
    t = 1200  # temperatura otoczenia
    dt = 50  # krok czasowy
    time = 500
    con = 25
    t0 = [100 for _ in range(grid.amount)]  # wektor temperatur poczatkowych
    print(grid.nodes)
    # c.printFlag()
    grid.printElements()
    element = Element4_2D()
    calculate(element.ksi, element.eta, grid, element, t0)
    print(f'H Globalne:\n {HGlobal} \nP Globalne: \n {PGlobal} \n C Globalne: \n {CGlobal}')
    print("\n Suma H i C:\n", sumHC)
    #print("\n Suma C i P:\n", sumCP)


if __name__ == '__main__':
    main()

    # no 3 point integration yet
