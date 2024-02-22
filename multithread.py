
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import sys
import time as tm

app = QApplication([])

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("GET OUT OF YOUR SLUMP!")
        self.threadpool = QThreadPool()

        self.button = QPushButton()
        self.button.setText("Start timer")
        self.button.clicked.connect(self.timerStart)

        self.label = QLabel()
        self.timer = 5
        self.label.setText(f'The timer is: {self.timer} minutes!')

        self.input = QLineEdit()
        self.input.textEdited.connect(self.newtime)
        self.layout = QGridLayout()
        self.layout.addWidget(self.label, 0,0)
        self.layout.addWidget(self.input, 1,0)
        self.layout.addWidget(self.button, 2,0,)
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    def newtime(self, time):
        try:
            timen = int(time)
            self.timer = timen
            self.label.setText(f'The timer is: {timen} minutes!')
        except:
            pass

    def goBackTitle(self):
        self.loop = False
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    def timerStart(self):
        self.time = self.timer * 60
        self.label2 = QLabel()
        self.label2.setText(f"Time left: {self.time//60}m {self.time%60}s")

        self.button2 = QPushButton()
        self.button2.setText("Go Back.")
        self.button2.clicked.connect(self.goBackTitle)
        layout2 = QGridLayout()
        layout2.addWidget(self.label2)
        layout2.addWidget(self.button2)
        wi = QWidget()
        wi.setLayout(layout2)
        self.setCentralWidget(wi)
        self.loop = True
        #Do timer
        t = self.time
        for i in range(0,t,1):
            QApplication.processEvents()
            tm.sleep(1)
            self.time-=1
            self.label2.setText(f"Time left: {self.time // 60}m {self.time % 60}s")
            if not self.loop:
                return





window = MainWindow()
window.show()
app.exec()