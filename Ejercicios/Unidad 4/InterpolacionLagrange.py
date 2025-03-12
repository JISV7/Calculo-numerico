import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

class InterpolacionLagrange:
    def __init__(self, file_path):
        self.file_path = file_path
        self.temperaturas = None
        self.x_values = None
        self.L_poly = None
        self.L_func = None
        self.divisoresL = None
        
    def cargar_datos(self, num_dias):
        self.temperaturas = np.loadtxt(self.file_path, delimiter=",", skiprows=1, usecols=1)[:num_dias]
        self.x_values = np.arange(len(self.temperaturas))
        print(f"Mostrando {len(self.temperaturas)} dias")
        
    def generar_polinomio(self):
        x = sp.symbols('x')
        n = len(self.temperaturas)
        polinomio = 0
        self.divisoresL = np.zeros(n, dtype=float)
        
        for i in range(n):
            term = self.temperaturas[i]
            denominador = 1
            for j in range(n):
                if j != i:
                    num = (x - self.x_values[j])
                    den = (self.x_values[i] - self.x_values[j])
                    term *= num / den
                    denominador *= den
            self.divisoresL[i] = denominador
            polinomio += term
        
        self.L_poly = polinomio.expand()
        self.L_func = sp.lambdify(x, self.L_poly, "numpy")
        
        print('\nValores de temperaturas:', self.temperaturas)
        print('Divisores en L(i):', self.divisoresL)
        print('\nPolinomio simplificado:')
        print(self.L_poly)
    
    def plot_time(self):
        x_fine = np.linspace(self.x_values[0], self.x_values[-1], 200)
        L_values = self.L_func(x_fine)
        
        plt.figure(figsize=(12, 5))
        plt.scatter(self.x_values, self.temperaturas, label="Datos originales", color="blue")
        plt.plot(x_fine, L_values, "--", label="Interpolación Lagrange", color="green")
        plt.xlabel("Dia")
        plt.ylabel("Temperatura (°C)")
        plt.title("Interpolación de Lagrange de Temperaturas Diarias")
        plt.legend()
        plt.grid(True)
        plt.show()
        
def main():
    interpol = InterpolacionLagrange("open-meteo-10.25N68.only9.csv")
    
    num_dias = int(input('Numero de dias a mostrar: '))
    interpol.cargar_datos(num_dias)
    
    interpol.generar_polinomio()
    interpol.plot_time()

if __name__ == "__main__":
    main()