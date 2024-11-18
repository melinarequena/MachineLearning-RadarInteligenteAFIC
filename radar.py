import tensorflow as tf
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Desactiva las advertencias

# Datos simulados (distancia, velocidad, ángulo) -> Movimiento y distancia futura
# Distancia en mm, velocidad en mm/s, ángulo en grados
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
# Movimiento definido por velocidad: lento (|v| <= 30 mm/s), rápido (|v| > 30 mm/s)
etiquetas_salida = np.array([
    [1, 650],  # Movimiento lento, distancia futura a 3 s
    [1, 1410],  # Movimiento lento
    [0, 200],  # Fijo
    [2, 2010],  # Movimiento rápido
    [1, 240],  # Movimiento lento
    [2, 1400],  # Movimiento rapido
    [1, 240],  # Movimiento lento
    [0, 1111],  # Movimiento fijo
    [2, 540],  # Movimiento rapido
    [2, 1210]  # Movimiento rapido

], dtype=float)

# Definición de la red neuronal
entrada = tf.keras.layers.Dense(units=3, input_shape=[3])  # 3 entradas
oculta1 = tf.keras.layers.Dense(units=6, activation='relu')  # Capa oculta con 6 neuronas
oculta2 = tf.keras.layers.Dense(units=6, activation='relu')  # Segunda capa oculta
salida = tf.keras.layers.Dense(units=2)  # 2 salidas (movimiento, distancia futura)

modelo = tf.keras.Sequential([entrada, oculta1, oculta2, salida])

# Compilación del modelo
modelo.compile(
    optimizer=tf.keras.optimizers.Adam(0.1),
    loss='mean_squared_error'
)

# Entrenamiento
print("Comenzando el entrenamiento...\n")
historial = modelo.fit(datos_entrada, etiquetas_salida, epochs=500, verbose=False)
print("¡Entrenamiento finalizado!\n")

# Visualización de la pérdida
#plt.xlabel("# Época")
#plt.ylabel("Magnitud de pérdida")
#plt.plot(historial.history["loss"])
#plt.show()

# Predicciones
print("Realizando predicciones...\n")
nueva_entrada = np.array([[1000, 100, 60]])  # Distancia=1000 mm, Velocidad=-60 mm/s, Ángulo=60°
prediccion = modelo.predict(nueva_entrada)
movimiento, distancia_futura = prediccion[0]

# Clasificación del movimiento
# Verifica el valor de 'movimiento' antes de clasificar
print(f"Valor de velocidad asignado: {movimiento}")

# Clasificación del movimiento
if -0.95 < movimiento < 0.95 and abs(movimiento) > 0.1:  # Lento, entre -0.95 y 0.95, pero no en 0
    movimiento_clasificado = "Lento"
elif abs(movimiento) >= 1:  # Rápido, si el valor absoluto es mayor o igual a 1
    movimiento_clasificado = "Rápido"
else:  # Si no es lento ni rápido, debe ser fijo
    movimiento_clasificado = "Fijo"


print("\nPrediccion:")
print(f"Movimiento clasificado: {movimiento_clasificado}")
print(f"Movimiento: {movimiento_clasificado}")
print(f"Distancia futura (3 s): {distancia_futura:.2f} mm")

# Variables de las capas
#print("Pesos de las capas:")
#print(entrada.get_weights())
#print(oculta1.get_weights())
#print(oculta2.get_weights())
#print(salida.get_weights())
