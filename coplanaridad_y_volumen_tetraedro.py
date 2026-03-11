from determinante import Determinante 

class Coplanaridad(Determinante):
    def __init__(self, p1, p2, p3, p4):
        try:
            if any(len(p) != 3 for p in (p1, p2, p3, p4)):
                raise ValueError("Todos los puntos deben tener exactamente 3 coordenadas (x, y, z).")

            matriz_base = [
                [p1[0], p1[1], p1[2], 1],
                [p2[0], p2[1], p2[2], 1],
                [p3[0], p3[1], p3[2], 1],
                [p4[0], p4[1], p4[2], 1]
            ]

            super().__init__(matriz_base)

        except TypeError:
            print("[Advertencia]: Los puntos proporcionados no son iterables o carecen del formato correcto.")
            raise
        except ValueError as e:
            print(f"[Advertencia]: {e}")
            raise

    def son_coplanarios(self):
        det = self.calcular()
        return abs(det) < 1e-9 # Consideramos el determinante como cero si es muy pequeño

   
    def volumen_tetraedro(self):
        try:
            det = self.calcular()
            volumen = abs(det) / 6
            return volumen
        except Exception as e:
            print(f"[Advertencia]: Error al calcular el volumen: {e}")
            return None


if __name__ == '__main__':
    punto1 = (1, 2, 3)
    punto2 = (4, 5, 1)
    punto3 = (7, 2, 9)
    punto4 = (10, 11, 12)

    obj_Coplanaridad = Coplanaridad(punto1, punto2, punto3, punto4)

    if obj_Coplanaridad.son_coplanarios():
        print("Los puntos son coplanares.")
    else:
        print("Los puntos no son coplanares.")

    # calculo del volumen
    volumen = obj_Coplanaridad.volumen_tetraedro()
    print(f"El volumen del tetraedro es: {volumen}")
