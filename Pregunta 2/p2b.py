# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 16:47:12 2020

@author: Brayan Dennis Aguilar
Materia: INF - 354
    PREGUNTA 2 Sin el uso de librerias
"""

# Se necesita los elementos aleatorios 
import random


largo = 10 #La longitud del material genetico de cada individuo
num = 10 #La cantidad de individuos que habra en la poblacion
ng = 100 #Cantidad de generaciones 
pressure = 3 #Cuantos individuos se seleccionan para reproduccion. Necesariamente mayor que 2
mutation_chance = 0.5 #La probabilidad de que un individuo mute
  
print("\n\nFuncion F(x): x^3+x^2+x %s\n") #Mostrar el modelo, con un poco de espaciado

  
def individual(min, max):
    """
        Crea un individual
    """
    return[random.randint(min, max) for i in range(largo)]
  
def crearPoblacion():
    """
        Crea una poblacion nueva de individuos
    """
    return [individual(0,1) for i in range(num)]
  
def funcionObjetivo(individual):
    """
        Calcula la funcion definida.
    """

    decimal = int("".join(map(str, individual)),2)
    
    y = decimal**3+decimal**2+decimal
    
    return y

  
def selection_and_reproduction(population):
    """
        Puntua todos los elementos de la poblacion (population) y se queda con los mejores
        guardandolos dentro de 'selected'.
        Despues mezcla el material genetico de los elegidos para crear nuevos individuos y
        llenar la poblacion (guardando tambien una copia de los individuos seleccionados sin
        modificar).
  
        Por ultimo muta a los individuos.
  
    """
    puntuados = [ (funcionObjetivo(i), i) for i in population] #Calcula el fitness de cada individuo, y lo guarda en pares ordenados de la forma (5 , [1,2,1,1,4,1,8,9,4,1])
    
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

funcionO = [] # array para guardar el resultado de la funcion objetivo en decimal

for i in population:
    funcionO.append(int("".join(map(str,i)),2)) # Añadimos al array el resultado en decimal del individuo

print("\nResultado de las funcion F(x) en decimal:\n%s"%(funcionO)) #Se muestra los resultados de la funcion f(x)