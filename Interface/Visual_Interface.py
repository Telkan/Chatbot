from PyQt5.QtWidgets import QWidget, QSlider, QLineEdit, QLabel, QPushButton, QScrollArea, QApplication, \
    QHBoxLayout, QVBoxLayout, QMainWindow, QSpacerItem, QSizePolicy, QFormLayout, QGroupBox, QShortcut, QGridLayout
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QKeySequence
import sys


class mainWidget(QWidget):

    def __init__(self, parent):
        super().__init__(parent=parent)

        # Main layout
        self.layout = QVBoxLayout()

        # Logo zone
        self.logoZone = QHBoxLayout()
        self.labelRasaLogo = QLabel(self)
        self.labelUpssiLogo = QLabel(self)
        pixmap = QPixmap('images.png')
        pixmap = pixmap.scaled(48, 48, Qt.KeepAspectRatio)
        self.labelRasaLogo.setPixmap(pixmap)
        pixmap = QPixmap('logo_upssitech.png')
        pixmap = pixmap.scaled(164, 48, Qt.KeepAspectRatio)
        self.labelUpssiLogo.setPixmap(pixmap)
        self.logoZone.addWidget(self.labelRasaLogo)
        self.logoZone.addWidget(self.labelUpssiLogo)
        self.logoZone.setAlignment(Qt.AlignTop)

        # Text zone
        mygroupbox = QGroupBox('Visual Chatbot')
        self.myform = QFormLayout()
        self.messages = []
        mygroupbox.setLayout(self.myform)

        scroll = QScrollArea()
        scroll.setWidget(mygroupbox)
        scroll.setWidgetResizable(True)
        self.msgZone = QVBoxLayout()
        self.msgZone.addWidget(scroll)

        # Input zone
        self.sendZone = QHBoxLayout()
        self.labelTextZone = QLineEdit()
        self.validateButton = QPushButton("SEND")
        self.validateButton.clicked.connect(self.sendIntent)
        self.validateButton.setShortcut("Return")
        self.sendZone.addWidget(self.labelTextZone)
        self.sendZone.addWidget(self.validateButton)
        self.sendZone.setAlignment(Qt.AlignBottom)

        # Put all together
        self.layout.addLayout(self.logoZone)
        self.layout.addLayout(self.msgZone)
        self.layout.addLayout(self.sendZone)
        self.setLayout(self.layout)

        self.ansSc = QShortcut(QKeySequence('Ctrl+M'), self)
        self.ansSc.activated.connect(self.getUtter)

    def sendIntent(self):
        myLabel = QLabel(self.labelTextZone.text())
        myLabel.setAlignment(Qt.AlignRight)
        self.messages.append(myLabel)
        self.myform.addRow(self.messages[-1])
        self.labelTextZone.clear()

    def getUtter(self):
        myLabel = QLabel("ANSWER")  # Replace the ANSWER field by the bot answer
        myLabel.setAlignment(Qt.AlignLeft)
        self.messages.append(myLabel)
        self.myform.addRow(self.messages[-1])


class mainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        myWidget = mainWidget(self)
        self.setWindowTitle("MySuperInterface")
        self.resize(450, 600)
        self.setCentralWidget(myWidget)


app = QApplication(sys.argv)
app.setStyle('Fusion')
w = mainWindow()
w.show()
app.exec()
