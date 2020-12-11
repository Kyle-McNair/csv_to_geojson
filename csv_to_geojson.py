#########################################
#### csv_to_geojson.py               ####
#### Author: Kyle McNair             ####
#### Last Updated: December 10, 2020 ####
#########################################

# pandas and json needed
import sys
import os
import ctypes
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pandas as pd
import json

# setGeometry(x, y, width, height)

class GeoJsonConverter(QWidget):
    def __init__(self, parent = None):
        super().__init__()
        path = os.path.dirname(__file__)
        self.setWindowIcon(QIcon(path + '\Icon.png')) 
        self.setWindowTitle('CSV XY COORDINATES TO GEOJSON FILE')
        self.setGeometry(600,200,600,300)
        self.setStyleSheet("background-color: #141414")
        self.createUI()
        self.show()

    def createUI(self):
        self.fileLabel = QLabel(self)
        self.fileLabel.setText("Open your csv file")
        self.fileLabel.move(50,10)
        self.fileLabel.setFont(QFont('Arial',10))
        self.fileLabel.setStyleSheet("color: white")

        self.filePath = QLineEdit(self)
        self.filePath.move(50, 30)
        self.filePath.resize(440, 20)
        self.filePath.setStyleSheet("background-color: white; color: black")

        self.browse = QPushButton(self)
        self.browse.setText("Browse")
        self.browse.move(500, 30)
        self.browse.resize(50,20)
        self.browse.setStyleSheet("QPushButton{background-color: #141414; color: white; border: 1px solid white; font-weight: 600}""QPushButton::hover""{""background-color: #ffb327; color: black""}")

        self.xLabel = QLabel(self)
        self.xLabel.setText("Select X coordinate (Longitude) field: ")
        self.xLabel.setFont(QFont('Arial',10))
        self.xLabel.setStyleSheet("color: white")
        self.xLabel.move(50, 70)
        self.xPick = QComboBox(self)
        self.xPick.move(270,70)
        self.xPick.resize(275,20)
        self.xPick.setStyleSheet("background-color: white; color: black")

        self.yLabel = QLabel(self)
        self.yLabel.setText("Select Y coordinate (Latitude) field: ")
        self.yLabel.setFont(QFont('Arial',10))
        self.yLabel.setStyleSheet("color: white")
        self.yLabel.move(50,110)
        self.yPick = QComboBox(self)
        self.yPick.move(270,110)
        self.yPick.resize(275,20)
        self.yPick.setStyleSheet("background-color: white; color: black")

        self.browse.clicked.connect(self.browser)
        

        self.outputLabel = QLabel(self)
        self.outputLabel.setText("Select file location and name:  ")
        self.outputLabel.setFont(QFont('Arial',10))
        self.outputLabel.move(50,150)
        self.outputLabel.setStyleSheet("color: white")
        self.output = QLineEdit(self)
        self.output.move(230,150)
        self.output.resize(260,20)
        self.output.setStyleSheet("background-color: white; color: black")

        self.xPick.activated.connect(lambda: self.columnCheck("X"))
        self.yPick.activated.connect(lambda: self.columnCheck("Y"))

        self.outputBrowse = QPushButton(self)
        self.outputBrowse.setText("Browse")
        self.outputBrowse.move(500, 150)
        self.outputBrowse.resize(50,20)
        self.outputBrowse.setStyleSheet("QPushButton{background-color: #141414; color: white; border: 1px solid white; font-weight: 600}""QPushButton::hover""{""background-color: #ffb327; color: black""}")
        self.outputBrowse.clicked.connect(self.outputBrowser)

        self.convertButton = QPushButton(self)
        self.convertButton.setText('Convert to geojson!')
        self.convertButton.setStyleSheet("QPushButton{background-color: #141414; color: white; border: 1px solid white; font-weight: 600}""QPushButton::hover""{""background-color: #ffb327; color: black""}")
        self.convertButton.setGeometry(50,190,500,25)
        self.convertButton.clicked.connect(self.geojson)

        self.prog_bar = QProgressBar(self)
        self.prog_bar.setGeometry(50, 240, 500, 30)
        self.prog_bar.setValue(0)
        self.prog_bar.setAlignment(Qt.AlignCenter)
        self.prog_bar.setStyleSheet("QProgressBar{background-color: #141414; color: white; border: 1px solid white;font-weight: 600}")

    def browser(self):
        self.fileName = QFileDialog.getOpenFileName(parent=self, caption='Find csv File...',filter='*.csv')
        if self.fileName:
            self.filePath.setText(self.fileName[0])
        self.csv = pd.read_csv(self.fileName[0])
        self.df = pd.DataFrame(self.csv)
        for d in self.df.columns:
            self.xPick.addItem(d)
            self.yPick.addItem(d)

    def outputBrowser(self):
        self.outputName = QFileDialog.getSaveFileName(parent=self, caption='Select file location to save geojson...')
        if self.outputName:
            self.output.setText(self.outputName[0])

    def columnCheck(self, field):
        self.field = field
        if self.field == "X":
            self.xCheck = self.xPick.currentText()
            print(self.xCheck)
            self.xList = ["X","x","Long","Longitude","long","longitude","Easting","easting"]
            if self.xCheck not in self.xList:
                self.xWarning = QMessageBox()
                self.xWarning.setIcon(QMessageBox.Warning)
                self.xWarning.setText("WARNING: This is not a X/Longitude Field!")
                self.xWarning.setWindowTitle("WARNING")
                self.xWarning.setStyleSheet("background-color: #141414; color: white")
                self.xWarning.exec_()

        if self.field == "Y":
            self.yCheck = self.yPick.currentText()
            self.yList = ["Y","y","Lat","Latitude","lat","latitude","Northing","northing"]
            if self.yCheck not in self.yList:
                self.yWarning = QMessageBox()
                self.yWarning.setIcon(QMessageBox.Warning)
                self.yWarning.setText("WARNING: This is not a Y/Latitude Field!")
                self.yWarning.setWindowTitle("WARNING")
                self.yWarning.setStyleSheet("background-color: #141414; color: white")
                self.yWarning.exec_()

    # geojson function converts pandas data frame data to geojson format
    def geojson(self):
        self.prog_bar.setStyleSheet("QProgressBar{background-color: #141414; border: 1px solid white;font-weight: 600}""QProgressBar::chunk""{""background-color: #ffb327; color: black""}")
        self.xfield = self.xPick.currentText()
        self.yfield = self.yPick.currentText()
        fc = {"type":"FeatureCollection"}
        col = []
        for c in self.df.columns:
            col.append(c)
        features = []
        properties = {}
        count = 0
        for index, row in self.df.iterrows():
            count += 1
            self.prog_bar.setValue(count)
            X = row[self.xfield]
            Y = row[self.yfield]
            coordinates = [X,Y]
            for c in col:
                properties.update({c:row[c]})
            data_dict = {"type":"Feature","geometry":{"type":"Point","coordinates":coordinates},"properties":properties}
            features.append(data_dict)
        fc.update({"features":features})
        geojson = json.dumps(fc)
        with open(self.output.text() + '.json','w') as geojson_file:
            geojson_file.write(geojson)
        geojson_file.close()

if __name__ == '__main__':
    path = os.path.dirname(__file__)

    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    trayIcon = QSystemTrayIcon(QIcon(path+'\Icon.png'), parent = app) 
    trayIcon.setToolTip("csv to geojson")
    trayIcon.show()

    taskbarApproval = 'mycompany.myproduct.subproduct.version'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(taskbarApproval)
    
    ui = GeoJsonConverter()

    sys.exit(app.exec_())