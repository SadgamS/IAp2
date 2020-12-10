# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 00:14:36 2020
@author: Brayan Dennis Aguilar
Materia: INF - 354
    PREGUNTA 3 Implementacion de una red neuronal 
"""

# Importamos las librerias 
import pandas as pd

from sklearn import preprocessing
# librerias para dividir los datos (dos opciones)
from sklearn.model_selection import train_test_split  
from sklearn.model_selection import StratifiedShuffleSplit
# Para sacar las metricas de la red neuronal
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
# la red neuronal
from sklearn.neural_network import MLPClassifier

# Cargamos los datos en un dataframe
datos =pd.read_csv('crx.csv')

# Definimos las entradas para la red neuronal
X = datos[['A3','A8','A15']] # entradas
y = datos['A1'] # salida


# Dividimos los datos en entrenamiento y testeo donde 80% es entrenamiento y 20% test
# usamos el primer metodo /train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2)

# Definimos la red neuronal
cl = MLPClassifier(hidden_layer_sizes=(10,10,10), max_iter=600, alpha=0.0001,
                   solver='sgd', random_state=21)
# ingresamos los datos de entrenamiento
cl.fit(X_train,y_train)
# hacemos la prediccion 
pred = cl.predict(X_test)

# Sacamos la matriz de confusion 
cm = confusion_matrix(y_test, pred)
# Precision de la red neuronal
dt_acc = accuracy_score(y_test, pred)
# mostramos el resultados de la red neuronal
print("\nResultados de la Red Neuronal:\n%s"%(classification_report(y_test,pred))) 

print("\nPrecision de la Red Neuronal:\n%s"%(round(100*dt_acc,0)),'%') 

print("\nMatriz de Confusion:\n%s"%(cm)) 

print("\n---Segunda forma de division de datos:")

# Para poder dividir los datos con este metodo es necesario hacer un preprocesamiento 
# hacemos un escalado estandar para las entradas
X1 = preprocessing.StandardScaler().fit(X).transform(X) 

# Definimos la funcion y damos 80% al entrenamiento y 20% al test
sss = StratifiedShuffleSplit(n_splits=5, test_size=0.2, random_state=0) 
scores = [] # para almacenar la precision de cada division 
# Sacamos los indices dividos de los datos
for train_index1, test_index1 in sss.split(X1, y):
    # guardamos los datos de entrenamiento y test
    X_train1, X_test1 = X1[train_index1], X1[test_index1] 
    y_train1, y_test1 = y[train_index1], y[test_index1] 
    # ingresamos los datos de entrenamiento
    cl.fit(X_train1, y_train1)
    # hacemos la prediccion 
    pred1 = cl.predict(X_test1)
    # guardamos la precision 
    scores.append(accuracy_score(y_test1, pred1))
 
    
print("\nArray de precision:\n%s"%(scores))
# Sacamos la matriz de confusion 
cm1 = confusion_matrix(y_test1, pred1)
print("\nMatriz de Confusion:\n%s"%(cm1)) 
print("\nResultados de la Red Neuronal:\n%s"%(classification_report(y_test1,pred1)))

