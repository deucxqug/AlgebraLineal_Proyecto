class Determinante:
    def __init__(self, matriz):
        if not matriz or not isinstance(matriz, list):
            raise ValueError("La entrada debe ser una lista de listas.")

        self.dimension = len(matriz)
        if not self._es_cuadrada(matriz):
            raise ValueError("La matriz debe ser cuadrada (nxn)")
        self.matriz = matriz

    def _es_cuadrada(self, matriz):
        n_filas = len(matriz)
        return  all(len(fila) == self.dimension for fila in matriz)

    def _obtener_menor(self, matriz, fila, columna):
        '''
        Genera la submatriz eliminando la fila y columna indicadas.
        :param matriz: matriz original
        :param fila: fila a ignorar
        :param columna: columna a ignorar
        :return: La submatriz eliminando la fila y columna
        '''
        return [
            [matriz[i][j] for j in range(len(matriz[i])) if j != columna]
            for i in range(len(matriz)) if i != fila
                ]

    def calcular(self, matriz_actual=None):
        '''
        Calcula el determinante de la matriz actual
        :param matriz_actual:
        :return: Un numero flotante que es el determinante
        '''
        if matriz_actual is None:
            matriz_actual = self.matriz

        n = len(matriz_actual)

        # Casos base
        if n == 1: # Matriz de 1x1
            return matriz_actual[0][0]
        if n == 2: # Matriz de 2x2
            return (matriz_actual[0][0] * matriz_actual[1][1] -
                    matriz_actual[0][1] * matriz_actual[1][0])

        det = 0
        # Calculo de la matriz por la primera fila
        for j in range(n):
            # Calculo recursivo del determinante
            signo = (-1) ** j # Calculo del signo
            # Calculo del cofactor
            cofactor = self.calcular(self._obtener_menor(matriz_actual, 0, j))
            det += signo * matriz_actual[0][j] * cofactor

        return det
