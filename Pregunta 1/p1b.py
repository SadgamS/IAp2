# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 00:30:14 2020

@author: Brayan Dennis Aguilar
Materia: INF - 354
    PREGUNTA 1 Sin el uso de librerias
"""

# Se necesita los elementos aleatorios y los datos de un archivo csv
import random
import pandas

  
largo = 4 #La longitud del material genetico de cada individuo
num = 16 #La cantidad de individuos que habra en la poblacion
ng = 100 #Cantidad de generaciones 
pressure = 3 #Cuantos individuos se seleccionan para reproduccion. Necesariamente mayor que 2
mutation_chance = 0.5 #La probabilidad de que un individuo mute


# Leemos los datos de un archivo csv 
datos= pandas.read_csv('Datos.csv')

print("\n\nMatriz de Distacias: %s\n"%(datos)) #Mostrar el modelo, con un poco de espaciado

# Convertimos en un array de numpy para el tratamiento y lo guardamos las distancias en una varible nueva
distance_mat = datos.to_numpy()

  
def individual(min, max):
    """
        Crea un individual
    """
    return[random.randint(min, max) for i in range(largo)]
  
def crearPoblacion():
    """
        Crea una poblacion nueva de individuos
    """
    return [individual(0,3) for i in range(num)]
  
# Funcion Objetivo
def calcularMejorRuta(individual):
    """
        Se hace uso el algoritmo de las n reinas para que que no exista numeros repetidos en lo posible.
    """
    
    size = len(individual)
    # Los ataques sólo pueden ser en las diagonales
    diagonal_izquierda_derecha = [0] * (2*size-1)
    diagonal_derecha_izquierda = [0] * (2*size-1)
    
    # Número de reinas en cada diagonal
    for i in range(size): # recorremos las columnas
        diagonal_izquierda_derecha[i+individual[i]] += 1 # [columna + fila]
        diagonal_derecha_izquierda[size-1-i+individual[i]] += 1 # [size-1-columna+ fila]
    
    # Número de ataques en cada diagonal
    suma = 0
    for i in range(2*size-1): # recorremos todas las diagonales
        if diagonal_izquierda_derecha[i] > 1: # hay ataques
            suma += diagonal_izquierda_derecha[i] - 1 # n-1 ataques
        if diagonal_derecha_izquierda[i] > 1:
            suma += diagonal_derecha_izquierda[i] - 1
    return suma,

  
def selection_and_reproduction(population):
    """
        Puntua todos los elementos de la poblacion (population) y se queda con los mejores
        guardandolos dentro de 'selected'.
        Despues mezcla el material genetico de los elegidos para crear nuevos individuos y
        llenar la poblacion (guardando tambien una copia de los individuos seleccionados sin
        modificar).
  
        Por ultimo muta a los individuos.
  
    """
    puntuados = [ (calcularMejorRuta(i), i) for i in population] #Calcula el fitness de cada individuo, y lo guarda en pares ordenados de la forma (5 , [1,2,1,1,4,1,8,9,4,1])
    
    puntuados = [i[1] for i in sorted(puntuados)] #Ordena los pares ordenados y se queda solo con el array de valores
    
    population = puntuados
  
  
  
    selected =  puntuados[(len(puntuados)-pressure):] #Esta linea selecciona los 'n' individuos del final, donde n viene dado por 'pressure'
    print(selected)
  
  
    #Se mezcla el material genetico para crear nuevos individuos
    for i in range(len(population)-pressure):
        punto = random.randint(1,largo-1) #Se elige un punto para hacer el intercambio
        padre = random.sample(selected, 2) #Se eligen dos padres
          
        population[i][:punto] = padre[0][:punto] #Se mezcla el material genetico de los padres en cada nuevo individuo
        population[i][punto:] = padre[1][punto:]
  
    return population #El array 'population' tiene ahora una nueva poblacion de individuos, que se devuelven
  
def mutation(population):
    """
        Se mutan los individuos al azar. Sin la mutacion de nuevos genes nunca podria
        alcanzarse la solucion.
        Se esta usando el algoritmo mutShuffleIndexes de deap
    """
    size = len(population)
    for i in range(size):
        if random.random() < mutation_chance:
            swap_indx = random.randint(0, size - 2)
            if swap_indx >= i:
                swap_indx += 1
            population[i], population[swap_indx] = \
                population[swap_indx], population[i]

    return population
      
  
  
population = crearPoblacion()#Inicializar una poblacion
print("Poblacion Inicial:\n%s"%(population)) #Se muestra la poblacion inicial
  
  
#Se evoluciona la poblacion
for i in range(ng):
    population = selection_and_reproduction(population)
    population = mutation(population)
  
  
print("\nPoblacion Final:\n%s"%(population)) #Se muestra la poblacion evolucionada


sumdistance=[] # array para guardar el resultado de la suma de las distancias

for individuo in population: # Sacamos los individuos de la poblacion
     distance = distance_mat[individuo[-1]][individuo[0]] # Añadimos la distancia final
     for pos1, pos2 in zip(individuo[0:-1], individuo[1:]): # Sacamos tuplas del individuo
         distance += distance_mat[pos1][pos2] # Sumamos la distancia 
     sumdistance.append(distance) # Añadimos al array la suma de la distancia del individuo
     distance = 0 # Resetamos la distancia para el siguiente iteracion 

print("\nSuma de las distancias de la poblacion final:\n%s"%(sumdistance)) #Se muestra la distancia sumada de la poblacion

