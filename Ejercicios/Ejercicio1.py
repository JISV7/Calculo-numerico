import numpy as np
import matplotlib.pyplot as plt

class NumeroCondicion:
    def __init__(self, n):
        self.n = n
        self.tamanos = list(range(3, n+1))
        self.tamano_matriz = []
        self.condicion_matriz = []
    
    def generar_matriz_aleatoria(self, tamano):
        matriz = np.random.randint(-20, 20, size=(tamano, tamano))
        print("Matriz generada:\n", matriz)
        return matriz
    
    def obtener_condicion(self):
        tamano = self.n
        matriz = self.generar_matriz_aleatoria(tamano)
        matriz = np.array([[1, 3, 0], [4, 7, 2], [3, 4, 2]]) # det0
        det = np.linalg.det(matriz)
        if det != 0.0:
            nc = np.linalg.cond(matriz)
            self.tamano_matriz.append(tamano)
            self.condicion_matriz.append(nc)
            print(f"Número de condición: {nc}")
            return (tamano, nc)
        else:
            print(f"La matriz {matriz.shape[0]}x{matriz.shape[1]} es singular")
            return None

def main():
    nxn = int(input("Ingrese tamaño de la matriz (n): "))
    ejercicio1 = NumeroCondicion(nxn)
    resultado = ejercicio1.obtener_condicion()

    # Gráfico NumeroCondicion
    def plot_time():
        if resultado is not None:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            
            x = ejercicio1.tamano_matriz
            y = ejercicio1.condicion_matriz
            z = 0
            
            ax.scatter(x, y, z, c='b', marker='o', s=100)
            
            ax.set_xlabel('Tamaño de la matriz')
            ax.set_ylabel('Número de condición')
            ax.set_zlabel('Z')
            plt.title('Tamaño vs Condición')
            
            ax.view_init(elev=20, azim=30)
            
            plt.show()
        else:
            print("No se pudo graficar: matriz singular.")
    plot_time()

if __name__ == "__main__":
    main()