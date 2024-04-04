import json

from PyQt6.QtWidgets import *
from detectCameras import list_cameras_ids, read_config


class newCamWindow(QMainWindow):
    def __init__(self, type, id=None):
        self.id = id

        super().__init__()
        self.js = read_config()
        if self.id != None:
            self.data = self.js[self.id]
        self.type = type
        self.setWindowTitle(f"Camera - {type}")
        self.setMinimumSize(500, 500)
        self.layout = QGridLayout()
        self.container = QWidget()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

        self.label = QLabel("Name")
        self.name = QLineEdit()
        self.layout.addWidget(self.label,0,0)
        self.layout.addWidget(self.name,0,1)

        if type == "IP":
            self.label0 = QLabel("Connection protocol")
            self.protocol = QComboBox()
            self.protocol.addItem("HTTP")
            self.protocol.addItem("RSTP")

            self.label1 = QLabel("Url \n <ip>:<port>/<uri>")
            self.ip = QLineEdit()
            self.ip.textEdited.connect(self.ip_check)

            self.label2 = QLabel("Requires authorization")
            self.hascreds = QCheckBox()
            self.hascreds.stateChanged.connect(self.show_creds_fields)

            self.label3 = QLabel("Username")
            self.user = QLineEdit()


            self.label4 = QLabel("Password")
            self.passw = QLineEdit()
            self.passw.setEchoMode(QLineEdit.EchoMode.Password)


            self.list_creds = [self.label3, self.user, self.label4, self.passw]

            self.hide_show(self.list_creds, False)

            self.layout.addWidget(self.label0,1,0)
            self.layout.addWidget(self.protocol,1,1)
            self.layout.addWidget(self.label1,2,0)
            self.layout.addWidget(self.ip,2,1)
            self.layout.addWidget(self.label2,3,0)
            self.layout.addWidget(self.hascreds, 3,1)
            self.layout.addWidget(self.label3, 4,0)
            self.layout.addWidget(self.user, 4,1)
            self.layout.addWidget(self.label4,5,0)
            self.layout.addWidget(self.passw,5,1)
            if self.id != None:
                self.protocol.setCurrentIndex(self.protocol.findText(self.data["protocol"]))
                self.ip.setText(self.data["ip"])


        else:
            self.label5 = QLabel("Available cameras")
            ids = list_cameras_ids()
            print('inserting ids')
            self.idchoice = QComboBox()
            for id in ids:
                self.idchoice.addItem(str(id))

            self.layout.addWidget(self.label5,1,0)
            self.layout.addWidget(self.idchoice,1,1)
            if self.id!= None:
                data = self.js[self.id]
                self.idchoice.addItem(data["idchoice"])


        self.label6 = QLabel("Movement detection")
        self.movdetect = QCheckBox()
        self.movdetect.stateChanged.connect(self.show_movdetect_options)

        self.layout.addWidget(self.label6,20,0)
        self.layout.addWidget(self.movdetect,20,1)

        self.label7 = QLabel("Absolute path to video storage")
        self.path = QLineEdit()

        self.label8 = QLabel("Notify using pop-ups when motion is detected")
        self.popup = QCheckBox()

        self.layout.addWidget(self.label7, 21,0)
        self.layout.addWidget(self.path,21,1)
        self.layout.addWidget(self.label8,22,0)
        self.layout.addWidget(self.popup,22,1)

        self.list_movdetect = [self.label7, self.path, self.label8, self.popup]
        self.hide_show(self.list_movdetect, False)

        self.apply = QPushButton("Apply")
        self.apply.clicked.connect(self.apply_close)
        if self.id != None:
            self.name.setText(self.data["name"])
        self.layout.addWidget(self.apply,30,1)

    def apply_close(self):
        js = {}
        js["name"] = self.name.text()
        if self.type == "IP":
            protocol = self.protocol.currentText()
            ip = self.ip.text()
            hascreds = self.hascreds.isChecked()
            user = 0
            passw = 0
            if hascreds:
                user = self.user.text()
                passw = self.passw.text()
            js["protocol"] = protocol
            js["ip"] = ip
            js["hascreds"] = hascreds
            js["user"] = user
            js["passw"] = passw


        else:
            idchoice = self.idchoice.currentText()
            js["idchoice"] = idchoice
        movdetect = self.movdetect.isChecked()
        path = 0
        popup = 0
        if movdetect:
            path = self.path.text()
            popup = self.popup.isChecked()
        js["movdetect"] = movdetect
        js["path"] = path
        js["popup"] = popup

        if self.id == None:
            js["id"] = len(self.js)
            self.js.append(js)
        else:
            print("REWRITING")
            js["id"] = self.id
            print(js)
            self.js[self.id] = js
        with open('./config/cameras.json', 'w') as f:
            json.dump(self.js, f, indent=4)
        #print(js)
        self.close()

    def ip_check(self,ip):
        #TODO: check ip for correctness
        pass

    def show_creds_fields(self):
        self.hide_show(self.list_creds, self.hascreds.isChecked())

    def hide_show(self,list, show):
        if show == True:
            for i in list:
                i.show()

        else:
            for i in list:
                i.hide()

    def show_movdetect_options(self):
        self.hide_show(self.list_movdetect, self.movdetect.isChecked())