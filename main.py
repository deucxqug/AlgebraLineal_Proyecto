import tkinter as tk
from tkinter import messagebox

def saludar():
    nombre = entrada_nombre.get()
    if nombre:
        messagebox.showinfo("Mensaje", f"Hola {nombre}, bienvenido a Tkinter")
    else:
        messagebox.showwarning("Advertencia", "Por favor, escribe tu nombre")

if __name__ == '__main__':

    ventana = tk.Tk()
    ventana.title("Mi Primera GUI")
    ventana.geometry("300x200") # Ancho x Alto

    etiqueta = tk.Label(ventana, text="Escribe tu nombre:", font=("Arial", 10))
    entrada_nombre = tk.Entry(ventana)
    boton_accion = tk.Button(ventana, text="Saludar", command=saludar)

    # 3. Posicionar Widgets (Sistema de empaquetado)
    etiqueta.pack(pady=10)
    entrada_nombre.pack(pady=5)
    boton_accion.pack(pady=20)

    # 4. Iniciar el bucle de la aplicación
    ventana.mainloop()
