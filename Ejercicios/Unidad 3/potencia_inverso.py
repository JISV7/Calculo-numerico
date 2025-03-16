import numpy as np
import matplotlib.pyplot as plt
import condicion

class MetodoPotenciaInverso:
    def __init__(self, matriz, max_iter=300, tolerancia=1e-8):
        self.matriz = matriz
        self.max_iter = max_iter
        self.tolerancia = tolerancia
        self.n = matriz.shape[0]
        self.vector_actual = np.random.randint(-5, 6, size=self.n)
        print("Vector inicial utilizado (PotenciaInversa):\n", self.vector_actual)
        self.vector_actual = self.vector_actual / np.linalg.norm(self.vector_actual, ord=np.inf)
        self.autovalores_hist = []

    def calcular_autovalor(self):
        for i in range(self.max_iter):
            try:
                nuevo_vector = np.linalg.solve(self.matriz, self.vector_actual)
            except np.linalg.LinAlgError:
                print("La matriz es singular o no se puede resolver el sistema lineal.")
                return None, None
            
            u = self.vector_actual @ nuevo_vector
            u_normalizado = u / (self.vector_actual @ self.vector_actual)

            if abs(u_normalizado) < 1e-10:
                print("División por cero en el cálculo del autovalor.")
                return None, None

            autovalor_aprox = 1 / u_normalizado
            self.autovalores_hist.append(autovalor_aprox)

            norma_nuevo = np.linalg.norm(nuevo_vector, ord=np.inf)
            if norma_nuevo == 0:
                print("Vector nulo después de la normalización.")
                return None, None

            self.vector_actual = nuevo_vector / norma_nuevo
            
            if len(self.autovalores_hist) > 1:
                diferencia = abs(self.autovalores_hist[-1] - self.autovalores_hist[-2])
                if diferencia < self.tolerancia:
                    print(f"Convergencia alcanzada en {i + 1} iteraciones")
                    break
        return autovalor_aprox, self.vector_actual

    def graficar_convergencia(self):
        plt.figure(figsize=(12, 5))
        plt.plot(self.autovalores_hist, 'o--', markersize=4, label="Autovalor estimado")
        plt.xlabel('N Iteración')
        plt.ylabel("Valor del Autovalor")
        plt.title("Convergencia del Menor Autovalor")
        plt.grid()
        plt.legend()
        plt.show()
        
def main():
    matriz =  condicion.NumeroCondicion(2).generar_matriz_aleatoria()
    #matriz = matriz = np.array([[9, 8], [4, 9]])
    metodo = MetodoPotenciaInverso(matriz)

    autovalor, autovector = metodo.calcular_autovalor()

    print(f"Autovalor aproximado: {autovalor}")
    print(f"Autovector asociado:\n{autovector}")

    metodo.graficar_convergencia()