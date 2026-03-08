import sys
import numpy as np

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QStackedWidget, QDoubleSpinBox, QGridLayout, QFrame
)

from PyQt6.QtCore import Qt

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


# ---------- GRAFICA ----------
class MatplotlibCanvas(FigureCanvas):

    def __init__(self, is_3d=False):

        self.fig = Figure(figsize=(5,5), dpi=100)

        if is_3d:
            self.ax = self.fig.add_subplot(111, projection='3d')
        else:
            self.ax = self.fig.add_subplot(111)

        super().__init__(self.fig)


# ---------- MENU ----------
class MenuWidget(QWidget):

    def __init__(self, switch_function):
        super().__init__()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        titulo = QLabel("Geometría con Determinantes")
        titulo.setStyleSheet("font-size:30px;font-weight:bold;")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(titulo)

        btn2d = QPushButton("Geometría en el plano (2D)")
        btn3d = QPushButton("Geometría en el espacio (3D)")

        btn2d.clicked.connect(lambda: switch_function(1))
        btn3d.clicked.connect(lambda: switch_function(2))

        btn2d.setMinimumHeight(50)
        btn3d.setMinimumHeight(50)

        layout.addSpacing(30)
        layout.addWidget(btn2d)
        layout.addWidget(btn3d)

        self.setLayout(layout)


# ---------- GEOMETRIA 2D ----------
class Geo2DWidget(QWidget):

    def __init__(self, back_function):
        super().__init__()

        main_layout = QHBoxLayout()

        panel = QFrame()
        panel.setStyleSheet("background:white;border-radius:10px")
        control = QVBoxLayout()

        btn_back = QPushButton("Regresar al menú")
        btn_back.clicked.connect(lambda: back_function(0))

        titulo = QLabel("Coordenadas")
        titulo.setStyleSheet("font-size:18px;font-weight:bold")

        control.addWidget(btn_back)
        control.addWidget(titulo)

        self.points = np.array([[0.,0.],[4.,0.],[2.,4.]])

        grid = QGridLayout()
        self.spinboxes = []

        grid.addWidget(QLabel("Punto"),0,0)
        grid.addWidget(QLabel("X"),0,1)
        grid.addWidget(QLabel("Y"),0,2)

        for i in range(3):

            sx = QDoubleSpinBox()
            sy = QDoubleSpinBox()

            sx.setRange(-20,20)
            sy.setRange(-20,20)

            sx.setValue(self.points[i,0])
            sy.setValue(self.points[i,1])

            sx.valueChanged.connect(self.update_plot)
            sy.valueChanged.connect(self.update_plot)

            grid.addWidget(QLabel(f"P{i+1}"),i+1,0)
            grid.addWidget(sx,i+1,1)
            grid.addWidget(sy,i+1,2)

            self.spinboxes.append((sx,sy))

        control.addLayout(grid)

        # RESULTADOS
        self.lbl_recta = QLabel()
        self.lbl_det = QLabel()
        self.lbl_area = QLabel()
        self.lbl_col = QLabel()

        for l in [self.lbl_recta,self.lbl_det,self.lbl_area,self.lbl_col]:
            l.setStyleSheet("font-size:14px")

        control.addSpacing(20)

        control.addWidget(self.lbl_recta)
        control.addWidget(self.lbl_det)
        control.addWidget(self.lbl_area)
        control.addWidget(self.lbl_col)

        control.addStretch()

        panel.setLayout(control)

        self.canvas = MatplotlibCanvas()

        main_layout.addWidget(panel,1)
        main_layout.addWidget(self.canvas,2)

        self.setLayout(main_layout)

        self.update_plot()


    def update_plot(self):

        for i in range(3):
            self.points[i,0] = self.spinboxes[i][0].value()
            self.points[i,1] = self.spinboxes[i][1].value()

        p1,p2,p3 = self.points

        A = p1[1]-p2[1]
        B = -(p1[0]-p2[0])
        C = p1[0]*p2[1]-p2[0]*p1[1]

        self.lbl_recta.setText(f"Recta: {A:.2f}x + {B:.2f}y + {C:.2f} = 0")

        matrix_area = np.array([
            [p1[0],p1[1],1],
            [p2[0],p2[1],1],
            [p3[0],p3[1],1]
        ])

        det = np.linalg.det(matrix_area)

        area = abs(det)/2

        self.lbl_det.setText(f"Determinante = {det:.2f}")

        self.lbl_area.setText(f"Área triángulo = {area:.2f}")

        if abs(det) < 1e-6:
            self.lbl_col.setText("Puntos COLINEALES")
        else:
            self.lbl_col.setText("Puntos NO colineales")

        self.canvas.ax.clear()

        poly = np.vstack((self.points,self.points[0]))

        self.canvas.ax.plot(poly[:,0],poly[:,1],'bo-')
        self.canvas.ax.fill(poly[:,0],poly[:,1],alpha=0.2)

        dir_vec = p2-p1

        t = np.linspace(-10,10,2)

        line_x = p1[0] + dir_vec[0]*t
        line_y = p1[1] + dir_vec[1]*t

        self.canvas.ax.plot(line_x,line_y,'r--')

        self.canvas.ax.grid(True)

        self.canvas.draw()


