#  Aplicaciones de los determinantes con interfaz gráfica (Tkinter)
- Bibliotecas: import.tkinter, sub modulo tkinter (tkk)
- Interfaz Grafica:
- Geometrias en 2D y 3D para algunas aplicaciones. 
- Clase determinante: calcula el determinante de una matriz cuadrada utilizando la expansión por cofactores
- Clase Cramer: Resuelve sistemas de ecuaciones lineales Ax = b mediante la Regla de Cramer. Restringido a sistemas de dimensiones 2x2 hasta 5x5.
- Clase área de triangulo y colinealidad: recibe tres vertices como valores de entrada, se calcula el determinante (1/det) y se multiplica por la matriz.  
- Clase colinealidad: recibe como valores de entrada 3 puntos si el determinante es 0, los tres puntos son colineales. 
- Clase Ecuación de la recta por dos puntos distintos: recibe 2 puntos que seran multiplicados por la matriz para calcular la ecuacion de la recta de la forma 𝐴𝑥 + 𝐵𝑦 + 𝐶 = 0.
- Clase volumen de un tetraedro: el procedimiento para el volumen es con los vertices, el determinante y su respectiva matriz. 
- Clase ecuacion de un plano por tres puntos distintos: Se ingresa 3 puntos distintos para calcular su determinate y multiplicarla por la matriz, asi, obtendremos la ecuacion de la forma 𝐴𝑥 + 𝐵𝑦 + 𝐶𝑧 + 𝐷 = 0.




###Clase Determinante
----
```
class Determinante:
    def __init__(self, matriz: list):
        try:
            if not matriz or not isinstance(matriz, list):
                raise TypeError("La entrada debe ser una lista de listas.")

            self.dimension = len(matriz)


            for fila in matriz:
                if not isinstance(fila, (list, tuple)): # Comprueba el tipo
                    raise TypeError("Cada fila de la matriz debe ser una lista tupla.")
                if len(fila) != self.dimension:
                    raise ValueError("La matriz debe ser cuadrada (nxn).")
                .......

```
###Clase Colinealidad y área del triangulo
----
```
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

                .......
```
###Clase Colinealidad 
----
```
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

                .......
```
###Clase Coplanaridad y volumen del tetraedro 
----
```
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

                .......
```
###Clase Cramer 
----
```
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
                .......
```

###Clase Ecuacion de la recta
----
```
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

                .......
```
###Clase Ecuacion del plano
----
```
from determinante import  Determinante

class Plano(Determinante):
    def __init__(self, p1, p2, p3):
        try:
            # Validación de la longitud de los puntos
            if any(len(p) != 3 for p in (p1, p2, p3)):
                raise ValueError("Todos los puntos deben tener exactamente 3 coordenadas (x, y, z).")

            # Construcción de la matriz base con la primera fila como placeholder
            matriz_base = [
                [0, 0, 0, 0],
                [p1[0], p1[1], p1[2], 1],
                [p2[0], p2[1], p2[2], 1],
                [p3[0], p3[1], p3[2], 1]
            ]
            super().__init__(matriz_base)

                .......
```

Aplicaciones 
=============
Programa creado para calcular el determinante de matrices cuadradas o de diferentes tamaños, esto con el fin de aplicarlas a diferenes metodos aljebraicos que nos ayudara a obtener ecuaciones, áreas y volumenes, ademas, de poder visualizarlos de manera 2D y 3D según sea la preferencia del usuario, esto gracias a las opciones que ofrece la interfaz de usuario que da diferentes opciones al usuario para poder manipular, ingresar y visualizarlas en la pantalla. 
