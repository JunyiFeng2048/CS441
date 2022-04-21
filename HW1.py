"""
Winter 2022
CS 441
Junyi Feng
Program 1
"""

import numpy as np
import math
import operator

"""
initState = [[1, 2, 3], [0, 4, 6], [8, 5, 7]]
goalState = [[0, 1, 3], [4, 2, 5], [7, 8, 6]]   #no solution
"""

initState = [[3, 7, 2], [6, 8, 0], [4, 5, 1]]
goalState = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

"""
initState = [[2, 8, 3], [1, 0, 4], [7, 6, 5]]
goalState = [[1, 2, 3], [8, 0, 4], [7, 6, 5]]
"""
"""
initState = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]   
goalState = [[1, 0, 2], [3, 4, 5], [6, 7, 8]]
"""

"""
initState = [[2, 8, 3], [6, 0, 4], [1, 7, 5]]   
goalState = [[1, 2, 3], [8, 0, 4], [7, 6, 5]]
"""
"""
initState = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]   
goalState = [[3, 1, 2], [4, 0, 6], [7, 5, 8]]
"""

dic = np.zeros((9, 2))
k = 0
for i in range(3):  # goal index dictionary auto generater
    for j in range(3):
        dic[k][0] = i
        dic[k][1] = j
        k += 1

step = 0


def checkInversions(no0):
    count = 0
    for i in range(len(no0)):
        for j in range(i + 1, len(no0)):
            if no0[i] > no0[j]:
                # print(no0[i], " - ", no0[j])
                count += 1
    return count


def checkSolution():
    initNo0 = ""
    goalNo0 = ""
    # print(type(initState))
    for i in range(len(initState)):
        for j in range(len(initState[i])):
            if initState[i][j] != 0:
                initNo0 += str(initState[i][j])

    for i in range(len(goalState)):
        for j in range(len(goalState[i])):
            if goalState[i][j] != 0:
                goalNo0 += str(goalState[i][j])

    inv1 = checkInversions(initNo0)
    print("")
    inv2 = checkInversions(goalNo0)
    invResult = inv1 - inv2
    # print(invResult)
    if invResult % 2 != 0:
        return 0
    return 1


def copyState(state):  # copy state without change
    new = []
    for i in state: new.append(i[:])
    return new


def h1(state):  # number of misplaced tiles
    hn = 0
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] != goalState[i][j]:
                hn += 1
    return hn


def h2(state):  # Manhattan distance
    hn = 0
    for i in range(len(state)):
        for j in range(len(state[i])):
            loc = dic[state[i][j]]
            y, x = loc[0], loc[1]
            hn += abs(y - i) + abs(x - j)
    return hn


def h3(state):  # Euclidean distance
    hn = 0
    for i in range(len(state)):
        for j in range(len(state[i])):
            loc = dic[state[i][j]]
            y, x = loc[0], loc[1]
            hn += math.sqrt(abs(y - i) ** 2 + abs(x - j) ** 2)
    return hn


def getAvailActs(state):
    acts = []
    for a in range(len(state)):  # find the index for 0
        for b in range(len(state[a])):
            if state[a][b] == 0:
                break
        if state[a][b] == 0:
            break

    for i in range(len(state)):  #swap
        for j in range(len(state[i])):
            if ((i - a) ** 2 + (j - b) ** 2) == 1:
                cp = copyState(state)
                cp[a][b] = cp[i][j]
                cp[i][j] = 0
                acts.append(cp)
    # print(acts[0])
    # print(acts)
    return acts


class aStarNode:
    def __init__(self, state, gn, parent):
        self.state = state
        self.gn = gn
        self.parent = parent
        self.fn = h1(state) + gn
        # self.fn = h2(state) + gn
        #self.fn = h3(state) + gn


class gbfsNode:
    def __init__(self, state, parent):
        self.state = state
        self.parent = parent
        self.fn = h1(state)
        # self.fn = h2(state)
        #self.fn = h3(state)


def printPath(root):
    if root is None:
        return
    global step
    step += 1
    printPath(root.parent)
    # print(root.state)
    for i in root.state:
        print(i)
    print("")


def aStar():
    list1 = [aStarNode(initState, 0, None)]
    visit = []
    count = 0
    while list1:
        list1.sort(key=operator.attrgetter('fn'))
        last = list1[0]
        visit.append(last.state)
        # print(last.state)
        count += 1
        if count == 20000:
            return last, count
        if last.state == goalState:
            return last, count
        del list1[0]
        acts = getAvailActs(last.state)
        for i in acts:
            availAct = aStarNode(i, last.gn + 1, last)
            if availAct.state not in visit:
                # print(availAct.state)
                list1.append(availAct)
                visit.append(availAct.state)

    return None, count


def gbfs():
    list2 = [gbfsNode(initState, None)]
    visit = []
    count = 0
    while list2:
        list2.sort(key=operator.attrgetter('fn'))
        last = list2[0]
        visit.append(last.state)
        count += 1
        if last.state == goalState:
            return last, count
        if count == 20000:
            return last, count
        del list2[0]
        acts = getAvailActs(last.state)
        for i in acts:
            availAct = gbfsNode(i, last)
            if availAct.state not in visit:
                list2.append(availAct)
                visit.append(availAct.state)

    return None, count


if __name__ == '__main__':

    if checkSolution() == 0:
        print("No solution")
    else:
        root1, count1 = aStar()

        print("A*: ")
        printPath(root1)
        if count1 == 10000:
            print("exceeds limit, solution not found")
        print("Steps: ", step)
        print("")
        root2, count2 = gbfs()
        step = 0
        print("gbfs: ")
        printPath(root2)
        if count2 == 10000:
            print("exceeds limit, solution not found")
        print("Steps: ", step)
