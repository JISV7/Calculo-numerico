import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from math import comb, factorial

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
        self.factoriales = []
        
    def cargar_datos(self, num_dias):
        self.temperaturas = np.loadtxt(self.file_path, delimiter=",", skiprows=1, usecols=1)[:num_dias]
        self.x_values = np.arange(len(self.temperaturas))
        print(f"Mostrando {len(self.temperaturas)} dias")
        
    def configurar_interpolacion(self, orden):
        self.n = orden
        self.x0 = len(self.temperaturas) // 2
        if self.x0 + self.n >= len(self.temperaturas):
            raise ValueError(f"Datos insuficientes para orden {self.n}. Necesarios {self.x0 + self.n + 1} dias")

    def calcular_derivada(self, k):
        return sum(((-1)**(k - j)) * comb(k, j) * self.temperaturas[self.x0 + j] for j in range(k + 1))
    
    def generar_polinomio(self):
        self.coeficientes = []
        self.factoriales = []
        for k in range(self.n + 1):
            derivada = self.calcular_derivada(k)
            fact = factorial(k)
            coef = derivada / fact
            self.coeficientes.append(coef)
            self.factoriales.append(fact)
            print(f"Orden {k}: derivada = {derivada:.2f}, factorial = {fact}, coeficiente = {coef:.4f}")
            
        x = sp.symbols('x')
        polinomio = sum(c * (x - self.x0)**i for i, c in enumerate(self.coeficientes))
        self.T_poly = polinomio.expand()
        self.T_func = sp.lambdify(x, self.T_poly, "numpy")
        
        print('\nValores de temperatura:', self.temperaturas)
        print('Factoriales por orden:', self.factoriales)
        print('\nPolinomio simplificado:')
        print(self.T_poly)
    
    def plot_time(self):
        x_fine = np.linspace(self.x_values[0], self.x_values[-1], 200)
        T_values = self.T_func(x_fine)
        
        plt.figure(figsize=(12, 5))
        plt.scatter(self.x_values, self.temperaturas, label="Datos originales", color="blue")
        plt.plot(x_fine, T_values, "--", label=f"Taylor orden {self.n}", color="red")
        plt.xlabel("Dia")
        plt.ylabel("Temperatura (°C)")
        plt.title("Interpolacion de Taylor de Temperaturas Diarias")
        plt.legend()
        plt.grid(True)
        plt.show()

def main():
    interpol = InterpolacionTaylor("open-meteo-10.25N68.only9.csv")
    
    num_dias = int(input('Numero de dias a mostrar: '))
    interpol.cargar_datos(num_dias)
    
    orden = int(input("Orden de la serie: "))
    interpol.configurar_interpolacion(orden)
    interpol.generar_polinomio()
    interpol.plot_time()

if __name__ == "__main__":
    main()