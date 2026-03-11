from determinante import Determinante

class Recta(Determinante):
    def __init__(self, p1, p2):
        try:
            # Validación de la longitud de los puntos
            if any(len(p) != 2 for p in (p1, p2)):
                raise ValueError("Todos los puntos deben tener exactamente 2 coordenadas (x, y).")

            # Construcción de la matriz base con la primera fila como placeholder
            matriz_base = [
                [0, 0, 0],
                [p1[0], p1[1], 1],
                [p2[0], p2[1], 1]
            ]
            super().__init__(matriz_base)

        except TypeError:
            print("[Advertencia]: Los puntos proporcionados no son iterables o carecen del formato correcto.")
            raise
        except ValueError as e:
            print(f"[Advertencia]: {e}")
            raise
        except Exception as e:
            print(f"[Advertencia]: Error inesperado durante la inicialización del recta: {e}")
            raise

    def obtener_coeficientes(self):
        try:
            coeficientes = []
            for j in range(3):
                menor = self._obtener_menor(self.matriz, 0, j)
                signo = (-1) ** j
                det_menor = self.calcular(menor)
                coeficientes.append(signo * det_menor)

            return tuple(coeficientes)

        except Exception as e:
            print(f"[Advertencia]: Fallo al calcular los coeficientes mediante cofactores: {e}")
            return None

    def __str__(self):
        try:
            coeficientes = self.obtener_coeficientes()

            if coeficientes is None:
                return "[Error]: No se puede generar la ecuación debido a un fallo en los coeficientes."

            variables = ['x', 'y', '']
            terminos = []

            for coef, var in zip(coeficientes, variables):
                if abs(coef) < 1e-9: # Consideramos coeficientes muy pequeños como cero para evitar términos insignificantes
                    continue

                if isinstance(coef, float):
                    coef = int(coef) # Si el coeficiente es un número entero, lo convertimos a int para evitar decimales innecesarios
                else:
                    coef = round(coef, 6) # Redondeo para 6 digitos después del punto decimal

                # Construccion de la cadena (Ecuacion de la recta)
                if coef == 1 and var != '':
                    str_coef = ""
                elif coef == -1 and var != '':
                    str_coef = "-"
                else:
                    str_coef = str(coef)

                terminos.append(f"{str_coef}{var}")

            if not terminos:
                return "0 = 0"

            ecuacion = terminos[0]
            for termino in terminos[1:]:
                if termino.startswith('-'):
                    ecuacion += f" - {termino[1:]}"
                else:
                    ecuacion += f" + {termino}"

            return f"{ecuacion} = 0"

        except Exception as e:
            print(f"[Advertencia]: Excepción capturada al dar formato a la cadena de la ecuación: {e}")
            return "Error de formato en la representación del plano."

if __name__ == '__main__':
    punto1 = (2, 1)
    punto2 = (3, -2)
    obj_Recta = Recta(punto1, punto2)

    print(obj_Recta)