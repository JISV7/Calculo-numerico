import numpy as np
import matplotlib.pyplot as plt

# Clase para manejar los datos meteorológicos
class DatosMeteorologicos:
    def __init__(self, archivo):
        # Cargar datos desde el archivo CSV
        self.tiempos, self.temperaturas = self._cargar_datos(archivo)
        self.dias = np.arange(len(self.tiempos))  # Convertir tiempos a días numéricos

    def _cargar_datos(self, archivo):
        tiempos = []
        temperaturas = []
        with open(archivo, 'r') as file:
            next(file)  # Saltar la primera línea (encabezado)
            for linea in file:
                tiempo, temp = linea.strip().split(',')
                tiempos.append(tiempo)
                temperaturas.append(float(temp))
        return tiempos, temperaturas

    def interpolar_polinomio_trozos(self):
        # Interpolación lineal a trozos manualmente
        self.interpolacion = self._interpolacion_lineal_trozos()

    def _interpolacion_lineal_trozos(self):
        # Función para calcular la interpolación lineal a trozos
        def interpolador(x):
            for i in range(len(self.dias) - 1):
                if self.dias[i] <= x <= self.dias[i + 1]:
                    # Ecuación de la recta entre dos puntos
                    pendiente = (self.temperaturas[i + 1] - self.temperaturas[i]) / (self.dias[i + 1] - self.dias[i])
                    return self.temperaturas[i] + pendiente * (x - self.dias[i])
            return np.nan  # Fuera del rango
        return interpolador

    def graficar_datos(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.dias, self.temperaturas, 'o', label='Datos Originales')
        dias_interpolados = np.linspace(min(self.dias), max(self.dias), 500)
        temperaturas_interpoladas = [self.interpolacion(x) for x in dias_interpolados]
        plt.plot(dias_interpolados, temperaturas_interpoladas, '-', label='Interpolación Polinómica a Trozos')
        plt.xlabel('Días desde el inicio')
        plt.ylabel('Temperatura (°C)')
        plt.title('Interpolación Polinómica a Trozos de Temperaturas Diarias')
        plt.legend()
        plt.grid(True)
        plt.show()

# Ruta al archivo CSV (ajusta la ruta según sea necesario)
archivo_csv = "open-meteo-10.25N68.only9.csv"
# Creación del objeto DatosMeteorologicos
datos_meteo = DatosMeteorologicos(archivo_csv)

# Interpolación polinómica a trozos
datos_meteo.interpolar_polinomio_trozos()

# Graficación de los datos y la interpolación
datos_meteo.graficar_datos()