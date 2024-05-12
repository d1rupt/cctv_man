import numpy
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from newCamWindow import *
from camThread import *
from detectCameras import *
import cv2

app = QApplication([])
screen_resolution = app.primaryScreen().size()
width = screen_resolution.width()
height = screen_resolution.height()

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setMinimumSize(720,1000)

        self.button_is_checked = False
        self.setWindowTitle("CCTV")

        self.layout = QVBoxLayout()
        container = QWidget()

        self.menu = QMenuBar()
        self.setMenuBar(self.menu)
        self.settings = QMenu("Cameras", self)
        self.js = read_config()
        self.add_cameras_to_changecams()

        self.tabs = QTabWidget()
        self.tabs.addTab(self.camchoiceTabUi(), "Camera choice")
        self.tabs.addTab(self.camViewTabUi(), "Camera view")
        self.layout.addWidget(self.tabs)

        container.setLayout(self.layout)
        self.setCentralWidget(container)
        self.running_cans = [0,0]
        self.threads = []
        #self.choicecam2.currentIndexChanged.connect(lambda x: self.change_showing_cams(2, x))
        #self.choicecam1.currentIndexChanged.connect(lambda x: self.change_showing_cams(1, x))
        self.reload_cams()

    def camchoiceTabUi(self):
        camchoice = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        self.list = QListWidget()
        self.list.setFixedHeight(200)
        layout.addWidget(self.list, )
        self.choicecam1 = QComboBox()
        self.choicecam2 = QComboBox()

        layout.addWidget(self.choicecam1, )
        layout.addWidget(self.choicecam2, )
        self.button = QPushButton("Update")
        self.button.clicked.connect(self.reload_cams)
        layout.addWidget(self.button)
        layout.setSpacing(0)
        camchoice.setLayout(layout)
        return camchoice
    def camViewTabUi(self):
        global width
        global height
        camView = QWidget()
        layout = QHBoxLayout()

        self.labelcam1 = QLabel()
        self.labelcam1.setStyleSheet("background: blue;")
        self.labelcam1.resize(width//2 - 10, height)
        layout.addWidget(self.labelcam1)

        self.labelcam2 = QLabel()
        self.labelcam2.setStyleSheet("background: green;")
        self.labelcam2.resize(width//2 - 10, height)
        layout.addWidget(self.labelcam2)

        camView.setLayout(layout)
        return camView


    def open_new_cam(self, type):
        self.newcam = newCamWindow(type)
        self.newcam.show()

    def open_camera_sett(self, id):
        def on_triggered():
            print(f"ID: {id}")
            if "protocol" in self.js[id]:
                self.camerasett = newCamWindow("IP", id)
            else:
                self.camerasett = newCamWindow("USB", id)
            self.camerasett.show()
        return on_triggered
    @pyqtSlot(numpy.ndarray)
    def upd_cam(self,cv_img,index, i): #show next frame
        print("Updating", self.running_cans, i)
        global width
        global height
        #print("UPDATING CAM: ", i)
        #convert frame format
        pixmap = convert_cv_qt(cv_img, width, height)
        if index == 0:
            #print("UPDATING LABEL 1!")
            self.labelcam1.setPixmap(pixmap)
            #print("LABEL 1 updated")
        elif index == 1:
            #print("UPDATING LABEL 2!")
            self.labelcam2.setPixmap(pixmap)
            #print("LABEL 2 updated")
    def add_cameras_to_changecams(self): #list configured cameras in settings menu
        self.settings.clear()
        ip = self.settings.addAction("New IP camera...")
        usb = self.settings.addAction("New USB camera...")

        cams_menu = []
        for i in self.js:
            id = i["id"]
            print(id)

            self.settings.addAction(str(id)+" - "+i["name"]).triggered.connect(self.open_camera_sett(id))

        ip.triggered.connect(lambda x: self.open_new_cam("IP"))
        usb.triggered.connect(lambda x: self.open_new_cam("USB"))

        self.menu.addMenu(self.settings)

    def reload_cams(self): #read config file to update ui; change currently showing cameras if user changed
        #reloads cam listing, cam choice
        self.running_cans[0] = self.choicecam1.currentIndex()
        self.running_cans[1] = self.choicecam2.currentIndex()
        self.js = read_config()
        print("STOPPING THREADS")
        for i in self.threads:
            try:
                i.run = False
                i.terminate()
            except: pass
        self.threads = []

        self.list.clear()

        #self.choicecam1.currentIndexChanged.disconnect()
        #self.choicecam2.currentIndexChanged.disconnect()
        print("DISCONNECT")
        self.choicecam1.clear()
        self.choicecam2.clear()

        for i in self.js:
            QListWidgetItem(i["name"], self.list)
            id = i["id"]
            print("WRITTEN:", id, i["name"])
            self.threads.append(camThread(int(id)))
            self.choicecam1.addItem(i["name"])
            self.choicecam2.addItem(i["name"])
        self.choicecam1.addItem("None")
        self.choicecam2.addItem("None")
        if self.running_cans[0]!=None:
            self.choicecam1.setCurrentIndex(self.running_cans[0])
        if self.running_cans[1]!=None:
            self.choicecam2.setCurrentIndex(self.running_cans[1])

        #self.choicecam2.currentIndexChanged.connect(lambda x: self.change_showing_cams(2, x))
        #self.choicecam1.currentIndexChanged.connect(lambda x: self.change_showing_cams(1, x))
        print("CONNECT")
        print(f"Running {min(2, len(self.threads))} cams")
        for i in self.running_cans:
            print(self.running_cans, i, self.running_cans.index(i))
            if i != (self.choicecam1.count()-1) and i!=-1:
                #print("Starting thread")
                print("RUNNING INDEX", i)
                self.threads[i].change_pixmap_signal.connect(lambda cv_img, i=i: self.upd_cam(cv_img, (self.running_cans.index(i)), i))
                self.threads[i].start()
            else:
                print("None")

        self.add_cameras_to_changecams()

    def change_showing_cams(self, i ,ind):
        print('ok')
        self.running_cans[i-1] = ind
        print(self.running_cans)


window = MainWindow()


window.show()
app.exec()