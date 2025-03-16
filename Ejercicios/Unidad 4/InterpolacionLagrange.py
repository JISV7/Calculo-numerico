import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

class InterpolacionLagrange:
    def __init__(self, file_path):
        self.file_path = file_path
        self.temperaturas = None
        self.x_values = None
        self.poly = None
        self.func = None
        
        

    def cargar_datos(self, num_dias):
        self.temperaturas = np.loadtxt(self.file_path, delimiter=",", skiprows=1, usecols=1)[:num_dias]
        self.x_values = np.arange(len(self.temperaturas))
        print(f"Mostrando {len(self.temperaturas)} dias")

    def lagrange_polynomial(self):
        # Declaramos la variable simbólica
        x = sp.symbols('x')
        n = len(self.x_values)
        L = 0
        
        # Fórmula de interpolación de Lagrange:
        # L(x) = suma_{j=0}^{n-1} [ y_j * (producto_{i=0, i != j}^{n-1} (x - x_i)/(x_j - x_i) ) ]
        for j in range(n):
            term = self.temperaturas[j]
            for i in range(n):
                if i != j:
                    term *= (x - self.x_values[i]) / (self.x_values[j] - self.x_values[i])
            L += term
        
        # Simplificamos el polinomio resultante
        self.poly = sp.simplify(L)
        # Convertimos a función numérica
        self.func = sp.lambdify(x, self.poly, 'numpy')
        print(f"Temperaturas: {self.temperaturas}")
        return self.poly

    def plot_interpolation(self):
        # Creamos un rango fino de valores para x para graficar la curva interpolada
        x_vals = np.linspace(min(self.x_values), max(self.x_values), 200)
        y_vals = self.func(x_vals)
        
        plt.figure(figsize=(12, 5))
        plt.scatter(self.x_values, self.temperaturas, label="Datos originales", color="blue")
        plt.plot(x_vals, y_vals, label="Interpolación de Lagrange", color="red")
        plt.xlabel("Día")
        plt.ylabel("Temperatura (°C)")
        plt.title("Interpolación de Lagrange")
        plt.legend()
        plt.grid(True)
        plt.xlim(self.x_values[0]-1, self.x_values[-1]+1)
        plt.ylim(min(self.temperaturas)-1, max(self.temperaturas)+1)
        plt.show()

def main():
    interpol = InterpolacionLagrange("open-meteo-10.25N68.only9.csv")

    num_dias = 7
    interpol.cargar_datos(num_dias)
    
    poly = interpol.lagrange_polynomial()
    
    print("Polinomio de interpolación de Lagrange:")
    sp.pprint(poly)
    
    interpol.plot_interpolation()

if __name__ == "__main__":
    main()
