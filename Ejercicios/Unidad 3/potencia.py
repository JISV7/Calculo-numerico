import numpy as np
import matplotlib.pyplot as plt
import condicion

class MetodoPotencia:
    def __init__(self, matriz, max_iter=300, tolerancia=1e-8):
        self.matriz = matriz
        self.max_iter = max_iter
        self.tolerancia = tolerancia
        self.n = matriz.shape[0]
        self.vector_actual = np.random.randint(-5, 6, size=self.n)
        print("Vector inicial utilizado (Potencia):\n", self.vector_actual)
        self.vector_actual = self.vector_actual / np.linalg.norm(self.vector_actual, ord=np.inf)
        self.autovalor_hist = []
        self.autovector_hist = []

    def calcular(self):
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
                    print(f"Convergencia alcanzada en {i + 1} iteraciones")
                    break
        return autovalor_aprox, self.vector_actual

    def graficar_convergencia(self):
        plt.figure(figsize=(12, 5))

        # Gráfico del autovalor
        plt.subplot(1, 2, 1)
        plt.plot(self.autovalor_hist, 'o-', markersize=4)
        plt.xlabel('N Iteración')
        plt.ylabel('Autovalor estimado')
        plt.title('Convergencia del Autovalor Dominante')
        plt.grid(True)

        plt.subplot(1, 2, 2)
        autovector_hist = np.array(self.autovector_hist)
        for i in range(autovector_hist.shape[1]):
            plt.plot(autovector_hist[:, i], 'o--', markersize=4, label=f'Componente {i + 1}')
        plt.xlabel("N Iteraciones")
        plt.ylabel('Componentes del Autovector')
        plt.title('Convergencia del Autovector')
        plt.legend()
        plt.grid(True)

        plt.tight_layout()
        plt.show()

def main():
    matriz = condicion.NumeroCondicion(2).generar_matriz_aleatoria()
    #matriz = np.array([[3,10,11.5,5],[10,3,14.5,13.5],[11.5,14.5,14,14.5],[5,13.5,14.5,13]])
    #matriz = np.array([[1, 5],[5, 18]])
    #matriz = np.array([[9, 8], [4, 9]])
    #matriz = np.array([[1,5],[1,3]])
    #matriz = np.array([[-1,0],[-1,3]])
    metodo_potencia = MetodoPotencia(matriz)

    autovalor, autovector = metodo_potencia.calcular()
    print("\nAutovalor dominante calculado:", autovalor)
    print("Autovector asociado:\n", autovector)

    # Graficar la convergencia
    metodo_potencia.graficar_convergencia()