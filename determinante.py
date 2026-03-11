class Determinante:
    def __init__(self, matriz: list):
        try:
            if not matriz or not isinstance(matriz, list):
                raise TypeError("La entrada debe ser una lista de listas.")

            self.dimension = len(matriz)


            for fila in matriz:
                if not isinstance(fila, list or tuple):
                    raise TypeError("Cada fila de la matriz debe ser una lista o tupla.")
                if len(fila) != self.dimension:
                    raise ValueError("La matriz debe ser cuadrada (nxn).")
                for valor in fila:
                    if not isinstance(valor, (int, float)):
                        raise TypeError(f"El elemento '{valor}' es inválido. La matriz solo admite int o float.")

            self.matriz = matriz

        except (TypeError, ValueError) as e:
            print(f"[Advertencia]: En constructor Determinante: {e}")
            raise
        except Exception as e:
            print(f"[Advertencia]: Error inesperado en la inicialización: {e}")
            raise

    def _es_cuadrada(self, matriz: list) -> bool:
        try:
            n_filas = len(matriz)
            return all(len(fila) == self.dimension for fila in matriz)
        except Exception as e:
            print(f"[Advertencia]: Al verificar dimensión cuadrada: {e}")
            raise

    def _obtener_menor(self, matriz: list, fila: int, columna: int) -> list:
        '''
        Genera la submatriz eliminando la fila y columna indicadas.
        '''
        try:
            return [
                [matriz[i][j] for j in range(len(matriz[i])) if j != columna]
                for i in range(len(matriz)) if i != fila
            ]
        except Exception as e:
            print(f"[Advertencia]: Al generar la submatriz (menor): {e}")
            raise

    def calcular(self, matriz_actual: list = None) -> float:
        '''
        Calcula el determinante de la matriz actual
        '''
        try:
            if matriz_actual is None:
                matriz_actual = self.matriz

            n = len(matriz_actual)

            # Casos base
            if n == 1:
                return float(matriz_actual[0][0])
            if n == 2:
                return float(matriz_actual[0][0] * matriz_actual[1][1] -
                             matriz_actual[0][1] * matriz_actual[1][0])

            det = 0.0
            # Cálculo de la matriz por la primera fila
            for j in range(n):
                signo = (-1) ** j
                cofactor = self.calcular(self._obtener_menor(matriz_actual, 0, j))
                det += signo * matriz_actual[0][j] * cofactor

            return float(det)

        except TypeError as e:
            print(f"[Advertencia]: Tipos no validos durante el cálculo: {e}")
            raise
        except Exception as e:
            print(f"[Advertencia]: Error inesperado durante el cálculo del determinante: {e}")
            raise


# Ejemplo de ejecución
if __name__ == "__main__":
    datos = [
        [1, 1, 1],
        [4, 5, 1],
        [7, 8, 1],
    ]

    try:
        obj_matriz = Determinante(datos)
        print(f"El determinante de la matriz es: {obj_matriz.calcular()}")
    except Exception as e:
        print(f"Ejecución detenida por error de validación: {e}")
