import os
import requests
import time
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QWidget, QPushButton, QProgressBar, QLabel, QLineEdit, QMessageBox
from ManageCodeAnalysis import ManageCodeAnalysis

class ProSyWis_GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initMe()
    def initMe(self):
        myFont=QFont()
        myFont.setBold(True)
        self.setWindowIcon(QIcon("logo_hbrs.png"))
        self.resize(400, 300)
        self.setWindowTitle("ProSyWis")
        self.buttonAssociationsImport = QPushButton("Association Import", self)
        self.buttonAssociationsImport.clicked.connect(self.pushAssociationsImport)
        self.buttonAssociationsImport.setGeometry(QtCore.QRect(30, 35, 141, 28))
        buttonCamundaEngine = QPushButton("Camunda Engine",self)
        buttonCamundaEngine.setGeometry(QtCore.QRect(222, 35, 151, 28))
        buttonCamundaEngine.clicked.connect(self.pushCamundaEngine)
        self.progressBar = QProgressBar (self)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setGeometry(QtCore.QRect(30, 199, 351, 23))
        self.progressBar.setProperty("value", 0)
        buttonBox = QtWidgets.QDialogButtonBox(self)
        buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        buttonBox.setOrientation(QtCore.Qt.Horizontal)
        buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        buttonBox.setEnabled(True)
        buttonBox.rejected.connect(self.close)
        buttonBox.accepted.connect(self.close)
        linkLabel = QLabel (self)
        linkLabel.setGeometry(QtCore.QRect(10, 10, 35, 16))
        linkLabel.setObjectName("linkLabel")
        linkLabel.setText("Links:")
        linkLabel.setFont(myFont)
        codeAnalysisLabel = QLabel (self)
        codeAnalysisLabel.setText("Code Analysis:")
        codeAnalysisLabel.setFont(myFont)
        codeAnalysisLabel.setGeometry(QtCore.QRect(10, 80, 95, 16))
        urlLabel = QLabel (self)
        urlLabel.setGeometry(QtCore.QRect(30, 112, 55, 16))
        urlLabel.setObjectName("linkLabel")
        urlLabel.setText("Git-URL:")
        self.analyzeCodeButton = QPushButton ("Analyze Code",self)
        self.analyzeCodeButton.setGeometry(QtCore.QRect(150, 150, 101, 28))
        self.analyzeCodeButton.clicked.connect(self.pushAnalyzeCodeButton)
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(80, 110, 291, 22))
        self.lineEdit.setObjectName("lineEdit")


    def pushAssociationsImport(self):
        os.startfile('http://localhost:8080/')
    def pushCamundaEngine(self):
        print ("Camunda gedrückt")
        os.startfile('http://localhost:8081/camunda/app/cockpit/default/#/login/')

    def pushAnalyzeCodeButton (self):
        link =self.lineEdit.displayText()
        self.progressBar.setProperty("value", 0)
        try:
            response = requests.get("https://www.google.de/")
            try:
             response = requests.get(link)
             try:
                 time.sleep(1);
                 managerepdata = ManageCodeAnalysis()
                 managerepdata.getSourceCode(link)
                 self.progressBar.setProperty("value", 20)
                 time.sleep(6);
                 managerepdata.getGitInfo(link)
                 try:
                     self.progressBar.setProperty("value", 40)
                     time.sleep(1);
                     managerepdata.analyseDependencies()
                     self.progressBar.setProperty("value", 60)
                     time.sleep(1);
                     managerepdata.persData()
                     self.progressBar.setProperty("value", 80)
                     time.sleep(1);
                     managerepdata.persPatternData()
                     self.progressBar.setProperty("value", 100)
                     buttonSuccess = QMessageBox.question (self,'Success', "Code Analysis successful!",
                                              QMessageBox.Ok , QMessageBox.Ok)
                 except:
                     msgBoxError =QMessageBox.question (self, 'Error', "Error while analyzing the Repository!", QMessageBox.Ok , QMessageBox.Ok)

             except Exception as e:
                 print (e)
                 msgBoxGit = QMessageBox.question (self,'Warning', "No Permission on given Git Repository! Please check again!",
                                                   QMessageBox.Ok , QMessageBox.Ok)



            except:
                msgBoxURL = QMessageBox.question (self,'Warning', "URL not reachable! Please check again!",
                                        QMessageBox.Ok , QMessageBox.Ok)

        except:
            msgBoxNetwork = QMessageBox.question (self,'Warning', "Network not available! Please check your Connection!",
                                                QMessageBox.Ok , QMessageBox.Ok)







import sys
app = QtWidgets.QApplication(sys.argv)
w= ProSyWis_GUI()
w.show()
sys.exit(app.exec_())
