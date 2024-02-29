from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot, Qt
import cv2
import numpy
from PyQt6.QtGui import *
from detectCameras import *
def convert_cv_qt(cv_img,width,height):
    rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb_image.shape
    bytes_per_line = ch * w
    convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
    p = convert_to_Qt_format.scaled(width//2 - 10, height, Qt.AspectRatioMode.KeepAspectRatio)
    return QPixmap.fromImage(p)

class camThread(QThread):
    change_pixmap_signal = pyqtSignal(numpy.ndarray)
    def __init__(self,id):
        super().__init__()
        self.id = id
        self.run = True
        self.usb = False
        self.js = read_config()
        if ("idchoice" in self.js[id].keys()):
            self.usb = True

    #TODO: change this to capture IP ALSO!!! for now only usb
    def run(self):
        #print('running', self.id)
        if self.usb:
            print('running', self.id)
            print("thread: ", int(self.js[self.id]["idchoice"]))
            c = cv2.VideoCapture(int(self.js[self.id]["idchoice"]))
            while self.run:

                ret, cv_img = c.read()
                if ret:
                    print("EMITTING SIGNAL")
                    self.change_pixmap_signal.emit(cv_img)
                    print("EMITTED")
            c.release()

        else:
            #ip capture
            pass

