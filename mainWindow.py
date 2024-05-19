import numpy
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from newCamWindow import newCamWindow
from camThread import convert_cv_qt, camThread
from detectCameras import read_config

app = QApplication([])
screen_resolution = app.primaryScreen().size()
width = screen_resolution.width()
height = screen_resolution.height()

class MainWindow(QMainWindow):

    def __init__(self):
        #initialise ui
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
        self.running_cams = [0, 0]
        self.threads = []
        self.reload_cams()

    def camchoiceTabUi(self):
        # the camera choice tab ui
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
        # the camera view tab ui
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
        # new cam window - opens on "new (usb/ip) cam..."
        self.newcam = newCamWindow(type)
        self.newcam.show()

    def open_camera_sett(self, id):
        # window for changing camera config - name, ip, etc...
        def on_triggered():
            if "protocol" in self.js[id]:
                self.camerasett = newCamWindow("IP", id)
            else:
                self.camerasett = newCamWindow("USB", id)
            self.camerasett.show()
        return on_triggered
    @pyqtSlot(numpy.ndarray)
    def upd_cam(self,cv_img,index, i): #show next frame
        #run when a frame is delivered by camera-capturing thread
        #print("Updating", self.running_cans, i)
        global width
        global height
        pixmap = convert_cv_qt(cv_img, width, height)
        if index == 0:
            self.labelcam1.setPixmap(pixmap)
        elif index == 1:
            self.labelcam2.setPixmap(pixmap)
    def add_cameras_to_changecams(self):
        # sets up setting menu and
        # reads from configuration to
        # list configured cameras in settings menu
        self.settings.clear()
        ip = self.settings.addAction("New IP camera...")
        usb = self.settings.addAction("New USB camera...")

        for i in self.js:
            id = i["id"]

            self.settings.addAction(str(id)+" - "+i["name"]).triggered.connect(self.open_camera_sett(id))

        ip.triggered.connect(lambda x: self.open_new_cam("IP"))
        usb.triggered.connect(lambda x: self.open_new_cam("USB"))

        self.menu.addMenu(self.settings)

    def reload_cams(self):
        #read config file to update ui (list and choicelist)
        #change currently showing cameras if user changed his choice
        self.running_cams[0] = self.choicecam1.currentIndex()
        self.running_cams[1] = self.choicecam2.currentIndex()
        self.js = read_config()
        for i in self.threads:
            try:
                i.run = False
                i.terminate()
            except: pass
        self.threads = []

        self.list.clear()

        self.choicecam1.clear()
        self.choicecam2.clear()

        for i in self.js:
            QListWidgetItem(i["name"], self.list)
            id = i["id"]
            self.threads.append(camThread(int(id)))
            self.choicecam1.addItem(i["name"])
            self.choicecam2.addItem(i["name"])
        self.choicecam1.addItem("None")
        self.choicecam2.addItem("None")
        if self.running_cams[0]!=None:
            self.choicecam1.setCurrentIndex(self.running_cams[0])
        if self.running_cams[1]!=None:
            self.choicecam2.setCurrentIndex(self.running_cams[1])

        for i in self.running_cams:
            if i != (self.choicecam1.count()-1) and i!=-1:
                self.threads[i].change_pixmap_signal.connect(lambda cv_img, i=i: self.upd_cam(cv_img, (self.running_cams.index(i)), i))
                self.threads[i].start()

        self.add_cameras_to_changecams()


window = MainWindow()
window.show()
app.exec()