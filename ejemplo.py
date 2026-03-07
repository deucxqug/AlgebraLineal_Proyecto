import sys
from typing import Final, Optional, List, Any
import numpy as np
from numpy.linalg import LinAlgError
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QDoubleSpinBox, QLabel, QMessageBox, QFrame)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Configuración global
LIMIT: Final[int] = 10


class MathEngine:
    """Motor de cálculo para transformaciones lineales."""

    @staticmethod
    def calcular_volumen(u: np.ndarray, v: np.ndarray, w: np.ndarray) -> float:
        """Calcula el determinante de una matriz 3x3."""
        # Los vectores u, v, w forman las columnas de la matriz
        matriz: np.ndarray = np.array([u, v, w]).T
        return float(np.linalg.det(matriz))


class MplCanvas(FigureCanvas):
    """Lienzo compatible con proyecciones 3D."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        self.fig: Figure = Figure(figsize=(8, 6), dpi=100)
        # Importante: Proyección 3D habilitada
        self.axes = self.fig.add_subplot(111, projection='3d')
        super().__init__(self.fig)


class GeoGebra3D(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Determinantes 3D: Volumen del Paralelepípedo - IPN")
        self.setMinimumSize(1000, 700)
        self._init_ui()

    def _init_ui(self) -> None:
        main_widget: QWidget = QWidget()
        self.setCentralWidget(main_widget)
        layout_principal: QHBoxLayout = QHBoxLayout(main_widget)

        # 1. Canvas 3D (Izquierda)
        self.canvas: MplCanvas = MplCanvas(self)
        layout_principal.addWidget(self.canvas, stretch=3)

        # 2. Panel de Control (Derecha)
        panel: QVBoxLayout = QVBoxLayout()
        layout_principal.addLayout(panel, stretch=1)

        panel.addWidget(QLabel("<b>Vectores en $\mathbb{R}^3$:</b>"))

        # Generar inputs para U, V y W
        self.u_inputs: List[QDoubleSpinBox] = self._crear_bloque_vector(panel, "Vector U (Rojo)", [4, 0, 0])
        self.v_inputs: List[QDoubleSpinBox] = self._crear_bloque_vector(panel, "Vector V (Verde)", [0, 4, 0])
        self.w_inputs: List[QDoubleSpinBox] = self._crear_bloque_vector(panel, "Vector W (Azul)", [0, 0, 4])

        # Resultados
        linea = QFrame();
        linea.setFrameShape(QFrame.Shape.HLine);
        panel.addWidget(linea)
        self.label_vol: QLabel = QLabel("Volumen: 64.00")
        self.label_vol.setStyleSheet("font-size: 16px; color: #1A5276; font-weight: bold;")
        panel.addWidget(self.label_vol)

        panel.addStretch()
        self.actualizar_escena()

    def _crear_bloque_vector(self, layout: QVBoxLayout, titulo: str, default: List[float]) -> List[QDoubleSpinBox]:
        layout.addWidget(QLabel(titulo))
        inputs = []
        fila = QHBoxLayout()
        for val in default:
            sb = QDoubleSpinBox()
            sb.setRange(-LIMIT, LIMIT)
            sb.setValue(val)
            sb.setSingleStep(0.5)
            sb.valueChanged.connect(self.actualizar_escena)
            fila.addWidget(sb)
            inputs.append(sb)
        layout.addLayout(fila)
        return inputs

    def actualizar_escena(self) -> None:
        try:
            # Obtener datos de la UI
            u: np.ndarray = np.array([i.value() for i in self.u_inputs])
            v: np.ndarray = np.array([i.value() for i in self.v_inputs])
            w: np.ndarray = np.array([i.value() for i in self.w_inputs])

            # Cálculo del determinante
            det: float = MathEngine.calcular_volumen(u, v, w)

            # Dibujado
            self._render_3d(u, v, w, det)

        except LinAlgError:
            self.label_vol.setText("Error: Vectores coplanares")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error en cálculo: {e}")

    def _render_3d(self, u: np.ndarray, v: np.ndarray, w: np.ndarray, vol: float) -> None:
        ax = self.canvas.axes
        ax.cla()

        # Límites y rejilla
        ax.set_xlim([-LIMIT, LIMIT]);
        ax.set_ylim([-LIMIT, LIMIT]);
        ax.set_zlim([-LIMIT, LIMIT])
        ax.set_xlabel('X');
        ax.set_ylabel('Y');
        ax.set_zlabel('Z')

        # Vértices del paralelepípedo (Combinaciones lineales)
        origin = np.array([0, 0, 0])
        vertices = [
            origin, u, v, w,
            u + v, u + w, v + w,
            u + v + w
        ]

        # Definición de las 6 caras (orden de vértices para cerrar el polígono)
        caras = [
            [vertices[0], vertices[1], vertices[4], vertices[2]],  # Base
            [vertices[3], vertices[5], vertices[7], vertices[6]],  # Tapa
            [vertices[0], vertices[1], vertices[5], vertices[3]],  # Lado 1
            [vertices[2], vertices[4], vertices[7], vertices[6]],  # Lado 2
            [vertices[0], vertices[2], vertices[6], vertices[3]],  # Lado 3
            [vertices[1], vertices[4], vertices[7], vertices[5]]  # Lado 4
        ]

        # Dibujar el volumen sombreado
        poly = Poly3DCollection(caras, alpha=0.3, facecolor='skyblue', edgecolor='navy')
        ax.add_collection3d(poly)

        # Dibujar los 3 vectores base con flechas
        for vec, color in zip([u, v, w], ['red', 'green', 'blue']):
            ax.quiver(0, 0, 0, vec[0], vec[1], vec[2], color=color, linewidth=3, arrow_length_ratio=0.1)

        self.label_vol.setText(f"Volumen (Det): {abs(vol):.2f}")
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GeoGebra3D()
    window.show()
    sys.exit(app.exec())
