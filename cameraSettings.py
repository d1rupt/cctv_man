from PyQt6.QtWidgets import *
from detectCameras import *
class cameraSettings(QMainWindow):
    def __init__(self, id):
        super().__init__()

        self.js = read_config()
        self.data = self.js[id]
        self.setWindowTitle(f"Camera settings - {self.data['name']}")

        self.setMinimumSize(500, 500)
        self.layout = QGridLayout()
        self.container = QWidget()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

        self.label = QLabel("Name")
        self.name = QLineEdit()
        self.name.setText(self.data['name'])
        self.layout.addWidget(self.label, 0, 0)
        self.layout.addWidget(self.name, 0, 1)