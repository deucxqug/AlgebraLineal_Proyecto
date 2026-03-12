from determinante import Determinante

class Colinealidad(Determinante):
    def __init__(self, p1, p2, p3):
        try:
            if any(len(p) != 2 for p in (p1, p2, p3)):
                raise ValueError("Todos los puntos deben tener exactamente 2 coordenadas (x, y).")
            
            matriz_base = [
                [p1[0], p1[1], 1],
                [p2[0], p2[1], 1],
                [p3[0], p3[1], 1]
            ]

            super().__init__(matriz_base) # Inicializa la matriz en la clase base Determinante

        except TypeError:
            print("[Advertencia]: Los puntos proporcionados no son iterables o carecen del formato correcto.")
            raise
        except ValueError as e:
            print(f"[Advertencia]: {e}")
            raise

    def son_colineales(self):
        det = self.calcular()
        return det == 0 
    

 
    def area_triangulo(self):
        det = self.calcular()
        area = abs(det) / 2
        return area
    

if __name__ == '__main__':
    punto1 = (1, 2)
    punto2 = (3, 4)
    punto3 = (5, 6)

    obj_colinealidad = Colinealidad(punto1, punto2, punto3)

    if obj_colinealidad.son_colineales():
        print("Los puntos son colineales.")
    else:
        print("Los puntos no son colineales.")

 
    area = obj_colinealidad.area_triangulo()
    print(f"Área del triángulo formado por los puntos: {area}")
