import json
from PyQt6.QtWidgets import *
from detectCameras import list_cameras_ids, read_config


class newCamWindow(QMainWindow):
    #opens window for creating a cam, or changing (if id is set) already existing one
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

            self.label2 = QLabel("Requires authorization")
            self.hascreds = QCheckBox()
            self.hascreds.stateChanged.connect(self.show_creds_fields)

            self.label3 = QLabel("Username")
            self.user = QLineEdit()


            self.label4 = QLabel("Password")
            self.passw = QLineEdit()
            self.passw.setEchoMode(QLineEdit.EchoMode.Password)


            self.list_creds = [self.label3, self.user, self.label4, self.passw]

            self.show_creds_fields()

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
            # get connected cameras ids
            ids = list_cameras_ids()
            self.idchoice = QComboBox()
            for id in ids:
                self.idchoice.addItem(str(id))

            self.layout.addWidget(self.label5,1,0)
            self.layout.addWidget(self.idchoice,1,1)
            if self.id!= None:
                data = self.js[self.id]
                self.idchoice.addItem(data["idchoice"])

        self.apply = QPushButton("Apply")
        self.apply.clicked.connect(self.apply_close)
        if self.id != None:
            self.name.setText(self.data["name"])
        self.layout.addWidget(self.apply,30,1)

    def apply_close(self):
        # write to cameras.json
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
            js["protocol"] = protocol.lower()
            js["ip"] = ip.lower()
            js["hascreds"] = hascreds
            js["user"] = user
            js["passw"] = passw


        else:
            idchoice = self.idchoice.currentText()
            js["idchoice"] = idchoice

        if self.id == None:
            js["id"] = len(self.js)
            self.js.append(js)
        else:
            js["id"] = self.id
            self.js[self.id] = js
        read_config()
        with open('./config/cameras.json', 'w') as f:
            json.dump(self.js, f, indent=4)
        self.close()

    def show_creds_fields(self):
        # show password and username fields when user checks `requires authorisation`
        # when configuring a camera
        if self.hascreds.isChecked() == True:
            for i in self.list_creds:
                i.show()
        else:
            for i in self.list_creds:
                i.hide()
