from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot, Qt
import cv2
import numpy
from PyQt6.QtGui import *
from detectCameras import *
from datetime import datetime
from windows_toasts import Toast, WindowsToaster
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
        self.toaster = WindowsToaster('Python')
        if self.usb: #this is a usb camera
            print('running', self.id)
            print("thread: ", int(self.js[self.id]["idchoice"]))
            try:
                c = cv2.VideoCapture(int(self.js[self.id]["idchoice"]))
            except:
                print("Failed USB capture")
                self.run = False
        else:
            # ip capture
            ip = self.js[self.id]["ip"]
            protocol = self.js[self.id]["protocol"]
            creds = ""
            if self.js[self.id]["user"]:
                creds = f"{self.js[self.id]['user']}:{self.js[self.id]['passw']}@"
            print(f'{protocol}://{creds}{ip}')
            try:
                c = cv2.VideoCapture(f'{protocol}://{creds}{ip}')
            except:
                print("Failed IP captute")
                self.run = False
            #calculate background for movement capture
        background = get_background(c)

        notif = False
        while self.run:

            ret, cv_img = c.read()
            if ret:
                #detects movement and draws contours arount new objects
                cv_img, movement = detect_mov(background, cv_img)
                if movement == True and notif == False:

                    notif = True
                    #sends nodification using windows_toasts lib
                    self.notification()
                elif movement == False:
                    notif = False
                #add name & time to camera feed
                cv_img = cv2.putText(cv_img, self.name, (10,20), 1, 1, (255,0,0),1 )
                cv_img = cv2.putText(cv_img, get_date_time(), (10, 50), 1, 1, (255, 0, 0), 1)
                self.change_pixmap_signal.emit(cv_img)
        c.release()


    def notification(self):
        self.newToast = Toast()
        self.newToast.text_fields = [f'[{self.name}] - Movement Detected!']
        self.toaster.show_toast(self.newToast)


