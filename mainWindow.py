import numpy
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from newCamWindow import *
from cameraSettings import *
from camThread import *
from detectCameras import *
import cv2

app = QApplication([])

#any settings changed - get written to a file
#the MainWindow then accesses this file

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setMinimumSize(720,1000)

        self.button_is_checked = False
        self.setWindowTitle("CCTV")

        menu = QMenuBar()
        self.setMenuBar(menu)
        settings = QMenu("Settings",self)
        new = settings.addMenu("Add camera")

        self.change = settings.addMenu("Change camera")
        self.js = read_config()
        self.add_cameras_to_changecams()
        ip = new.addAction("IP")
        usb = new.addAction("USB")
        ip.triggered.connect(lambda x: self.open_new_cam("IP"))
        usb.triggered.connect(lambda x: self.open_new_cam("USB"))

        menu.addMenu(settings)
        self.layout = QVBoxLayout()
        container = QWidget()

        self.tabs = QTabWidget()
        self.tabs.addTab(self.camchoiceTabUi(), "Camera choice")
        self.tabs.addTab(self.camViewTabUi(), "Camera view")
        self.layout.addWidget(self.tabs)

        container.setLayout(self.layout)
        self.setCentralWidget(container)


        self.threads = []

        for i in self.js:
            QListWidgetItem(i["name"], self.list)
            id = i["id"]
            print("WRITTEN:", id, i["name"])
            self.threads.append(camThread(int(id)))
        print(f"Running {min(2,len(self.threads))} cams")
        for i in range(min(2,len(self.threads))):
            self.threads[i].change_pixmap_signal.connect(lambda cv_img: self.upd_cam(cv_img, i))
            self.threads[i].start()
        #TODO: for now, shows only 2 first cams! Make usr choose
    def camchoiceTabUi(self):
        camchoice = QWidget()
        layout = QVBoxLayout()
        self.list = QListWidget()
        label = QLabel("Configured cameras:")
        layout.addWidget(label, )
        layout.addWidget(self.list, )
        choicecam1 = QComboBox()
        choicecam2 = QComboBox()

        layout.addWidget(choicecam1, )
        layout.addWidget(choicecam2, )
        camchoice.setLayout(layout)
        return camchoice
    def camViewTabUi(self):
        camView = QWidget()
        layout = QVBoxLayout()

        self.labelcam1 = QLabel()
        self.labelcam1.setStyleSheet("background: blue;")
        self.labelcam1.resize(640, 480)
        layout.addWidget(self.labelcam1)

        self.labelcam2 = QLabel()
        self.labelcam2.setStyleSheet("background: green;")
        self.labelcam2.resize(640, 480)
        layout.addWidget(self.labelcam2)

        camView.setLayout(layout)
        return camView


    def open_new_cam(self, type):
        self.newcam = newCamWindow(type)
        self.newcam.show()

    def open_camera_sett(self, id):
        self.camerasett = cameraSettings(id)
        self.camerasett.show()
    @pyqtSlot(numpy.ndarray)
    def upd_cam(self,cv_img,i):
        print("UPDATING CAM: ", i)
        pixmap = convert_cv_qt(cv_img)
        if i == 0:
            print("UPDATING LABEL 1!")
            self.labelcam1.setPixmap(pixmap)
            print("LABEL 1 updated")
        else:
            print("UPDATING LABEL 2!")
            self.labelcam2.setPixmap(pixmap)
            print("LABEL 2 updated")
    def add_cameras_to_changecams(self):
        for i in self.js:
            self.change.addAction(str(i["id"])+" - "+i["name"])



window = MainWindow()


window.show()
app.exec()