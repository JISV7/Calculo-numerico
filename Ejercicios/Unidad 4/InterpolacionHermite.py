import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

class InterpolacionHermite:
    def __init__(self, file_path):
        self.file_path = file_path
        self.temperaturas = None
        self.x_values = None
        self.derivadas = None
        self.H_poly = None
        self.H_func = None
        self.denominadores = None
        
    def cargar_datos(self, num_dias):
        self.temperaturas = np.loadtxt(self.file_path, delimiter=",", skiprows=1, usecols=1)[:num_dias]
        self.x_values = np.arange(len(self.temperaturas))
        print(f"Mostrando {len(self.temperaturas)} dias")
        
    def calcular_derivadas(self):
        self.derivadas = []
        n = len(self.temperaturas)
        for i in range(n):
            if i == 0:
                deriv = self.temperaturas[1] - self.temperaturas[0]
            elif i == n-1:
                deriv = self.temperaturas[-1] - self.temperaturas[-2]
            else:
                deriv = (self.temperaturas[i+1] - self.temperaturas[i-1])/2
            self.derivadas.append(deriv)
        print("\nDerivadas calculadas:", [float(round(d, 4)) for d in self.derivadas])
    
    def generar_polinomio(self):
        x = sp.symbols('x')
        polinomio = 0
        n = len(self.temperaturas)
        self.denominadores = []
        
        for i in range(n):
            xi = self.x_values[i]
            fi = self.temperaturas[i]
            fpi = self.derivadas[i]
            
            term_base = fi + fpi*(x - xi)
            productorio = 1
            
            for j in range(n):
                if j != i:
                    num = (x - self.x_values[j])**2
                    den = (xi - self.x_values[j])**2
                    term = num / den
                    term_base *= term
                    productorio *= den
            
            self.denominadores.append(productorio)
            polinomio += term_base / productorio
        
        self.H_poly = polinomio.expand().simplify()
        self.H_func = sp.lambdify(x, self.H_poly, "numpy")
        
        print("\nValores de temperatura:", self.temperaturas)
        print("Denominadores por punto:", [float(round(d, 4)) for d in self.denominadores])
        print("\nPolinomio simplificado:")
        print(self.H_poly)
    
    def plot_time(self):
        x_fine = np.linspace(self.x_values[0], self.x_values[-1], 200)
        H_values = self.H_func(x_fine)
        
        plt.figure(figsize=(12, 5))
        plt.scatter(self.x_values, self.temperaturas, label="Datos originales", color="blue")
        plt.plot(x_fine, H_values, "--", label="Interpolación Hermite", color="purple")
        plt.xlabel("Dia")
        plt.ylabel("Temperatura (°C)")
        plt.title("Interpolación de Hermite de Temperaturas Diarias")
        plt.legend()
        plt.grid(True)
        plt.show()

def main():
    interpol = InterpolacionHermite("open-meteo-10.25N68.only9.csv")
    
    num_dias = int(input('Numero de dias a mostrar: '))
    interpol.cargar_datos(num_dias)
    interpol.calcular_derivadas()
    interpol.generar_polinomio()
    interpol.plot_time()

if __name__ == "__main__":
    main()