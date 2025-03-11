import numpy as np
import matplotlib.pyplot as plt

class MetodoPotenciaSimetrico:
    def __init__(self, matriz, max_iter=300, tolerancia=1e-8):
        self.matriz = matriz
        self.max_iter = max_iter
        self.tolerancia = tolerancia
        self.n = matriz.shape[0]
        self.vector_actual = np.random.randint(-5, 6, size=self.n)
        print("Vector utilizado:\n", self.vector_actual)
        self.vector_actual = self.vector_actual / np.linalg.norm(self.vector_actual)
        self.autovalor_hist = []
        self.autovector_hist = []
        
    def calcular(self):
        for i in range(self.max_iter):
            nuevo_vector = self.matriz @ self.vector_actual
            autovalor_aprox = self.vector_actual @ nuevo_vector

            self.autovalor_hist.append(autovalor_aprox)
            if np.linalg.norm(nuevo_vector) == 0:
                return 0, self.vector_actual
            self.vector_actual = nuevo_vector / np.linalg.norm(nuevo_vector)
            self.autovector_hist.append(self.vector_actual.copy())
            
            if len(self.autovalor_hist) > 1:
                dif = abs(self.autovalor_hist[-1] - self.autovalor_hist[-2])
                if dif < self.tolerancia:
                    print(f"Convergencia alcanzada en {i+1} iteraciones")
                    break
        return autovalor_aprox, self.vector_actual

def main():
    n = int(input("Ingrese tamaño de la matriz (n): "))
    matriz = np.random.randint(-20, 20, size=(n, n))
    #matriz = np.array([[1, 3, 0], [4, 7, 2], [3, 4, 2]]) # det0
    print("Matriz utilizada:\n", matriz)
    A = (matriz + matriz.T)/2
    print("Matriz simetrica:\n", A)
    
    potencia = MetodoPotenciaSimetrico(A)
    autovalor, autovector = potencia.calcular()

    print("\nAutovalor dominante calculado:", autovalor)
    print("Autovector asociado:", autovector)
    
    # Gráfico MetodoPotencia
    def plot_time():
        plt.figure(figsize=(12,5))
        
        # Gráfico autovalor
        # Convergencia del autovalor
        plt.subplot(1,2,1)
        plt.plot(potencia.autovalor_hist, 'o-', markersize=4)
        plt.title("Convergencia del Autovalor")
        plt.xlabel('N Iteración')
        plt.ylabel("Valor del Autovalor")
        plt.grid(True)
        
        # Gráfico del autovector
        # Convergencia de las componentes del autovector
        diferencias = []
        for i in range(1, len(potencia.autovector_hist)):
            dif = np.linalg.norm(potencia.autovector_hist[i] - potencia.autovector_hist[i-1])
            diferencias.append(dif)
        
        plt.subplot(1,2,2)
        plt.plot(diferencias, 'ro--', markersize=4)
        plt.title("Cambios en el Autovector")
        plt.xlabel('N Iteración')
        plt.ylabel("Diferencia con anterior")
        plt.grid(True)
        
        plt.tight_layout()
        plt.show()
    plot_time()

if __name__ == "__main__":
    main()