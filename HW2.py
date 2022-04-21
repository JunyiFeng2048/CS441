import numpy as np
from numpy import random
import copy
import matplotlib.pyplot as plt

populationSize = 100
mutationPct = 0.9  # 10%

avgFitness = []
generation = []


def calFitness(chromosomes):    #cal each chromosomes' fitness value
    attack = 0
    for i in range(len(chromosomes) - 1):
        for j in range(i + 1, len(chromosomes)):
            if chromosomes[i] == chromosomes[j]:
                attack += 1
    for i in range(len(chromosomes) - 1):
        for j in range(i + 1, len(chromosomes)):
            if abs(chromosomes[j] - chromosomes[i]) == abs(j - i):
                attack += 1
    return 28 - attack


def fitness(population):
    tempFitnessList = []
    for chromosomes in population:
        fitnessValue = calFitness(chromosomes)
        if fitnessValue == 28:
            print("Find solution: ")
            print("generation: ",generation[len(generation)-1])
            print(chromosomes)
            return 28
        tempFitnessList.append(fitnessValue)
    return tempFitnessList


def percentage(fitnessList, fitnessPercentage):
    # global avgFitness
    total = 0
    for i in fitnessList:
        total += i
    # print(total)
    for j in range(0, len(fitnessList)):
        fitnessPercentage.append(fitnessList[j] / total)
    avgFitness.append(total / populationSize)   #average fitness value for this gen


def crossover(newPopulation):
    for i in range(0, populationSize, 2):
        crossValue1 = random.randint(0, 3)
        crossValue2 = random.randint(4, 7)
        for j in range(crossValue1, crossValue2):
            temp1 = copy.deepcopy(newPopulation[i][j])
            temp2 = copy.deepcopy(newPopulation[i + 1][j])
            newPopulation[i][j] = temp2
            newPopulation[i + 1][j] = temp1


def mutation(chromosomes):
    pct = np.random.rand(8)
    for i in range(len(pct)):
        if pct[i] > mutationPct:
            chromosomes[i] = random.randint(0, 8)
    return chromosomes


def GA():
    if populationSize % 2 == 1:
        print("population must be even")
        return

    numIterations = 0
    population = []
    for i in range(populationSize):
        population.append(np.random.choice(range(8), 8))
    # print(population)
    # while numIterations < 2:
    while 1:
        if numIterations == 100000:
            print("reach maximum iterations!")
            return

        #print("generation : ", numIterations)
        fitnessList = []
        fitnessPercentage = []
        newPopulation = []

        fitnessList = fitness(population)
        if fitnessList == 28:
            return

        percentageList = percentage(fitnessList, fitnessPercentage)
        selectedChromosomes = np.random.choice(range(populationSize), populationSize, replace=True, p=percentageList)
        for chromosomesIndex in selectedChromosomes:
            newPopulation.append(population[chromosomesIndex])

        crossover(newPopulation)

        for i in range(populationSize):
            newPopulation[i] = copy.deepcopy(mutation(newPopulation[i]))

        population = newPopulation


        """if numIterations % 20 == 0:
            print("generation : ", numIterations)
            print(population)"""
        print("generation : ", numIterations)
        print(population)
        numIterations += 1
        generation.append(numIterations)


GA()
# plt.scatter(generation, avgFitness)
linear_model = np.polyfit(generation, avgFitness, 12)
linear_model_fn = np.poly1d(linear_model)
x_s = np.arange(0, len(generation))
plt.plot(x_s, linear_model_fn(x_s), color="blue")
plt.show()
