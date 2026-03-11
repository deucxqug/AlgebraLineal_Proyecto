import tkinter as tk
from tkinter import messagebox

class MenuPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicaciones de los Determinantes")
        self.root.geometry("400x500")
        
        #Titulos 
        tk.Label(self.root, text="Menú Principal", font=("Arial", 16, "bold"), pady=20).pack()
        tk.Label(self.root, text="Seleccione una aplicación:", font=("Arial", 10)).pack()

        # Lista de botones junto a las rutas de los archivos
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
                command=lambda n=nombre_visible, f=nombre_archivo: self.abrir_ventana_nueva(n, f),
                width=30, pady=5
            )
            btn.pack(pady=5)

    def abrir_ventana_nueva(self, titulo_app, archivo):
        # Para ocultar la ventana principal
        self.root.withdraw()
        
        # Creamos una ventana nueva (Toplevel)
        nueva_ventana = tk.Toplevel()
        nueva_ventana.title(titulo_app)
        nueva_ventana.geometry("400x300")
        
        tk.Label(nueva_ventana, text=f"Módulo: {titulo_app}", font=("Arial", 12, "bold"), pady=20).pack()
        
        # --- Aqui ira la informacion de cada archivo que se mostrara en cada ventana ---
        tk.Label()
        
        # Botón para regresar
        btn_regresar = tk.Button(
            nueva_ventana, 
            text=" Regresar al Menú", 
            command=lambda: self.regresar(nueva_ventana),
            bg="#ecf0f1"
        )
        btn_regresar.pack(pady=20)

    def regresar(self, ventana_hija):
        ventana_hija.destroy() # Elimina la ventana actual
        self.root.deiconify()  # Vuelve a mostrar el menú principal

if __name__ == "__main__":
    root = tk.Tk()
    app = MenuPrincipal(root)
    root.mainloop()
