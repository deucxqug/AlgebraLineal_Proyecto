from determinante import  Determinante

class Cramer(Determinante):
    """
        Resuelve sistemas de ecuaciones lineales Ax = b mediante la Regla de Cramer.
        Restringido a sistemas de dimensiones 2x2 hasta 5x5.
    """
    def __init__(self, matriz_coeficientes: list, vector_terminos: list):
        super().__init__(matriz_coeficientes)
        self.A = matriz_coeficientes
        self.b = vector_terminos
        self.n = len(self.A)

# No agregue la comprobacion de la matriz cuadrada porque ya la tiene la clase determinante

        if len(self.b) != self.n:
            raise ValueError("Las dimensiones del vector de términos "
                             "independientes no coinciden con la matriz.")

        if not (2 <= self.n <= 5):
            raise ValueError(f"Dimensión no permitida (n={self.n}). El sistema debe ser de 2x2 a 5x5.")

    def resolver(self):
        '''
        :return: Regresa una lista con  las soluciones del sistema, ordendas como x1,x2,x3,...,xn
        '''
        try:
            det_A = Determinante(self.A).calcular()
            if det_A == 0.0:
                raise ValueError("[Advertencia] No hay solucion unica: "
                                 "El determinante de la matriz de coeficientes es 0.")
            else:
                soluciones = []
                for columnas in range(self.n): # columnas
                    Ai = [fila[:] for fila in self.A] # Copia de la matriz de coeficientes
                    for fila in range(self.n): # filas
                        Ai[fila][columnas] = self.b[fila] # Remplaza la columna x, y, z por b

                    det_Ai = Determinante(Ai).calcular()
                    soluciones.append(det_Ai / det_A)
            return soluciones
        except Exception as e:
            raise RuntimeError(f"{e}")

if __name__ == '__main__':
    matriz_A = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    vector_b = [6, 15, 11]

    try:
        sistema = Cramer(matriz_A, vector_b)
        resultado = sistema.resolver()
        print(f"Soluciones: {resultado}")
    except (ValueError, RuntimeError) as err:
        print(f"{err}")