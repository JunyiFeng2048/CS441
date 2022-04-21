import numpy as np
import random
import matplotlib.pyplot as plt

class robot:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.reward = 0
        self.collection = 0

    # Sensor Functions
    def getCurrent(self, grid):
        return grid[self.x][self.y]

    def getNorth(self, grid):
        return grid[self.x - 1][self.y]

    def getSorth(self, grid):
        return grid[self.x + 1][self.y]

    def getEast(self, grid):
        return grid[self.x][self.y + 1]

    def getWest(self, grid):
        return grid[self.x][self.y - 1]

    # Action Functions
    def pickUp(self, grid):  # pick up a can
        if grid[self.x][self.y] == 1:
            grid[self.x][self.y] = 0
            return True  # if action was successful
        else:
            return False

    def moveNorth(self, grid):  # move north on the grid
        if self.getNorth(grid) == -1:
            return False
        self.x -= 1
        return True  # if action was successful

    def moveSouth(self, grid):  # move south on the grid
        if (self.getSorth(grid) == -1):
            return False
        self.x += 1
        return True  # if action was successful

    def moveEast(self, grid):  # move east on the grid
        if (self.getEast(grid) == -1):
            return False
        self.y += 1
        return True  # if action was successful

    def moveWest(self, grid):  # move est on the grid
        if (self.getWest(grid) == -1):
            return False
        self.y -= 1
        return True  # if action was successful

    # Other Functions
    def convertState(self, grid):  # represents state as a tuple
        stateVector = (self.getCurrent(grid), self.getNorth(grid), self.getSorth(grid), self.getEast(grid), self.getWest(grid))
        return stateVector

    def selectAction(self, curr_state, qTable, epsilon):
        if np.random.rand() < epsilon:
            # print("epsilon:")
            # print(epsilon)
            action = random.randint(0, 4)
            return action
        poss_actions = list()  # list of possible action's q values
        PU = qTable[curr_state][0]  # pick up q value
        poss_actions.append(PU)
        N = qTable[curr_state][1]  # move north q value
        poss_actions.append(N)
        S = qTable[curr_state][2]  # move south q value
        poss_actions.append(S)
        E = qTable[curr_state][3]  # move east q value
        poss_actions.append(E)
        W = qTable[curr_state][4]  # move west q value
        poss_actions.append(W)
        Max = max(poss_actions)  # the max q value of all possible actions
        #print(Max)
        if (Max == N):
            action = 1
        if (Max == PU):
            action = 0
        elif (Max == S):
            action = 2
        elif (Max == E):
            action = 3
        elif (Max == W):
            action = 4
        return action

    def performAction(self, action, grid):  # perform the action that was selected
        if (action == 0):  # Pick up
            success = self.pickUp(grid)
            if (success == True):
                self.collection += 1
                return 10
            else:
                return -1
        elif (action == 1):  # move North
            success = self.moveNorth(grid)
            if (success == True):
                return 0
            else:
                return -5
        elif (action == 2):  # move South
            success = self.moveSouth(grid)
            if (success == True):
                return 0
            else:
                return -5
        elif (action == 3):  # move East
            success = self.moveEast(grid)
            if (success == True):
                return 0
            else:
                return -5
        elif (action == 4):  # move West
            success = self.moveWest(grid)
            if (success == True):
                return 0
            else:
                return -5


    def train(self, qTable):
        N = 5000  # number of reps for training
        epsilon = 0.1  # greedy action selection
        rewardList = list()
        plotList = list()

        for i in range(N):
            M = 200  # number of reps
            E = 0.2  # 𝜂
            G = 0.9  # 𝛾
            grid = np.random.randint(2, size=(12, 12))  # creates grid
            for j in range(len(grid)):
                for k in range(len(grid[j])):
                    if j == 0 or j == 11 or k == 0 or k == 11:
                        grid[j][k] = -1
            self.x = random.randint(1, 10)
            self.y = random.randint(1, 10)
            self.collection = 0
            self.reward = 0
            totalCans = np.sum(grid == 1)
            for step in range(M):
                curr_state = self.convertState(grid)
                if curr_state not in qTable:  # if first time seeing state then add to Q_matrrix
                    qTable[curr_state] = np.zeros(5)
                action = self.selectAction(curr_state, qTable, epsilon)
                reward = self.performAction(action, grid)
                self.reward += reward
                new_state = self.convertState(grid)
                if new_state not in qTable:  # if first time seeing state then add to Q_matrrix
                    qTable[new_state] = np.zeros(5)
                qTable[curr_state][action] = qTable[curr_state][action] + E * (reward + G * max(qTable[new_state]) - qTable[curr_state][action])
            print("Cans Collected:")
            print(self.collection)
            print("Total Reward:")
            print(self.reward)
            print("Points lost:")
            lost = ((self.collection * 10) - self.reward)
            print(lost)
            print("Iteration:")
            print(i)
            print('\n')
            if i % 50 == 0:
                epsilon -= 0.001
            if i % 100 == 0:
                plotList.append(self.reward)
            rewardList.append(self.reward)
        #print("size:", len(rewardList))
        print("Average Reward(training):")
        print(sum(rewardList) / N)
        plt.plot(plotList)
        plt.show()




    def test(self, qTable):
        N = 5000  # number of reps for testing
        epsilon = 0.1  # greedy action selection
        rewardList = list()
        plotList = list()
        for i in range(N):
            M = 200  # number of reps
            grid = np.random.randint(2, size=(12, 12))  # creates grid
            for j in range(len(grid)):
                for k in range(len(grid[j])):
                    if j == 0 or j == 11 or k == 0 or k == 11:
                        grid[j][k] = -1
            self.x = random.randint(1, 10)
            self.y = random.randint(1, 10)
            self.reward = 0
            for step in range(M):
                curr_state = self.convertState(grid)
                action = self.selectAction(curr_state, qTable, epsilon)
                reward = self.performAction(action, grid)
                self.reward += reward
            if i % 100 == 0:
                plotList.append(self.reward)
            rewardList.append(self.reward)

        print("Average Reward(test):")
        print(sum(rewardList) / N)
        plt.plot(plotList)
        print(len(rewardList))
        plt.show()


if __name__ == '__main__':
    qTable = {}
    Robby = robot()
    Robby.train(qTable)  # trains Robby
    Robby.test(qTable)  # tests Robby+

