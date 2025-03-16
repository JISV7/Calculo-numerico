import numpy as np
import matplotlib.pyplot as plt

class NumeroCondicion:
    def __init__(self, n):
        self.n = n
        self.tamano_matriz = []
        self.condicion_matriz = []
        self.matriz = None
    
    def generar_matriz_aleatoria(self):
        tamano = self.n
        self.matriz = np.random.randint(1, 11, size=(tamano, tamano))
        print("Matriz generada:\n", self.matriz)
        return self.matriz
    
    def generar_matriz_aleatoria_simetrica(self):
        tamano = self.n
        self.matriz = np.random.randint(1, 11, size=(tamano, tamano))
        self.matriz = (self.matriz + self.matriz.T) / 2
        print("Matriz generada:\n", self.matriz)
        return self.matriz
    
    def obtener_condicion(self):
        tamano = self.n
        matriz = self.matriz
        det = np.linalg.det(matriz)
        if det != 0.0:
            matrizI = np.linalg.inv(matriz)
            nMatrizI = np.linalg.norm(matrizI, ord=np.inf)
            nMatriz = np.linalg.norm(matriz, ord=np.inf)
            nc = nMatriz * nMatrizI
            self.tamano_matriz.append(tamano)
            self.condicion_matriz.append(nc)
            return nc
        else:
            print(f"La matriz {matriz.shape[0]}x{matriz.shape[1]} es singular")
            return None
        
    def graficar(self):
        """
        Grafica el número de condición en función del tamaño de la matriz.
        """
        if len(self.tamano_matriz) > 0:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')

            x = self.tamano_matriz
            y = self.condicion_matriz
            z = np.zeros_like(x)

            ax.scatter(x, y, z, c='b', marker='o', s=100)

            ax.set_xlabel('Tamaño de la matriz')
            ax.set_ylabel('Número de condición')
            ax.set_zlabel('Z')
            plt.title('Tamaño vs Condición')

            ax.view_init(elev=20, azim=30)
            plt.show()
        else:
            print("No hay datos para graficar: todas las matrices son singulares.")
    

def main():
    nxn = 4
    cond = NumeroCondicion(nxn)
    cond.generar_matriz_aleatoria()
    resultado = cond.obtener_condicion()
    print(resultado)

    cond.graficar()