import sys
from PySide6.QtWidgets import QApplication
from backend.grid_backend import GridBackend
from frontend.main_window import MainWindow

app = QApplication(sys.argv)

backend = GridBackend()
window = MainWindow(backend)
window.resize(900, 600)
window.show()

sys.exit(app.exec())
