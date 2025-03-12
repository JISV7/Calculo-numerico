import numpy as np
import matplotlib.pyplot as plt

class MetodoPotencia:
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
    matriz = np.random.randint(-20, 21, size=(n, n))
    #matriz = np.array([[1, 3, 0], [4, 7, 2], [3, 4, 2]]) # det0
    #matriz = np.array([[2, 0], [0, 0]]) #det0
    #matriz = np.array([[1, 0], [1, 3]]) #EjemploYT
    #matriz = np.array([[5,0,0], [1,1,0],[1,1,2]]) #EjemploYTInverso

    matriz = [[11,1,-15,15],[-6,0,-5,9],[8,-17,10,-12],[-17,16,-4,4]]
    matriz = np.array([[11.0,-2.5,-3.5,-1.0],[-2.5,0.0,-11.0,12.5],[-3.5,-11.0,10.0,-8.0],[-1.0,12.5,-8.0,4.0]])
    print("Matriz utilizada:\n", matriz)
    
    potencia = MetodoPotencia(matriz)
    autovalor, autovector = potencia.calcular()

    # Verificación autovector
    lambda_aprox, v = autovalor, autovector
    residual = matriz @ v - lambda_aprox * v
    print('Mv-kv = 0:', True if np.linalg.norm(residual) < 1e-6 else False)
    
    print("\nAutovalor dominante estimado:", autovalor)
    print("Autovector normalizado:", autovector)
    
    # Gráfico MetodoPotencia
    def plot_time(potencia):
        plt.figure(figsize=(12, 5))
        
        # Gráfico del autovalor
        # Convergencia del autovalor
        plt.subplot(1, 2, 1)
        plt.plot(potencia.autovalor_hist, 'o-', markersize=4)
        plt.xlabel('N Iteración')
        plt.ylabel('Autovalor estimado')
        plt.title('Convergencia del Autovalor Dominante')
        plt.grid(True)
        
        # Gráfico del autovector
        # Convergencia de las componentes del autovector
        plt.subplot(1, 2, 2)
        autovector_hist = np.array(potencia.autovector_hist)
        for i in range(autovector_hist.shape[1]):
            plt.plot(autovector_hist[:, i], 'o--', markersize=4, label=f'Componente {i+1}')
        plt.xlabel("N Iteraciones")
        plt.ylabel('Componentes del Autovector')
        plt.title('Convergencia del Autovector')
        plt.legend()
        plt.grid(True)
        
        plt.tight_layout()
        plt.show()
    plot_time(potencia)

if __name__ == "__main__":
    main()