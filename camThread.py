from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot, Qt
import cv2
import numpy
from PyQt6.QtGui import *
from detectCameras import *
from datetime import datetime
from mov_detection.detect import detect_mov
from mov_detection.get_background import get_background

def convert_cv_qt(cv_img,width,height):
    rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb_image.shape
    bytes_per_line = ch * w
    convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
    p = convert_to_Qt_format.scaled(width//2 - 10, height, Qt.AspectRatioMode.KeepAspectRatio)
    return QPixmap.fromImage(p)

def get_date_time():

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string
class camThread(QThread):
    change_pixmap_signal = pyqtSignal(numpy.ndarray)
    def __init__(self,id):
        super().__init__()
        self.id = id
        self.run = True
        self.usb = False
        self.js = read_config()
        self.name = self.js[id]["name"]
        if ("idchoice" in self.js[id].keys()):
            self.usb = True

    #TODO: change this to capture IP ALSO!!! for now only usb
    def run(self):
        #print('running', self.id)
        if self.usb:
            print('running', self.id)
            print("thread: ", int(self.js[self.id]["idchoice"]))
            c = cv2.VideoCapture(int(self.js[self.id]["idchoice"]))
            background = get_background(c)
            while self.run:

                ret, cv_img = c.read()
                if ret:
                    #detect movement
                    cv_img = detect_mov(background, cv_img)
                    cv_img = cv2.putText(cv_img, self.name, (10,20), 1, 1, (255,0,0),1 )
                    cv_img = cv2.putText(cv_img, get_date_time(), (10, 50), 1, 1, (255, 0, 0), 1)
                    self.change_pixmap_signal.emit(cv_img)
            c.release()

        else:
            #ip capture
            pass

