from PyQt6.QtWidgets import *

class cameraSettings(QMainWindow):
    def __init__(self, id):
        super().__init__()
        self.setWindowTitle(f"Camera settings - {id}")
        self.setMinimumSize(500, 500)