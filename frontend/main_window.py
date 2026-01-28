from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QRadioButton, QGroupBox,
    QLabel, QDoubleSpinBox
)
import pyqtgraph as pg
import numpy as np

class MainWindow(QWidget):
    def __init__(self, backend):
        super().__init__()
        self.backend = backend
        self.setWindowTitle("Bike Radar Grid Setup")

        self._build_ui()
        self.backend.grid_ready.connect(self.update_grid)

    def _build_ui(self):
        main_layout = QVBoxLayout(self)

        # -------- Mode selection --------
        mode_box = QGroupBox("Mode")
        mode_layout = QHBoxLayout()

        self.auto_btn = QRadioButton("Auto")
        self.manual_btn = QRadioButton("Manual")
        self.manual_btn.setChecked(True)

        mode_layout.addWidget(self.auto_btn)
        mode_layout.addWidget(self.manual_btn)
        mode_box.setLayout(mode_layout)

        main_layout.addWidget(mode_box)

        # -------- Grid parameters --------
        self.param_box = QGroupBox("Grid Parameters (Manual)")
        param_layout = QVBoxLayout()

        self.xmin = self._spin("X Min", param_layout)
        self.xmax = self._spin("X Max", param_layout, 20.0)
        self.ymin = self._spin("Y Min", param_layout, -5.0)
        self.ymax = self._spin("Y Max", param_layout, 5.0)
        self.dx   = self._spin("Cell Size X", param_layout, 0.5)
        self.dy   = self._spin("Cell Size Y", param_layout, 0.5)

        self.param_box.setLayout(param_layout)
        main_layout.addWidget(self.param_box)

        # -------- Create Grid Button --------
        self.create_btn = QPushButton("Create Grid")
        self.create_btn.clicked.connect(self.on_create_grid)
        main_layout.addWidget(self.create_btn)

        # -------- Plot --------
        self.plot = pg.PlotWidget()
        self.image = pg.ImageItem()
        self.plot.addItem(self.image)
        self.plot.setLabel("bottom", "X cells")
        self.plot.setLabel("left", "Y cells")

        main_layout.addWidget(self.plot)

        # Enable/disable params based on mode
        self.manual_btn.toggled.connect(self.param_box.setEnabled)

    def _spin(self, label, layout, default=0.0):
        row = QHBoxLayout()
        row.addWidget(QLabel(label))
        spin = QDoubleSpinBox()
        spin.setRange(-1000, 1000)
        spin.setValue(default)
        spin.setDecimals(2)
        row.addWidget(spin)
        layout.addLayout(row)
        return spin

    def on_create_grid(self):
        cfg = {
            "x_min": self.xmin.value(),
            "x_max": self.xmax.value(),
            "y_min": self.ymin.value(),
            "y_max": self.ymax.value(),
            "dx": self.dx.value(),
            "dy": self.dy.value(),
            "mode": "manual" if self.manual_btn.isChecked() else "auto"
        }
        self.backend.create_grid(cfg)

    def update_grid(self, grid):
        self.image.setImage(grid, autoLevels=False)
