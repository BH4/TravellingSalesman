from random import shuffle, random
from matplotlib import pyplot as plt

# parameters
# city positions
# mutations probability
# population size
# maximum number of generations

global maxNumberOfGenerations
maxNumberOfGenerations = 1000
populationSize = 1000
printAll = False


def distance(p1, p2):
    return (p1[0]-p2[0])**2+(p1[1]-p2[1])**2


def fitness(test, ans):
    f = 0

    for i in range(len(test)):
        f += distance(ans[test[i-1]], ans[test[i]])

    return f


def randIndividual(length):  # individual consists of the order they visit each city
    ind = list(range(length))
    shuffle(ind)

    return ind


def mutate(ind):
    mutProb = .2*(maxNumberOfGenerations-currGen)/maxNumberOfGenerations

    L = len(ind)
    for i in range(L):  # every city has a mutProb chance to be swaped with another
        if random() < mutProb:
            swapOrMoveOrFlip = random()
            if swapOrMoveOrFlip < .4:  # swap two points
                r = int(random()*L)
                temp = ind[r]
                ind[r] = ind[i]
                ind[i] = temp
            elif swapOrMoveOrFlip < .7:  # move one point to another place
                r = int(random()*L)
                temp = ind[i]
                ind.remove(ind[i])
                ind.insert(r, temp)
            else:  # flip back half
                r = int(random()*L)
                Front = ind[:r]
                Back = ind[r:]
                Back.reverse()
                Front.extend(Back)
                ind = Front

    return ind


def transpositions(ind):
    l = len(ind)

    ts = []
    for i in range(l):
        nex = ind[(ind.index(i)+1) % l]
        ts.append(nex)

    return ts


def fillIn(ind, L):

    missing = []
    for i in range(L):
        if not(i in ind):
            missing.append(i)

    shuffle(missing)

    ind.extend(missing)
    return ind


def breed(ind1, ind2):
    L = len(ind1)
    new = []

    trans1 = transpositions(ind1)
    trans2 = transpositions(ind2)

    nex = 0
    while not (nex in new):
        new.append(nex)

        r = random()

        if trans1[nex] in new and trans2[nex] in new:
            new = fillIn(new, L)  # randomly fill in the last remaining cities
        elif trans1[nex] in new:
            nex = trans2[nex]
        elif trans2[nex] in new:
            nex = trans1[nex]
        else:
            if r > .5:
                nex = trans1[nex]
            else:
                nex = trans2[nex]

    return mutate(new)


def selection(pop, ans):
    s = len(pop)

    # list of all population paired with fitness
    fPop = []

    for i in pop:
        fPop.append((fitness(i, ans), i))

    fPop.sort(key=lambda x: x[0])

    best = fPop[0]

    oldPop = [x[1] for x in fPop]
    keep = int(s/2)

    newPop = []
    for i in range(keep):
        newPop.append(oldPop[i])

    totalBabys = 0
    i = 0
    j = 1
    while totalBabys < (s-keep):
        newPop.append(breed(newPop[i], newPop[j]))
        totalBabys += 1

        j += 1
        if j == keep:
            i += 1
            j = i+1
            if j == keep:
                i = 0
                j = 1

    return (newPop, best)


def graph(ind, points):
    x = []
    y = []

    for i in ind:
        x.append(points[i][0])
        y.append(points[i][1])

    x.append(points[ind[0]][0])
    y.append(points[ind[0]][1])

    draw = plt.plot(x, y)
    return draw


def update(draw, ind, points):
    x = []
    y = []

    for i in ind:
        x.append(points[i][0])
        y.append(points[i][1])

    x.append(points[ind[0]][0])
    y.append(points[ind[0]][1])

    draw.set_xdata(x)
    draw.set_ydata(y)
    plt.draw()


def genRandPoints(num):
    p = []

    for i in range(num):
        x = int(random()*200-100)
        y = int(random()*200-100)
        p.append((x, y))

    return p


points = genRandPoints(20)

L = len(points)

pop = []
for i in range(populationSize):
    pop.append(randIndividual(L))


winner = []
wfit = -1
global currGen
currGen = 1

if printAll:
    plt.ion()
    drawing = graph(randIndividual(L), points)
    plt.show()
    while currGen < maxNumberOfGenerations:
        (pop, best) = selection(pop, points)
        bestFit = best[0]

        if bestFit < wfit or wfit == -1:
            # plt.clear()
            wfit = bestFit
            winner = best[1]
            update(drawing, winner, points)
            print("Gen: " + str(currGen) + " | Fitness: " + str(bestFit))

        currGen += 1

else:

    while currGen < maxNumberOfGenerations:
        (pop, best) = selection(pop, points)
        bestFit = best[0]

        if bestFit < wfit or wfit == -1:
            wfit = bestFit
            winner = best[1]
            print("Gen: " + str(currGen) + " | Fitness: " + str(bestFit))

        currGen += 1

    graph(winner, points)
    plt.show()


print("done")
