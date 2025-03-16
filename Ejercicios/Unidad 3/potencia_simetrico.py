import numpy as np
import matplotlib.pyplot as plt
import condicion

class MetodoPotenciaSimetrico:
    def __init__(self, matriz, max_iter=300, tolerancia=1e-8):
        self.matriz = matriz
        self.max_iter = max_iter
        self.tolerancia = tolerancia
        self.n = matriz.shape[0]
        self.vector_actual = np.random.randint(-5, 6, size=self.n)
        print("Vector utilizado:\n", self.vector_actual)
        self.vector_actual = self.vector_actual / np.linalg.norm(self.vector_actual, ord=np.inf)
        self.autovalor_hist = []
        self.autovector_hist = []

    def calcular(self):
        if not np.all(np.abs(self.matriz - self.matriz.T) < 1e-8):
            self.matriz = (self.matriz + self.matriz.T) / 2
            print(f"\n La matriz no era simetrica, ahora es:\n{self.matriz}")

        for i in range(self.max_iter):
            nuevo_vector = self.matriz @ self.vector_actual
            autovalor_aprox = self.vector_actual @ nuevo_vector

            self.autovalor_hist.append(autovalor_aprox)
            if np.linalg.norm(nuevo_vector, ord=np.inf) == 0:
                return 0, self.vector_actual
            self.vector_actual = nuevo_vector / np.linalg.norm(nuevo_vector, ord=np.inf)
            self.autovector_hist.append(self.vector_actual.copy())
            
            if len(self.autovalor_hist) > 1:
                dif = abs(self.autovalor_hist[-1] - self.autovalor_hist[-2])
                if dif < self.tolerancia:
                    print(f"Convergencia alcanzada en {i+1} iteraciones")
                    break
        return autovalor_aprox, self.vector_actual

    def graficar_convergencia(self):
        plt.figure(figsize=(12, 5))
        
        # Gráfico del autovalor
        plt.subplot(1, 2, 1)
        plt.plot(self.autovalor_hist, 'o-', markersize=4)
        plt.title("Convergencia del Autovalor")
        plt.xlabel('N Iteración')
        plt.ylabel("Valor del Autovalor")
        plt.grid(True)
        
        # Gráfico de las diferencias del autovector
        diferencias = []
        for i in range(1, len(self.autovector_hist)):
            dif = np.linalg.norm(self.autovector_hist[i] - self.autovector_hist[i-1])
            diferencias.append(dif)
        
        plt.subplot(1, 2, 2)
        plt.plot(diferencias, 'ro--', markersize=4)
        plt.title("Cambios en el Autovector")
        plt.xlabel('N Iteración')
        plt.ylabel("Diferencia con anterior")
        plt.grid(True)
        
        plt.tight_layout()
        plt.show()

def main():
    matriz = condicion.NumeroCondicion(3).generar_matriz_aleatoria()

    #matriz = np.array([[1,5],[1,3]])
    potencia = MetodoPotenciaSimetrico(matriz)
    autovalor, autovector = potencia.calcular()

    print("\nAutovalor dominante calculado:", autovalor)
    print("Autovector asociado:", autovector)
    
    # Graficar la convergencia
    potencia.graficar_convergencia()