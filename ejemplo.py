import sys
import numpy as np
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QStackedWidget,
                             QDoubleSpinBox, QGridLayout, QGroupBox)
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MatplotlibCanvas(FigureCanvas):
    def __init__(self, is_3d=False):
        self.fig = Figure(figsize=(5, 5), dpi=100)
        if is_3d:
            self.ax = self.fig.add_subplot(111, projection='3d')
        else:
            self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)


class MenuWidget(QWidget):
    def __init__(self, switch_function):
        super().__init__()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Cálculos Geométricos por Determinantes")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)

        btn_2d = QPushButton("Geometría 2D (Recta y Área de Triángulo)")
        btn_2d.clicked.connect(lambda: switch_function(1))
        layout.addWidget(btn_2d)

        btn_3d = QPushButton("Geometría 3D (Plano y Volumen de Tetraedro)")
        btn_3d.clicked.connect(lambda: switch_function(2))
        layout.addWidget(btn_3d)

        self.setLayout(layout)


class Geo2DWidget(QWidget):
    def __init__(self, back_function):
        super().__init__()
        self.layout = QHBoxLayout()

        # Panel de control
        control_panel = QWidget()
        control_layout = QVBoxLayout()

        btn_back = QPushButton("Volver al Menú Principal")
        btn_back.clicked.connect(lambda: back_function(0))
        control_layout.addWidget(btn_back)

        self.points = np.array([[0.0, 0.0], [4.0, 0.0], [2.0, 4.0]])
        self.spinboxes = []

        grid = QGridLayout()
        labels = ["P1 (Recta/Triángulo)", "P2 (Recta/Triángulo)", "P3 (Triángulo)"]
        for i in range(3):
            grid.addWidget(QLabel(labels[i]), i, 0)
            sb_x = QDoubleSpinBox()
            sb_x.setRange(-20, 20)
            sb_x.setValue(self.points[i, 0])
            sb_x.valueChanged.connect(self.update_plot)

            sb_y = QDoubleSpinBox()
            sb_y.setRange(-20, 20)
            sb_y.setValue(self.points[i, 1])
            sb_y.valueChanged.connect(self.update_plot)

            grid.addWidget(sb_x, i, 1)
            grid.addWidget(sb_y, i, 2)
            self.spinboxes.append((sb_x, sb_y))

        control_layout.addLayout(grid)

        self.lbl_eq = QLabel("Ecuación de la recta (P1, P2): ")
        self.lbl_area = QLabel("Área del triángulo: ")
        control_layout.addWidget(self.lbl_eq)
        control_layout.addWidget(self.lbl_area)
        control_layout.addStretch()

        control_panel.setLayout(control_layout)

        # Lienzo Matplotlib
        self.canvas = MatplotlibCanvas(is_3d=False)

        self.layout.addWidget(control_panel, 1)
        self.layout.addWidget(self.canvas, 2)
        self.setLayout(self.layout)
        self.update_plot()

    def update_plot(self):
        for i in range(3):
            self.points[i, 0] = self.spinboxes[i][0].value()
            self.points[i, 1] = self.spinboxes[i][1].value()

        p1, p2, p3 = self.points

        # Determinante para Ecuación de la recta (P1, P2)
        # | x  y  1 |
        # | x1 y1 1 | = 0  => x(y1 - y2) - y(x1 - x2) + (x1*y2 - x2*y1) = 0
        # | x2 y2 1 |
        A = p1[1] - p2[1]
        B = -(p1[0] - p2[0])
        C = p1[0] * p2[1] - p2[0] * p1[1]
        self.lbl_eq.setText(f"Ecuación recta (P1,P2): {A:.2f}x + {B:.2f}y + {C:.2f} = 0")

        # Determinante para Área del triángulo (P1, P2, P3)
        matrix_area = np.array([
            [p1[0], p1[1], 1],
            [p2[0], p2[1], 1],
            [p3[0], p3[1], 1]
        ])
        area = 0.5 * abs(np.linalg.det(matrix_area))
        self.lbl_area.setText(f"Área del triángulo: {area:.2f} u²")

        self.canvas.ax.clear()
        self.canvas.ax.grid(True, linestyle='--', alpha=0.6)
        self.canvas.ax.axhline(0, color='black', linewidth=1)
        self.canvas.ax.axvline(0, color='black', linewidth=1)

        # Trazar polígono
        poly = np.vstack((self.points, self.points[0]))
        self.canvas.ax.plot(poly[:, 0], poly[:, 1], 'bo-', alpha=0.5)
        self.canvas.ax.fill(poly[:, 0], poly[:, 1], 'blue', alpha=0.2)

        # Trazar recta extendida P1-P2
        if p1[0] != p2[0] or p1[1] != p2[1]:
            dir_vec = p2 - p1
            t = np.linspace(-10, 10, 2)
            line_x = p1[0] + dir_vec[0] * t
            line_y = p1[1] + dir_vec[1] * t
            self.canvas.ax.plot(line_x, line_y, 'r--', label='Recta P1-P2')

        self.canvas.ax.set_xlim(-15, 15)
        self.canvas.ax.set_ylim(-15, 15)
        self.canvas.draw()


