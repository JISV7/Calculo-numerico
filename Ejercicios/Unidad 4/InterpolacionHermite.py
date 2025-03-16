import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

class InterpolacionHermite:
    def __init__(self, file_path):
        self.file_path = file_path
        self.temperaturas = None
        self.x_values = None
        self.n = None
        self.coeficientes = []
        self.H_poly = None
        self.H_func = None

    def cargar_datos(self, num_dias):
        self.temperaturas = np.loadtxt(self.file_path, delimiter=",", skiprows=1, usecols=1)[:num_dias]
        self.x_values = np.arange(len(self.temperaturas))
        print(f"Mostrando {len(self.temperaturas)} dias")

    def calcular_derivadas(self):
        return np.gradient(self.temperaturas)

    def generar_polinomio(self):
        derivadas = self.calcular_derivadas()
        self.n = len(self.temperaturas)
        m = 2 * self.n
        z = [0] * m
        Q = [[0 for _ in range(m)] for _ in range(m)]
        for i in range(self.n):
            z[2 * i] = self.x_values[i]
            z[2 * i + 1] = self.x_values[i]
            Q[2 * i][0] = self.temperaturas[i]
            Q[2 * i + 1][0] = self.temperaturas[i]
            Q[2 * i + 1][1] = derivadas[i]
            if i != 0:
                Q[2 * i][1] = (Q[2 * i][0] - Q[2 * i - 1][0]) / (z[2 * i] - z[2 * i - 1])
        for j in range(2, m):
            for i in range(j, m):
                Q[i][j] = (Q[i][j - 1] - Q[i - 1][j - 1]) / (z[i] - z[i - j])
        x = sp.symbols('x')
        poly = Q[0][0]
        term = 1
        for i in range(1, m):
            term *= (x - z[i - 1])
            poly += Q[i][i] * term
        self.H_poly = sp.simplify(poly)
        self.H_func = sp.lambdify(x, self.H_poly, 'numpy')
        print(f"Temperaturas: {self.temperaturas}")
        #print(f"Derivadas obtenidas: {list(derivadas)}")
        print("\nPolinomio de Hermite generado:")
        print(self.H_poly)

    def plot_time(self):
        x_fine = np.linspace(self.x_values[0], self.x_values[-1], 200)
        H_values = self.H_func(x_fine)
        plt.figure(figsize=(12, 5))
        plt.scatter(self.x_values, self.temperaturas, label="Datos originales", color="blue")
        plt.plot(x_fine, H_values, "--", label="Hermite", color="red")
        plt.xlabel("Día")
        plt.ylabel("Temperatura (°C)")
        plt.title("Interpolación de Hermite")
        plt.legend()
        plt.grid(True)
        plt.xlim(self.x_values[0] - 1, self.x_values[-1] + 1)
        plt.ylim(min(self.temperaturas) - 1, max(self.temperaturas) + 1)
        plt.show()

def main():
    interpol = InterpolacionHermite("open-meteo-10.25N68.only9.csv")
    num_dias = 7
    interpol.cargar_datos(num_dias)
    interpol.generar_polinomio()
    interpol.plot_time()

if __name__ == "__main__":
    main()
