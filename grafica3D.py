def grafica3D(self):

    try:

        puntos=[self.leer3(e) for e in self.puntos3]

        ventana=tk.Toplevel()
        ventana.title("Gráfica 3D (Proyección)")

        canvas=tk.Canvas(ventana,width=400,height=400,bg="white")
        canvas.pack()

        escala=20
        centro=200

        coords=[]

        for x,y,z in puntos:

            # proyección simple 3D→2D
            px=centro+(x+z*0.5)*escala
            py=centro-(y+z*0.5)*escala

            coords.append((px,py))

            canvas.create_oval(px-4,py-4,px+4,py+4,fill="red")

        # unir puntos
        for i in range(len(coords)):

            for j in range(i+1,len(coords)):

                canvas.create_line(coords[i],coords[j])

    except Exception as e:

        messagebox.showerror("Error",str(e))
