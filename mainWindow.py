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
        # TODO: read from settings file and display them under change add_action
        ip = new.addAction("IP")
        usb = new.addAction("USB")
        ip.triggered.connect(lambda x: self.open_new_cam("IP"))
        usb.triggered.connect(lambda x: self.open_new_cam("USB"))

        menu.addMenu(settings)
        self.layout = QGridLayout()

        container = QWidget()

        self.labelcam1 = QLabel()
        self.labelcam1.setStyleSheet("background: gray;")
        self.labelcam1.resize(640, 480)

        self.layout.addWidget(self.labelcam1,0,1)

        self.labelcam2 = QLabel()
        self.labelcam2.setStyleSheet("background: gray;")
        self.labelcam2.resize(640, 480)
        self.layout.addWidget(self.labelcam2, 1, 1)

        container.setLayout(self.layout)
        self.setCentralWidget(container)


        self.threads = []
        list = QListWidget()
        label = QLabel("Configured cameras:")
        self.layout.addWidget(label,0,0)
        self.layout.addWidget(list, 1,0)
        for i in self.js:
            QListWidgetItem(i["name"], list)
            id = i["id"]
            print("WRITTEN:", id, i["name"])
            self.threads.append(camThread(int(id)))
        print(f"Running {min(2,len(self.threads))} cams")
        for i in range(min(2,len(self.threads))):
            self.threads[i].change_pixmap_signal.connect(lambda cv_img: self.upd_cam(cv_img, i))
            self.threads[i].start()
        #TODO: for now, shows only 2 first cams! Make usr choose

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