class Geo3DWidget(QWidget):
    def __init__(self, back_function):
        super().__init__()
        self.layout = QHBoxLayout()

        control_panel = QWidget()
        control_layout = QVBoxLayout()

        btn_back = QPushButton("Volver al Menú Principal")
        btn_back.clicked.connect(lambda: back_function(0))
        control_layout.addWidget(btn_back)

        self.points = np.array([[0., 0., 0.], [4., 0., 0.], [0., 4., 0.], [0., 0., 4.]])
        self.spinboxes = []

        grid = QGridLayout()
        labels = ["P1 (Plano/Tetra)", "P2 (Plano/Tetra)", "P3 (Plano/Tetra)", "P4 (Tetraedro)"]
        for i in range(4):
            grid.addWidget(QLabel(labels[i]), i, 0)
            sb_x = QDoubleSpinBox()
            sb_x.setRange(-10, 10)
            sb_x.setValue(self.points[i, 0])
            sb_x.valueChanged.connect(self.update_plot)

            sb_y = QDoubleSpinBox()
            sb_y.setRange(-10, 10)
            sb_y.setValue(self.points[i, 1])
            sb_y.valueChanged.connect(self.update_plot)

            sb_z = QDoubleSpinBox()
            sb_z.setRange(-10, 10)
            sb_z.setValue(self.points[i, 2])
            sb_z.valueChanged.connect(self.update_plot)

            grid.addWidget(sb_x, i, 1)
            grid.addWidget(sb_y, i, 2)
            grid.addWidget(sb_z, i, 3)
            self.spinboxes.append((sb_x, sb_y, sb_z))

        control_layout.addLayout(grid)

        self.lbl_eq = QLabel("Ecuación del plano (P1, P2, P3): ")
        self.lbl_vol = QLabel("Volumen del tetraedro: ")
        control_layout.addWidget(self.lbl_eq)
        control_layout.addWidget(self.lbl_vol)
        control_layout.addStretch()

        control_panel.setLayout(control_layout)

        self.canvas = MatplotlibCanvas(is_3d=True)

        self.layout.addWidget(control_panel, 1)
        self.layout.addWidget(self.canvas, 2)
        self.setLayout(self.layout)
        self.update_plot()

    def update_plot(self):
        for i in range(4):
            self.points[i, 0] = self.spinboxes[i][0].value()
            self.points[i, 1] = self.spinboxes[i][1].value()
            self.points[i, 2] = self.spinboxes[i][2].value()

        p1, p2, p3, p4 = self.points

        # Determinante Plano (P1, P2, P3)
        v1 = p2 - p1
        v2 = p3 - p1
        # Producto cruzado representa los cofactores del determinante matricial de 4x4 expandido
        n = np.cross(v1, v2)
        A, B, C = n
        D = -np.dot(n, p1)
        self.lbl_eq.setText(f"Plano (P1,P2,P3): {A:.2f}x + {B:.2f}y + {C:.2f}z + {D:.2f} = 0")

        # Determinante Volumen Tetraedro (P1, P2, P3, P4)
        matrix_vol = np.array([
            [p1[0], p1[1], p1[2], 1],
            [p2[0], p2[1], p2[2], 1],
            [p3[0], p3[1], p3[2], 1],
            [p4[0], p4[1], p4[2], 1]
        ])
        vol = (1 / 6) * abs(np.linalg.det(matrix_vol))
        self.lbl_vol.setText(f"Volumen del tetraedro: {vol:.2f} u³")

        self.canvas.ax.clear()

        # Trazar puntos y aristas del tetraedro
        for i in range(4):
            for j in range(i + 1, 4):
                xs = [self.points[i, 0], self.points[j, 0]]
                ys = [self.points[i, 1], self.points[j, 1]]
                zs = [self.points[i, 2], self.points[j, 2]]
                self.canvas.ax.plot(xs, ys, zs, 'b-', alpha=0.6)
        self.canvas.ax.scatter(self.points[:, 0], self.points[:, 1], self.points[:, 2], color='red', s=50)

        self.canvas.ax.set_xlim(-10, 10)
        self.canvas.ax.set_ylim(-10, 10)
        self.canvas.ax.set_zlim(-10, 10)
        self.canvas.draw()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Geometría Dinámica - Matrices y Determinantes")
        self.setGeometry(100, 100, 1000, 600)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.menu_widget = MenuWidget(self.switch_widget)
        self.geo2d_widget = Geo2DWidget(self.switch_widget)
        self.geo3d_widget = Geo3DWidget(self.switch_widget)

        self.stacked_widget.addWidget(self.menu_widget)  # Index 0
        self.stacked_widget.addWidget(self.geo2d_widget)  # Index 1
        self.stacked_widget.addWidget(self.geo3d_widget)  # Index 2

    def switch_widget(self, index):
        self.stacked_widget.setCurrentIndex(index)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
