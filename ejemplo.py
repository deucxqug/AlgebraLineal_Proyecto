import tkinter as tk
import math
from ecuacion_del_plano import  Plano


class Graficador3DTkinter:
    def __init__(self, p1_init, p2_init, p3_init):
        self.root = tk.Tk()
        self.root.title("Visualizador Dinámico de Plano 3D")

        self.width = 600
        self.height = 600
        self.angle = math.pi / 6

        self.frame_canvas = tk.Frame(self.root)
        self.frame_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.frame_controles = tk.Frame(self.root, padx=10, pady=10)
        self.frame_controles.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas = tk.Canvas(self.frame_canvas, width=self.width, height=self.height, bg="white")
        self.canvas.pack()

        self.lbl_eq = tk.Label(self.frame_canvas, text="Ecuación: ", font=("Consolas", 14))
        self.lbl_eq.pack(pady=10)

        self.vars_p1 = [tk.DoubleVar(value=v) for v in p1_init]
        self.vars_p2 = [tk.DoubleVar(value=v) for v in p2_init]
        self.vars_p3 = [tk.DoubleVar(value=v) for v in p3_init]

        # Declaración de la variable reactiva para la escala (E)
        self.var_escala = tk.IntVar(value=30)

        self._construir_panel_controles()
        self._actualizar_grafico()

    def _construir_panel_controles(self):
        # Implementación del panel de escala global
        marco_vista = tk.LabelFrame(self.frame_controles, text="Control de Vista")
        marco_vista.pack(fill=tk.X, pady=5)
        tk.Label(marco_vista, text="Escala:").pack(side=tk.LEFT)
        slider_escala = tk.Scale(marco_vista, from_=5, to=100, resolution=1,
                                 orient=tk.HORIZONTAL, variable=self.var_escala,
                                 command=self._actualizar_grafico)
        slider_escala.pack(side=tk.LEFT, fill=tk.X, expand=True)

        def crear_grupo(titulo, vars_punto):
            marco_grupo = tk.LabelFrame(self.frame_controles, text=titulo)
            marco_grupo.pack(fill=tk.X, pady=5)

            for i, eje in enumerate(['X', 'Y', 'Z']):
                marco_fila = tk.Frame(marco_grupo)
                marco_fila.pack(fill=tk.X, pady=2)
                tk.Label(marco_fila, text=f"{eje}:", width=3).pack(side=tk.LEFT)
                slider = tk.Scale(marco_fila, from_=-15, to=15, resolution=1,
                                  orient=tk.HORIZONTAL, variable=vars_punto[i],
                                  command=self._actualizar_grafico)
                slider.pack(side=tk.LEFT, fill=tk.X, expand=True)

        crear_grupo("Punto 1", self.vars_p1)
        crear_grupo("Punto 2", self.vars_p2)
        crear_grupo("Punto 3", self.vars_p3)

    def _proyectar(self, x, y, z):
        cx = self.width / 2
        cy = self.height / 2
        # Extracción del valor de escala en tiempo real
        escala = self.var_escala.get()

        x_2d = cx + (x - y) * escala * math.cos(self.angle)
        y_2d = cy - z * escala + (x + y) * escala * math.sin(self.angle)
        return x_2d, y_2d

    def _dibujar_ejes(self):
        px1, py1 = self._proyectar(-15, 0, 0)
        px2, py2 = self._proyectar(15, 0, 0)
        self.canvas.create_line(px1, py1, px2, py2, fill="red", dash=(4, 4))
        self.canvas.create_text(px2, py2, text="X", fill="red")

        px1, py1 = self._proyectar(0, -15, 0)
        px2, py2 = self._proyectar(0, 15, 0)
        self.canvas.create_line(px1, py1, px2, py2, fill="green", dash=(4, 4))
        self.canvas.create_text(px2, py2, text="Y", fill="green")

        px1, py1 = self._proyectar(0, 0, -15)
        px2, py2 = self._proyectar(0, 0, 15)
        self.canvas.create_line(px1, py1, px2, py2, fill="blue", dash=(4, 4))
        self.canvas.create_text(px2, py2, text="Z", fill="blue")

    def _dibujar_plano(self, plano):
        coefs = plano.obtener_coeficientes()
        if not coefs or all(c == 0 for c in coefs):
            self.canvas.create_text(self.width / 2, 20, text="Puntos colineales. El plano es indefinido.", fill="red")
            return

        A, B, C, D = coefs
        lim = 10

        if C != 0:
            base = [(lim, lim), (lim, -lim), (-lim, -lim), (-lim, lim)]
            esquinas_3d = [(x, y, -(A * x + B * y + D) / C) for x, y in base]
        elif B != 0:
            base = [(lim, lim), (lim, -lim), (-lim, -lim), (-lim, lim)]
            esquinas_3d = [(x, -(A * x + C * z + D) / B, z) for x, z in base]
        elif A != 0:
            base = [(lim, lim), (lim, -lim), (-lim, -lim), (-lim, lim)]
            esquinas_3d = [(-(B * y + C * z + D) / A, y, z) for y, z in base]
        else:
            return

        poligono_2d = [self._proyectar(x, y, z) for x, y, z in esquinas_3d]
        coords = [coord for punto in poligono_2d for coord in punto]

        # Corrección: Eliminación de stipple="gray50"
        self.canvas.create_polygon(*coords, fill="cyan", outline="black")

        puntos_actuales = [
            [v.get() for v in self.vars_p1],
            [v.get() for v in self.vars_p2],
            [v.get() for v in self.vars_p3]
        ]
        for idx, (px, py, pz) in enumerate(puntos_actuales):
            cx, cy = self._proyectar(px, py, pz)
            self.canvas.create_oval(cx - 4, cy - 4, cx + 4, cy + 4, fill="red")
            self.canvas.create_text(cx + 10, cy - 10, text=f"P{idx + 1}")

    def _actualizar_grafico(self, *args):
        self.canvas.delete("all")
        self._dibujar_ejes()

        p1 = [v.get() for v in self.vars_p1]
        p2 = [v.get() for v in self.vars_p2]
        p3 = [v.get() for v in self.vars_p3]

        try:
            plano_instancia = Plano(p1, p2, p3)
            self.lbl_eq.config(text=f"Ecuación: {str(plano_instancia)}")
            self._dibujar_plano(plano_instancia)
        except Exception as e:
            # Corrección: Exposición estricta del error en la salida estándar
            print(f"Excepción capturada en tiempo de ejecución gráfica: {e}")
            self.lbl_eq.config(text="Ecuación: Indefinida")

    def ejecutar(self):
        self.root.mainloop()


# Ejecución de la Interfaz
if __name__ == "__main__":
    # Puntos de inicialización requeridos
    p1_inicial = [1, 2, -2]
    p2_inicial = [3, -2, 1]
    p3_inicial = [5, 1, -4]

    app = Graficador3DTkinter(p1_inicial, p2_inicial, p3_inicial)
    app.ejecutar()
