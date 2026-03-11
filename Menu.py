import tkinter as tk
from tkinter import messagebox

class MenuPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicaciones de los Determinantes")
        self.root.geometry("400x550")
        
        # Titulos 
        tk.Label(self.root, text="Menú Principal", font=("Arial", 16, "bold"), pady=20).pack()
        tk.Label(self.root, text="Seleccione una aplicación:", font=("Arial", 10)).pack()
       #Lista de botones con sus funciones 
        self.opciones = [
            ("Colinealidad y Área", "colinealidad_y_area_triangulo"),
            ("Colinealidad", "colinealidad"),
            ("Coplanaridad y Volumen", "coplanaridad_y_volumen_tetraedro"),
            ("Regla de Cramer", "cramer"),
            ("Determinante", "determinante"),
            ("Ecuación del Plano", "ecuacion_del_plano"),
            ("Ecuación de la Recta", "ecuacion_de_la_recta")
        ]

        for nombre_visible, nombre_archivo in self.opciones:
            btn = tk.Button(
                self.root, 
                text=nombre_visible, 
                command=lambda n=nombre_visible, f=nombre_archivo: self.preguntar_dimension(n, f),
                width=30, pady=5
            )
            btn.pack(pady=5)

    def preguntar_dimension(self, titulo_app, archivo):
        # Ventana pequeña para elegir si 2D O 3D
        self.vent_dim = tk.Toplevel(self.root)
        self.vent_dim.title("Seleccionar Dimensión")
        self.vent_dim.geometry("300x150")
        self.vent_dim.grab_set() # Bloquea el menú hasta que elija una opción

        tk.Label(self.vent_dim, text=f"{titulo_app}", font=("Arial", 9, "italic")).pack(pady=5)
        tk.Label(self.vent_dim, text="Elija la dimensión:", font=("Arial", 11, "bold")).pack()

        frame_btns = tk.Frame(self.vent_dim)
        frame_btns.pack(pady=15)

        tk.Button(frame_btns, text="2D", width=10, 
                  command=lambda: self.abrir_ventana_nueva(titulo_app, archivo, "2D")).pack(side="left", padx=10)
        tk.Button(frame_btns, text="3D", width=10, 
                  command=lambda: self.abrir_ventana_nueva(titulo_app, archivo, "3D")).pack(side="left", padx=10)

    def abrir_ventana_nueva(self, titulo_app, archivo, dimension):
        # Cerramos la pregunta y ocultamos el menú principal
        self.vent_dim.destroy()
        self.root.withdraw()
        
        nueva_ventana = tk.Toplevel()
        nueva_ventana.title(f"{titulo_app} - {dimension}")
        nueva_ventana.geometry("450x400")
        
        tk.Label(nueva_ventana, text=f"Módulo: {titulo_app}", font=("Arial", 12, "bold"), pady=10).pack()
        tk.Label(nueva_ventana, text=f"Modo seleccionado: {dimension}", fg="blue").pack()

        # Botón para regresar al menu
        btn_regresar = tk.Button(
            nueva_ventana, 
            text=" Regresar al Menú", 
            command=lambda: self.regresar(nueva_ventana),
            bg="#ecf0f1", pady=5
        )
        btn_regresar.pack(side="bottom", pady=20)

    def regresar(self, ventana_hija):
        ventana_hija.destroy()
        self.root.deiconify()

if __name__ == "__main__":
    root = tk.Tk()
    app = MenuPrincipal(root)
    root.mainloop()
    

