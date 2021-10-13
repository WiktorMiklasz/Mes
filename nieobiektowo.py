

def Grid(nH,nB,amount):
    nodes=[]
    x = 0
    y = 0
    #cords=[x,y]
    for i in range(nH-1):
        cords = [x, y]
        nodes.append(cords)
        for j in range(nB):
            y+=1
            cords = [x,y]
            #print(cords)
            nodes.append(cords)
        x += 1
        y = 0
    print(nodes)
    return nodes


def Elements(nE,nH):
    elements=[]
    n=1
    for i in range(nE):

        ID1=n
        if (ID1%nH==0):
            n+=1
            ID1=n
        ID2=ID1+nH
        ID3=ID2+1
        ID4=ID1+1
        element=[ID1,ID2,ID3,ID4]
        elements.append(element)
        n+=1
    return elements

def Grid_data():
    H=0.2
    B=0.1
    nH=5
    nB=4
    amount=nH*nB
    nE=(nH-1)*(nB-1)
    return nH,nB,amount, nE
def main():
    nH,nB,amount,nE = Grid_data()
    print(Grid(nH,nB,amount))
    print(Elements(nE,nH))


if __name__ == '__main__':
    main()

