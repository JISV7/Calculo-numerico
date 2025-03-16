from condicion import NumeroCondicion
from potencia import MetodoPotencia
from potencia_inverso import MetodoPotenciaInverso

class AnalisisPuente:
    def __init__(self):
        self.numero_condicion = NumeroCondicion(5)
        self.matriz_rigidez = self.numero_condicion.generar_matriz_aleatoria_simetrica()
        self.potencia = MetodoPotencia(self.matriz_rigidez)
        self.potencia_inverso = MetodoPotenciaInverso(self.matriz_rigidez)

    def analizar_puente(self):

        # 1: COndicion
        condicion = self.numero_condicion.obtener_condicion()
        print(f"\nNumero de condicion de la matriz de rigidez: {condicion}")

        if condicion > 1e4:
            print("""
            Comentario: Un número de condición alto.
            Indica que la matriz de rigidez está mal condicionada, lo que sugiere un puente inestable.
            Pequeñas variaciones en las fuerzas aplicadas podrían causar grandes deformaciones.
            """)
        else:
            print("""
            Comentario: Un número de condición bajo.
            Indica que la matriz de rigidez está bien condicionada, lo que sugiere que el puente es estable.
            El sistema es menos sensible a errores y es probable que sea confiable.
            """)

        # 2: Metodo de Potencia
        autovalor_dominante, autovector_dominante = self.potencia.calcular()
        print(f"Autovalor dominante (maxima rigidez): {autovalor_dominante}")
        print(f"Autovector asociado (direccion de maxima rigidez): {autovector_dominante}")

        print("""
        Comentario: El autovalor dominante representa la máxima rigidez de la estructura.
        Un autovalor alto indica el punto en que el puente es más rígido.
        El autovector asociado indica el conjunto de puntos en la dirección con mayor resistencia.
        Importante para entender cómo se distribuyen las cargas en la estructura.
        """)


        # 3: Metodo de Potencia Inverso
        autovalor_pequeno, autovector_pequeno = self.potencia_inverso.calcular_autovalor()
        print(f"Autovalor mas pequeño (minima rigidez): {autovalor_pequeno}")
        print(f"Autovector asociado (dirección de minima rigidez): {autovector_pequeno}")

        print("""
        Comentario: El autovalor más pequeño representa la mínima rigidez de la estructura.
        Un autovalor minimo indica el punto en que el puente es más débil, sugiriendo que se necesitan refuerzos.
        El autovector asociado indica la dirección en la que el puente es más vulnerable.
        Esta dirección es crítica porque muestra dónde el puente es más propenso a fallar.
        """)

        # 4: Graficas  
        self.potencia.graficar_convergencia()
        self.potencia_inverso.graficar_convergencia()

        print("""
        Comentario: Las gráficas de convergencia muestran cómo los métodos de potencia y potencia inverso se acercan a los autovalores dominante y más pequeño, respectivamente.
        Una convergencia rápida indica que los métodos son eficientes y que la matriz de rigidez es favorable.
        Una convergencia lenta puede sugerir que los autovalores están muy cercanos entre sí o que la matriz que describe el sistema es complicada.
        """)


AnalisisPuente().analizar_puente()