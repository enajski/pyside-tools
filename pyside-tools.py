import sys
from subprocess import *
from time import gmtime, strftime
from PySide.QtCore import *
from PySide.QtGui import *

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setWindowTitle("Simple tools")
        
        # asset number / IP / server name widget
        self.assetBoxLabel = QLabel("Asset no / IP / Server name")
        self.assetBox = QLineEdit()
        self.assetBoxWidget = QFrame()
        layoutAsset = QHBoxLayout()
        layoutAsset.addWidget(self.assetBoxLabel)
        layoutAsset.addWidget(self.assetBox)
        self.assetBoxWidget.setLayout(layoutAsset)

        # Tools widget
        self.toolBoxLabel = QLabel("Please choose action:")
        self.toolBoxLabel.setAlignment(Qt.AlignCenter)
        self.pingButton = QPushButton("Ping", parent=None)
        self.pingButton.clicked.connect(self.ping)
        self.mstscButton = QPushButton("Remote Desktop", parent=None)
        self.mstscButton.clicked.connect(self.mstsc)
        self.uptimeButton = QPushButton("Uptime", parent=None)
        self.uptimeButton.clicked.connect(self.uptime)
        self.remoteCleanButton = QPushButton("Remote Clean", parent=None)
        self.remoteCleanButton.clicked.connect(self.batchScript)
        self.toolBoxWidget1 = QFrame()
        layoutTools1 = QHBoxLayout()
        layoutTools1.addWidget(self.pingButton)
        layoutTools1.addWidget(self.mstscButton)
        layoutTools1.addWidget(self.uptimeButton)
        self.toolBoxWidget1.setLayout(layoutTools1)
        self.toolBoxWidget2 = QFrame()
        layoutTools2 = QHBoxLayout()
        layoutTools2.addWidget(self.remoteCleanButton)
        self.toolBoxWidget2.setLayout(layoutTools2)

        # Console
        self.textConsole = QTextEdit("Enter details")
        self.textConsole.setMinimumHeight(150)
        self.clearConsoleButton = QPushButton("Clear console", parent=None)
        self.clearConsoleButton.clicked.connect(self.clearConsole)

        # Central widget
        self.box1 = QFrame()
        self.setCentralWidget(self.box1)
        layout = QVBoxLayout()
        layout.addWidget(self.assetBoxWidget)
        layout.addWidget(self.toolBoxLabel)
        layout.addWidget(self.toolBoxWidget1)
        layout.addWidget(self.toolBoxWidget2)
        layout.addWidget(self.textConsole)
        layout.addWidget(self.clearConsoleButton)
        self.box1.setLayout(layout)
        
    # Returns current time to console
    def reportTime(self):
        self.textConsole.append(strftime("%Y-%m-%d %H:%M:%S", gmtime()))

    # define the ping method
    def ping(self):
        try:
            pingResult = check_output(["ping", self.assetBox.text()], shell=True, stderr=STDOUT)
            self.textConsole.setTextColor("green")
            self.textConsole.append("Running ping command on " + self.assetBox.text())
            self.reportTime()
            self.textConsole.setTextColor("black")
            self.textConsole.append(pingResult)
            self.textConsole.append("*******************")
        except CalledProcessError:
            self.textConsole.setTextColor("red")
            self.reportTime()
            self.textConsole.append("Destination " + self.assetBox.text() + " not responding or invalid target selected.\n")

    # define the MS Terminal Services method
    def mstsc(self):
        self.textConsole.setTextColor("black")
        self.reportTime()
        self.textConsole.append("Starting Remote Desktop Client...\n")
        call(["mstsc", "/v:" + self.assetBox.text()])

    # define the uptime method
    def uptime(self):
        try:
            uptimeResult = check_output(["uptime", self.assetBox.text()], shell=True, stderr=STDOUT)
            self.textConsole.setTextColor("green")
            self.textConsole.append(uptimeResult)
        except CalledProcessError:
            self.textConsole.setTextColor("red")
            self.reportTime()
            self.textConsole.append("Failed to reach server " + self.assetBox.text() + " or cannot start the uptime command.\n")
            
    # clear console output
    def clearConsole(self):
        self.textConsole.clear()

    # run a batch script
    def batchScript(self):
        try:
            call(["cmd", "script.bat"], shell=True, stderr=STDOUT)
            batchScriptResult = check_output(["cmd", "remote.bat"], shell=True, stderr=STDOUT)
            self.textConsole.append(batchScriptResult)
            self.reportTime()
        except CalledProcessError:
            self.reportTime()
            self.textConsole.append("Failed to run script, perhaps the file is missing?") 
            
            
# this is the main application loop
if __name__ == '__main__':
    app = QApplication(sys.argv)
    frame = MainWindow()  
    frame.show()
    sys.exit(app.exec_())
 