# ---------- GEOMETRIA 3D ----------
class Geo3DWidget(QWidget):

    def __init__(self, back_function):
        super().__init__()

        layout = QHBoxLayout()

        panel = QFrame()
        panel.setStyleSheet("background:white;border-radius:10px")

        control = QVBoxLayout()

        btn_back = QPushButton("Regresar al menú")
        btn_back.clicked.connect(lambda: back_function(0))

        control.addWidget(btn_back)

        self.points = np.array([
            [0.,0.,0.],
            [4.,0.,0.],
            [0.,4.,0.],
            [0.,0.,4.]
        ])

        grid = QGridLayout()

        self.spinboxes = []

        grid.addWidget(QLabel("Punto"),0,0)
        grid.addWidget(QLabel("X"),0,1)
        grid.addWidget(QLabel("Y"),0,2)
        grid.addWidget(QLabel("Z"),0,3)

        for i in range(4):

            sx = QDoubleSpinBox()
            sy = QDoubleSpinBox()
            sz = QDoubleSpinBox()

            sx.setRange(-10,10)
            sy.setRange(-10,10)
            sz.setRange(-10,10)

            sx.setValue(self.points[i,0])
            sy.setValue(self.points[i,1])
            sz.setValue(self.points[i,2])

            sx.valueChanged.connect(self.update_plot)
            sy.valueChanged.connect(self.update_plot)
            sz.valueChanged.connect(self.update_plot)

            grid.addWidget(QLabel(f"P{i+1}"),i+1,0)
            grid.addWidget(sx,i+1,1)
            grid.addWidget(sy,i+1,2)
            grid.addWidget(sz,i+1,3)

            self.spinboxes.append((sx,sy,sz))

        control.addLayout(grid)

        self.lbl_plano = QLabel()
        self.lbl_det = QLabel()
        self.lbl_vol = QLabel()

        control.addWidget(self.lbl_plano)
        control.addWidget(self.lbl_det)
        control.addWidget(self.lbl_vol)

        control.addStretch()

        panel.setLayout(control)

        self.canvas = MatplotlibCanvas(is_3d=True)

        layout.addWidget(panel,1)
        layout.addWidget(self.canvas,2)

        self.setLayout(layout)

        self.update_plot()


    def update_plot(self):

        for i in range(4):
            self.points[i,0] = self.spinboxes[i][0].value()
            self.points[i,1] = self.spinboxes[i][1].value()
            self.points[i,2] = self.spinboxes[i][2].value()

        p1,p2,p3,p4 = self.points

        v1 = p2-p1
        v2 = p3-p1

        n = np.cross(v1,v2)

        A,B,C = n
        D = -np.dot(n,p1)

        self.lbl_plano.setText(f"Plano: {A:.2f}x + {B:.2f}y + {C:.2f}z + {D:.2f} = 0")

        matrix = np.array([
            [p1[0],p1[1],p1[2],1],
            [p2[0],p2[1],p2[2],1],
            [p3[0],p3[1],p3[2],1],
            [p4[0],p4[1],p4[2],1]
        ])

        det = np.linalg.det(matrix)

        vol = abs(det)/6

        self.lbl_det.setText(f"Determinante = {det:.2f}")

        self.lbl_vol.setText(f"Volumen tetraedro = {vol:.2f}")

        self.canvas.ax.clear()

        for i in range(4):
            for j in range(i+1,4):

                xs=[self.points[i,0],self.points[j,0]]
                ys=[self.points[i,1],self.points[j,1]]
                zs=[self.points[i,2],self.points[j,2]]

                self.canvas.ax.plot(xs,ys,zs)

        self.canvas.ax.scatter(self.points[:,0],self.points[:,1],self.points[:,2])

        self.canvas.draw()


# ---------- VENTANA ----------
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Geometría con Determinantes")

        self.resize(1100,600)

        self.stack = QStackedWidget()

        self.setCentralWidget(self.stack)

        self.menu = MenuWidget(self.switch)
        self.geo2d = Geo2DWidget(self.switch)
        self.geo3d = Geo3DWidget(self.switch)

        self.stack.addWidget(self.menu)
        self.stack.addWidget(self.geo2d)
        self.stack.addWidget(self.geo3d)

    def switch(self,i):
        self.stack.setCurrentIndex(i)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())