# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 14:35:49 2020

@author: Brayan Dennis Aguilar
Materia: INF - 354
    PREGUNTA 1 Usando DEAP
"""

# Importamos las librerias necesarias para el algoritmo genetico
import array
import random

import numpy
import pandas

# Librerias de Deap
from deap import algorithms
from deap import base
from deap import creator
from deap import tools

# Leemos los datos de un archivo csv 
datos= pandas.read_csv('Datos.csv')

# Convertimos en un array de numpy para el tratamiento y lo guardamos las distancias en una varible nueva
distance_mat = datos.to_numpy()

# Guardamos el tamaño de la matriz (numero de lugares) 
IND_SIZE = len(distance_mat)

# Definimos el tipo de problema en este caso es minimizacion 
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))

#  Definimos el Individuo que es de tipo integer 
creator.create("Individual", array.array, typecode='i', fitness=creator.FitnessMin)

# Operaciones 
toolbox = base.Toolbox()

# Funcion que llena los individuos 
toolbox.register("indices", random.sample, range(IND_SIZE), IND_SIZE)

# Funciones de inicilización del individuo y de la población
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Funcion Objetivo (Agente Viajero)
def evalAGV(individual):
    # Sacamos la primera distancia del individuo  
    distance = distance_mat[individual[-1]][individual[0]]
    # Recorremos el individuo formando tuplas para sacar el valor de la distancia  
    for pos1, pos2 in zip(individual[0:-1], individual[1:]):
        # Sumamos las distancias 
        distance += distance_mat[pos1][pos2]
    # Retornamos la suma
    return distance,

# Operaciones 
toolbox.register("mate", tools.cxPartialyMatched)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", evalAGV)

# Funcion principal 
def main():
    # Iniciamos la semilla en 0
    seed=0
    random.seed(seed)
    # Genermamos la poblacion con una cantidad de 
    pop = toolbox.population(n=100)
    
    # Sacamos al mejor individuo
    hof = tools.HallOfFame(1)
    # Estadisticas Basicas 
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)
    

    algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=40, stats=stats,
                        halloffame=hof, verbose=True) 
    return pop, stats, hof

if __name__ == "__main__":
    pop, stats, hof=main()
    print(" ")
    print("La mejor ruta es: ")
    print(hof)
    print(" ")
    print("Lugares a visitar: ")
    for i in range(len(datos)):
        print(datos.columns.values[hof[0][i]])

    