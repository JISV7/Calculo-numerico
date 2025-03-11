import numpy as np
import matplotlib.pyplot as plt

class MetodoPotenciaInverso:
    def __init__(self, matriz, max_iter=300, tolerancia=1e-8):
        self.matriz = matriz
        self.max_iter = max_iter
        self.tolerancia = tolerancia
        self.n = matriz.shape[0]
        self.vector_actual = np.random.randint(-5, 6, size=self.n)
        print("Vector utilizado:\n", self.vector_actual)
        self.vector_actual = self.vector_actual / np.linalg.norm(self.vector_actual, ord=np.inf)
        self.autovalores_hist = []
        
    def calcular_autovalor(self):
        for i in range(self.max_iter):
            try:
                nuevo_vector = np.linalg.solve(self.matriz, self.vector_actual)
            except np.linalg.LinAlgError:
                print("Error al resolver el sistema lineal")
                return None, None
            
            u = np.dot(self.vector_actual, nuevo_vector)
            u_normalizado = u / (self.vector_actual @ self.vector_actual)
            
            if abs(u_normalizado) < 1e-10:
                print("División por cero")
                return None, None
                
            autovalor_aprox = 1 / u_normalizado
            self.autovalores_hist.append(autovalor_aprox)
            
            norma_nuevo = np.linalg.norm(nuevo_vector, ord=np.inf)
            if norma_nuevo == 0:
                print("Vector nulo")
                return None, None
                
            self.vector_actual = nuevo_vector / norma_nuevo
            
            if len(self.autovalores_hist) > 1:
                diferencia = abs(self.autovalores_hist[-1] - self.autovalores_hist[-2])
                if diferencia < self.tolerancia:
                    print(f"Convergencia alcanzada en {i+1} iteraciones")
                    break
        return autovalor_aprox, self.vector_actual

def main():
    n = int(input("Ingrese tamaño de la matriz (n): "))
    matriz_valida = False
    while not matriz_valida:
        matriz = np.random.randint(-20, 20, size=(n, n))
        if np.linalg.det(matriz) != 0:
            matriz_valida = True
    #matriz = np.array([[2, 0], [0, 0]]) #det0
    #matriz = np.array([[5,0,0], [1,1,0],[1,1,2]]) #EjemploYTInverso1
    #matriz = np.array([[2,1], [1,5]]) #EjemploYTInverso2
    print(matriz)
    print("\nDeterminante = ", np.linalg.det(matriz))
    
    metodo = MetodoPotenciaInverso(matriz)
    autovalor, autovector = metodo.calcular_autovalor()
    
    # Gráfico MetodoPotenciaInverso
    def plot_time():
        plt.figure(figsize=(12, 5))

        # Gráfico autovalor
        # Gráfico de convergencia
        plt.plot(metodo.autovalores_hist, 'o--', markersize=4)
        plt.xlabel('N Iteración')
        plt.ylabel("Valor del Autovalor")
        plt.title("Convergencia del Menor Autovalor")
        plt.grid()
        plt.show()

    if autovalor is not None:
        print("\nAutovalor más pequeño estimado:", autovalor)
        print("Autovector correspondiente:", autovector)
        plot_time()
        
    else:
        print("No se pudo calcular el autovalor")

if __name__ == "__main__":
    main()