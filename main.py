import os
import numpy as np
import tensorflow as tf
from modelo import crear_modelo, entrenar_modelo
from clasificacion import clasificar_movimiento, mostrar_resultados

# Desactivar las advertencias de TensorFlow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Datos simulados (distancia, velocidad, ángulo)
datos_entrada = np.array([
    [500, 50, 45],  # Ejemplo 1
    [1500, -30, 90],  # Ejemplo 2
    [200, 0, 60],  # Ejemplo 3
    [1800, 70, 30],  # Ejemplo 4
    [300, -20, 120],  # Ejemplo 5
    [2000, -200, 120],  # Ejemplo 6
    [300, -20, 120],  # Ejemplo 7
    [1111, 0, 30],  # Ejemplo 8
    [300, 80, 45],  # Ejemplo 9
    [1000, 70, 85]  # Ejemplo 10
], dtype=float)

# Etiquetas de salida: [movimiento (0=fijo, 1=lento, 2=rápido), distancia futura en mm]
etiquetas_salida = np.array([
    [1, 650],  # Movimiento lento
    [1, 1410],  # Movimiento lento
    [0, 200],  # Fijo
    [2, 2010],  # Movimiento rápido
    [1, 240],  # Movimiento lento
    [2, 1400],  # Movimiento rápido
    [1, 240],  # Movimiento lento
    [0, 1111],  # Fijo
    [2, 540],  # Movimiento rápido
    [2, 1210]  # Movimiento rápido
], dtype=float)

# Crear y entrenar el modelo
modelo = crear_modelo()
entrenar_modelo(modelo, datos_entrada, etiquetas_salida)

# Realizar predicciones
nueva_entrada = np.array([[1000, 100, 60]])  # Distancia=1000 mm, Velocidad=-60 mm/s, Ángulo=60°
prediccion = modelo.predict(nueva_entrada)
movimiento, distancia_futura = prediccion[0]

# Clasificación del movimiento
movimiento_clasificado = clasificar_movimiento(movimiento)

# Mostrar resultados
mostrar_resultados(movimiento_clasificado, distancia_futura)