# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 19:14:26 2022

@author: Miguel
"""
import numpy as np
import pandas as pd
import random


datos1 = pd.read_csv("datos.csv")
datos = np.array(datos1)
nodos = [0,1,2,3,4]
modelEnd = [4, 1, 0, 3, 2]

largeIndividual = 5 
num=10
generation = 10 #Generaciones
pressure = 3 #individual>2
mutation_chance = 0.8

def individual(min, max):
    return[random.randint(min, max) for i in range(largeIndividual)]

def newPopulation():
    return [random.sample(range(5),5) for i in range(num)]



# Funcion objetivo
def functionType(individual):
    fitness = 0
    for i in range(len(individual)):
        if individual[i] == modelEnd[i]:
            fitness += 1
    return fitness

def selection_and_reproduction(population):
    evaluating = [ (functionType(i), i) for i in population]
    #print("eval",evaluating)
    evaluating = [i[1] for i in sorted(evaluating)]
    #print("eval",evaluating)
    population = evaluating
    #print("poblacion gaaa",population)
    selected = evaluating[(len(evaluating)-pressure):]
    #print ("selecionados",selected)
    for i in range(len(population)-pressure):
        pointChange = random.randint(1,largeIndividual-1)
        #print("punto de cambio",pointChange)
        father = random.sample(selected, 2)
        #print("padre",father)
        population[i][:pointChange] = father[0][:pointChange]
        #print("poblacion en i",population[i])
        population[i][pointChange:] = father[1][pointChange:]
        
    for i in range(len(population)-pressure):
        v =[]
        p =[]
        for j in range (5):
            if population[i].count(j)==0:
                v.append(j)
            elif population[i].count(j)==2:
                p.append(j)
            #print("numero que se repite",population[i].count(j))
        for j in range (len(p)):
            population[i].reverse()
            a = population[i].index(p[j])
            population[i][a] =v[j]
            population[i].reverse()
        #print("pos", p)
        #print("val", v)
    return population

def mutation(population):
    for i in range(len(population)-pressure):
        if random.random() <= mutation_chance: 
            pointChange = random.randint(1,largeIndividual-1) 
            new_val = random.randint(0,4) 
            while new_val == population[i][pointChange]:
                new_val = random.randint(0,4)
            population[i][pointChange] = new_val
    for i in range(len(population)-pressure):
        v =[]
        p =[]
        for j in range (5):
            if population[i].count(j)==0:
                v.append(j)
            elif population[i].count(j)==2:
                p.append(j)
        for j in range (len(p)):
            population[i].reverse()
            a = population[i].index(p[j])
            population[i][a] =v[j]
            population[i].reverse()
    return population

def ruta(population):
    suma=[]
    for i in range(len(population)):
        a=[]
        for j in range(4):
           #print(datos[population[i][j]][population[i][j+1]]) 
           a.append(datos[population[i][j]][population[i][j+1]]) 
        
        a.append(datos[population[i][4]][population[i][0]])
        #print(a)
        suma.append(sum(a))
    return suma
# Principal


population = newPopulation()
print(datos)

print("\nPopulation Begin:\n%s"%(population))
for i in range (generation):
    population = selection_and_reproduction(population)
    population = mutation(population)
    #print("\nMutation:\n%s"%(population))
    rut = ruta(population)
    
    #print("rut",rut)
    a= rut.index(min(rut))
    print("ruta minima",min(rut))
    #print(a)
    print("ruta ", population[a])
    




#print (nodos)

