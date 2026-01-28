import numpy as np
from PySide6.QtCore import QObject, Signal, Slot

class GridBackend(QObject):
    grid_ready = Signal(object)

    @Slot(dict)
    def create_grid(self, cfg):
        x_min = cfg["x_min"]
        x_max = cfg["x_max"]
        y_min = cfg["y_min"]
        y_max = cfg["y_max"]
        dx = cfg["dx"]
        dy = cfg["dy"]

        # Validation (important)
        if x_max <= x_min or y_max <= y_min:
            return
        if dx <= 0 or dy <= 0:
            return

        nx = int((x_max - x_min) / dx)
        ny = int((y_max - y_min) / dy)

        grid = np.zeros((ny, nx))  # Y rows, X columns
        self.grid_ready.emit(grid)
