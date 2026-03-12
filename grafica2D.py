def grafica2D(self):

    try:

        p1=self.leer2(self.p1)
        p2=self.leer2(self.p2)
        p3=self.leer2(self.p3)

        ventana=tk.Toplevel()
        ventana.title("Gráfica 2D")

        canvas=tk.Canvas(ventana,width=400,height=400,bg="white")
        canvas.pack()

        # Escala simple
        escala=20
        centro=200

        puntos=[p1,p2,p3]

        coords=[]

        for x,y in puntos:

            px=centro+x*escala
            py=centro-y*escala

            coords.append((px,py))

            canvas.create_oval(px-4,py-4,px+4,py+4,fill="blue")

        # dibujar triángulo
        canvas.create_line(coords[0],coords[1],fill="black")
        canvas.create_line(coords[1],coords[2],fill="black")
        canvas.create_line(coords[2],coords[0],fill="black")

    except Exception as e:

        messagebox.showerror("Error",str(e))
