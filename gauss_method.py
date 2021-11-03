import math

# from math import sqrt
from typing import List


def gauss(nodes_number, dimensions):
    nodes = nodes_amount(nodes_number)
    result = 0.0
    if dimensions == 1:

        for i in range(len(nodes)):
            # wpisywanie wartosci z funkcji recznie, 5x^2*3x+6
            result += nodes[i][1] * (5 * math.pow(nodes[i][0], 2) + 3 * (nodes[i][0]) + 6)
        print(result)
    if dimensions == 2:
        # 5x^2y^2+3xy+6
        for i in range(len(nodes)):
            for j in range(len(nodes)):
                result+= nodes[i][1]*nodes[j][1]*((5*math.pow(nodes[i][0]*nodes[j][0],2)) + 3 * (nodes[i][0]*nodes[j][0]) + 6)
        print(result)



def nodes_amount(nodes_number):
    nodes = []
    if nodes_number == 2:
        nodes = [[-1 / math.sqrt(3), 1], [1 / math.sqrt(3), 1]]
    elif nodes_number == 3:
        nodes = [[-math.sqrt(3 / 5), 5 / 9], [0, 8 / 9], [math.sqrt(3 / 5), 5 / 9]]
    elif nodes_number == 4:
        nodes = [[-0.861136, 0.347855], [-0.339981, 0.652145], [0.339981, 0.652145], [0.861136, 0.347855]]
    return nodes


def main():
    a = int(input("How many points does the scheme have?\n"))
    b = int(input("Choose the number of dimensions, up to 2\n"))
    gauss(a, b)
if __name__ == '__main__':
    main()
