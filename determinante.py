# Clase para calcular el determinante de una matriz cuadrada utilizando la expansión por cofactores
class Determinante:
    def __init__(self, matriz: list):
        try:
            if not matriz or not isinstance(matriz, list):
                raise TypeError("La entrada debe ser una lista de listas.")

            self.dimension = len(matriz)


            for fila in matriz:
                if not isinstance(fila, (list, tuple)): # Comprueba el tipo
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

    @staticmethod
    def _eliminar_columna(fila: list, columna: int) -> list:
        '''
        Elimina la columna de un renglon/fila

        :param fila: La fila que modificamos
        :param columna: La columna que elimina
        :return: Returna una lista con un elemento menos
        '''
        return [celda for j, celda in enumerate(fila) if j != columna]

    def _obtener_menor(self, matriz: list, indice_fila: int, indice_columna: int) -> list:
        '''
        Construye la submatriz resultante de eliminar la i-ésima fila y la j-ésima columna.

        :param matriz: Representa la matriz original de la que queremos encontrar sus menores
        :param indice_fila: Índice de la fila que se debe excluir del resultado.
        :param indice_columna: Índice de la columna que se debe excluir del resultado.
        :return: Submatriz de dimensiones (n-1) x (n-1).
        '''
        return [
            self._eliminar_columna(fila_actual, indice_columna)
            for i, fila_actual in enumerate(matriz)
            if i != indice_fila
        ]

    def calcular(self, matriz_actual: list = None) -> float:
        '''
        Calculo del determinante utilizando la expansión por cofactores
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

        # Control de errores por precisión numérica: Si el determinante es muy pequeño, se considera como cero
            tolerancia = 1e-9
            if abs(det) < tolerancia:
                det = 0.0

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
