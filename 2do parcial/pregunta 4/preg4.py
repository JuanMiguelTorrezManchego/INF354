# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 10:58:46 2022

@author: Miguel
"""


import array
import random
import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
import pandas as pd


datos1 = pd.read_csv("datos.csv")
tsp = numpy.array(datos1)
nodos = [0,1,2,3,4]


creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", array.array, typecode='i', fitness=creator.FitnessMin)

toolbox = base.Toolbox()

# Attribute generator
toolbox.register("indices", random.sample, range(5), 5)

# Structure initializers
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def funcionObjetivo(individual):
    distance = tsp[individual[-1]][individual[0]]
    for gene1, gene2 in zip(individual[0:-1], individual[1:]):
        distance += tsp[gene1][gene2]
    return distance,

toolbox.register("mate", tools.cxPartialyMatched)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", funcionObjetivo)

def main():
    random.seed(169)

    pop = toolbox.population(n=300)

    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    algorithms.eaSimple(pop, toolbox, 0.7, 0.2, 40, stats=stats, 
                        halloffame=hof)

    return pop, stats, hof

if __name__ == "__main__":
    main()