from condicion import NumeroCondicion
from potencia import MetodoPotencia
from potencia_inverso import MetodoPotenciaInverso

class AnalisisDeRiesgo:
    def __init__(self):
        self.numero_condicion = NumeroCondicion(5)
        self.matriz_firma = self.numero_condicion.generar_matriz_aleatoria_simetrica()
        self.potencia = MetodoPotencia(self.matriz_firma)
        self.potencia_inverso = MetodoPotenciaInverso(self.matriz_firma)
        
    def analizar_portafolio(self):
        # 1: Condicion
        condicion = self.numero_condicion.obtener_condicion()
        print(f"Numero condicion de la matriz de covarianza: {condicion}")

        if condicion > 1e4:
            print("""
            Comentario: Un número de condición alto.
            Sugiere que el portafolio puede ser muy inestable.
            Puede indicar una alta concentración de riesgo en pocos activos o una falta de diversificación.
            """)
        else:
            print("""
            Comentario: Un número de condición bajo.
            Esto indica que la matriz de covarianza está bien condicionada, lo que sugiere que el portafolio es estable.
            Sugiere que el riesgo está bien distribuido entre los activos.
            """)
            
        # 2: Potencia
        autovalor_dominante, autovector_dominante = self.potencia.calcular()
        print(f"Autovalor dominante: {autovalor_dominante}")
        print(f"Autovector dominante: {autovector_dominante}")

        print("""
        Comentario: El autovalor dominante representa la dirección de mayor volatilidad en el portafolio.
        El autovalor dominante indica que que activo es el principal riesgo del portafolio.
        El autovector asociado indica la combinación de activos que contribuyen al mayor riesgo del portafolio.
        """)

        # 3: Potencia Inverso
        autovalor_pequeno, autovector_pequeno = self.potencia_inverso.calcular_autovalor()
        print(f"Autovalor mas pequeno: {autovalor_pequeno}")
        print(f"Autovector asociado: {autovector_pequeno}")

        print("""
        Comentario: El autovalor más pequeño representa la dirección de menor volatilidad en el portafolio.
        El autovalor mas pequeño indica que activo presenta mas oportunidades para diversificar, por ser de muy bajo riesgo.
        El autovector asociado indica la combinación de activos que contribuyen menos al riesgo del portafolio.
        """)
        
        # 4: graficas
        self.potencia.graficar_convergencia()
        self.potencia_inverso.graficar_convergencia()

        print("""
        Comentario: Las gráficas de convergencia muestran cómo los métodos de potencia y potencia inverso se acercan a los autovalores dominante y más pequeño, respectivamente.
        Una convergencia rápida indica que los métodos son eficientes y que la matriz de covarianza es favorable.
        Una convergencia lenta puede sugerir que los autovalores están muy cercanos entre sí o que la matriz que describe el sistema es complicada.
        """)
        

AnalisisDeRiesgo().analizar_portafolio()