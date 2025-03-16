import numpy as np
import sympy as sp
from math import comb
import matplotlib.pyplot as plt

class InterpolacionTaylor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.temperaturas = None
        self.x_values = None
        self.x0 = None
        self.n = None
        self.coeficientes = []
        self.T_poly = None
        self.T_func = None
        
    def cargar_datos(self, num_dias):
        self.temperaturas = np.loadtxt(self.file_path, delimiter=",", skiprows=1, usecols=1)[:num_dias]
        self.x_values = np.arange(len(self.temperaturas))
        print(f"Mostrando {len(self.temperaturas)} dias")
        
    def configurar_interpolacion(self, orden):
        self.n = orden
        self.x0 = len(self.temperaturas) // 2
        if len(self.temperaturas) < 2*self.n + 1:
            raise ValueError(f"Se necesitan al menos {2*self.n + 1} puntos para orden {self.n}")

    def calcular_derivadas(self):
        h=1
        return [sum((-1)**(m-k)*comb(m,k)*self.temperaturas[self.x0-1+k] for k in range(m+1))/h**m for m in range(self.n+1)]

    def generar_polinomio(self):
        derivadas = self.calcular_derivadas()
        
        x = sp.symbols('x')
        poly = 0
        for k in range(self.n + 1):
            term = (derivadas[k]/sp.factorial(k)) * (x - self.x0)**k
            poly += term
        
        self.T_poly = poly.expand()
        self.T_func = sp.lambdify(x, self.T_poly, 'numpy')
        
        print(f"Temperaturas: {self.temperaturas}")
        print(f"Derivadas obtenidas: {derivadas}")
        print("\nPolinomio de Taylor generado:")
        print(self.T_poly)

    def plot_time(self):
        x_fine = np.linspace(self.x_values[0], self.x_values[-1], 200)
        T_values = self.T_func(x_fine)
        
        plt.figure(figsize=(12, 5))
        plt.scatter(self.x_values, self.temperaturas, label="Datos originales", color="blue")
        plt.plot(x_fine, T_values, "--", label=f"Taylor orden {self.n}", color="red")
        plt.xlabel("Día")
        plt.ylabel("Temperatura (°C)")
        plt.title(f"Interpolación de Taylor de orden {self.n} en x0 = {self.x0}")
        plt.legend()
        plt.grid(True)
        plt.xlim(self.x_values[0]-1, self.x_values[-1]+1)
        plt.ylim(min(self.temperaturas)-1, max(self.temperaturas)+1)
        plt.show()

def main():
    interpol = InterpolacionTaylor("open-meteo-10.25N68.only9.csv")
    
    num_dias = 7
    interpol.cargar_datos(num_dias)
    
    orden = 3
    interpol.configurar_interpolacion(orden)
    interpol.generar_polinomio()
    interpol.plot_time()

if __name__ == "__main__":
    main()