from PyQt6.QtWidgets import *
from detectCameras import *
class cameraSettings(QMainWindow):
    def __init__(self, id):
        super().__init__()

        self.js = read_config()
        self.setWindowTitle(f"Camera settings - {self.js[id]['name']}")
        self.setMinimumSize(500, 500)