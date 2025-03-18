#Franyer Marin: C.I: 32.293.396
#Jose Sanchez: C.I: 30.958.324
#Luis Pena: C.I: 30512332

import numpy as np
import matplotlib.pyplot as plt

class DatosMeteorologicos:
    def __init__(self, archivo):
        self.tiempos, self.temperaturas = self._cargar_datos(archivo)
        self.dias = np.arange(len(self.tiempos))  # Convertir tiempos a días numéricos

    def _cargar_datos(self, archivo):
        tiempos = []
        temperaturas = []
        with open(archivo, 'r') as file:
            next(file)  # Saltar la primera línea
            for _ in range(7):
                linea = file.readline().strip()
                if not linea:
                    break
                tiempo, temp = linea.split(',')
                tiempos.append(tiempo)
                temperaturas.append(float(temp))
        return tiempos, temperaturas

    def interpolar_polinomio_trozos(self):
        self.interpolacion = self._interpolacion_lineal_trozos()

    def _interpolacion_lineal_trozos(self):
        def interpolador(x):
            for i in range(len(self.dias) - 1):
                if self.dias[i] <= x <= self.dias[i + 1]:
                    pendiente = (self.temperaturas[i + 1] - self.temperaturas[i]) / (self.dias[i + 1] - self.dias[i])
                    return self.temperaturas[i] + pendiente * (x - self.dias[i])
            return np.nan
        return interpolador

    def graficar_datos(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.dias, self.temperaturas, 'o', label='Datos Originales')
        dias_interpolados = np.linspace(min(self.dias), max(self.dias), 500)
        temperaturas_interpoladas = [self.interpolacion(x) for x in dias_interpolados]
        plt.plot(dias_interpolados, temperaturas_interpoladas, '-', label='Interpolación Lineal a Trozos')
        plt.xlabel('Días desde el inicio')
        plt.ylabel('Temperatura (°C)')
        plt.title('Interpolación Lineal a Trozos de Temperaturas Diarias (7 días)')
        plt.legend()
        plt.grid(True)
        plt.xlim(self.dias[0]-1, self.dias[-1]+1)
        plt.ylim(min(self.temperaturas)-1, max(self.temperaturas)+1)
        plt.show()

# Uso del código
archivo_csv = "open-meteo-10.25N68.only9.csv"
datos_meteo = DatosMeteorologicos(archivo_csv)
datos_meteo.interpolar_polinomio_trozos()
datos_meteo.graficar_datos()