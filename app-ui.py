"""
    This Coordinate Conversion application offers multiple tools to 
    convert and transform coordinate formats and projections.
    Source code is available on https://github.com/tim-c-1/coord-converter-app.

    Copyright (C) 2025 Timothy Cooney

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import sys, os
import coord_converter
import pandas as pd

basedir = os.path.dirname(__file__)

try:
    from ctypes import windll #only exists on windows
    myappid = 'com.github.tim-c-1.coordconverter.version1'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Coordinate Converter")
        self.setWindowIcon(QIcon(os.path.join(basedir, 'icons/globe-green.png')))

        tabBar = QTabWidget()
        tabBar.setTabPosition(QTabWidget.TabPosition.North)
        tabBar.setMovable(False)

        tabBar.addTab(ddmConvert(), "DDM to DD")
        tabBar.addTab(transformCoords(), "Transform Coords")
        tabBar.addTab(bulkConversion(), "Convert in bulk")

        self.setCentralWidget(tabBar)
        

class ddmConvert(QWidget):
    def __init__(self):
        super().__init__()

        #init coord vars
        ddmConvert.ddNorthing = ""
        ddmConvert.ddEasting = ""
        self.ddmEasting = ""
        self.ddmNorthing = "" 

        # widgets for ddm to dd conversion        
        self.ddmEasting = QLineEdit()
        self.ddmEasting.setPlaceholderText("Latitude (DDM)")
        self.ddmEasting.setToolTip("Latitude in degree decimal minutes. Must include N/S/E/W. \nEx. 39 17.398N")
        self.ddmNorthing = QLineEdit()
        self.ddmNorthing.setPlaceholderText("Longitude (DDM)")
        self.ddmNorthing.setToolTip("Longitude in degree decimal minutes. Must include N/S/E/W. \nEx. 76 36.471W")
        self.ddmBtn = QPushButton("Submit")

        self.ddmBtn.pressed.connect(self.ddm_button_pressed)

        self.ddmOutputBox = QLabel("____")
        self.ddmOutputBox.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse | Qt.TextInteractionFlag.TextSelectableByKeyboard) #flag for access by mouse and keyboard
        ddmTitle = QLabel("DDM to DD Converter")
        
        font = ddmTitle.font()
        font.setPointSize(22)
        font.setFamily("Calibri")
        ddmTitle.setFont(font)
        ddmTitle.setMaximumHeight(30)
                
        ddmLayout = QGridLayout()
        ddmLayout.addWidget(ddmTitle, 0, 0, 1, 2)
        ddmLayout.addWidget(self.ddmEasting, 1, 0)
        ddmLayout.addWidget(self.ddmNorthing, 1, 1)
        ddmLayout.addWidget(self.ddmBtn, 2, 0)
        ddmLayout.addWidget(self.ddmOutputBox, 2, 1)

        ddmLayout.setContentsMargins(5,0,0,0)

        self.setLayout(ddmLayout)

    def ddm_button_pressed(self):
        easting = self.ddmEasting.text()
        northing = self.ddmNorthing.text()
        
        ddmConvert.ddEasting = coord_converter.Conversions.ddm_to_dd(easting)
        ddmConvert.ddNorthing = coord_converter.Conversions.ddm_to_dd(northing)

    
        self.ddmOutputBox.setText(str(ddmConvert.ddEasting) + ' ' + str(ddmConvert.ddNorthing))
        print(ddmConvert.ddEasting, ddmConvert.ddNorthing)

class transformCoords(QWidget):
    def __init__(self):
        super().__init__()

        #init coord vars
        self.ddLat = ""
        self.ddLon = ""

        #widgets for coord transformation
        self.epsgSource = QComboBox()
        self.epsgSource.addItems(["4326", "26918"])
        self.epsgSource.setEditable(True)
        self.epsgSource.setCurrentIndex(-1)
        self.epsgSource.lineEdit().setPlaceholderText("Source EPSG")
        self.epsgSource.setToolTip("Not sure what EPSG code you need? Check https://epsg.io")

        self.epsgTarget = QComboBox()
        self.epsgTarget.addItems(["26918", "4326"])
        self.epsgTarget.setEditable(True)
        self.epsgTarget.setCurrentIndex(-1)
        self.epsgTarget.lineEdit().setPlaceholderText("Target EPSG")
        self.epsgTarget.setToolTip("Not sure what EPSG code you need? Check https://epsg.io")

        self.ddLat = QLineEdit()
        self.ddLat.setPlaceholderText("Latitude (DD)")
        self.ddLat.setToolTip("Latitude in decimal degrees. Ex. 39.285016")
        self.ddLon = QLineEdit()
        self.ddLon.setPlaceholderText("Longitude (DD)")
        self.ddLon.setToolTip("Longitude in decimal degrees. Ex. -76.612080")
        
        self.useDDMOut = QCheckBox("Use results from ddm converter?")
        self.useDDMOut.setToolTip("This will use any results created in the DDM to DD tab. It will clear your entries when unselected.")
        self.useDDMOut.setCheckState(Qt.CheckState.Unchecked)
        self.useDDMOut.stateChanged.connect(self.use_ddm_out_checked)

        self.transformBtn = QPushButton("Submit")
        self.transformBtn.pressed.connect(self.transform_btn_pressed)

        self.transformOutputBox = QLabel("____")
        self.transformOutputBox.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse | Qt.TextInteractionFlag.TextSelectableByKeyboard)

        transformTitle = QLabel("Coordinate Transformation")
        font = transformTitle.font()
        font.setPointSize(22)
        font.setFamily("Calibri")
        transformTitle.setFont(font)
        transformTitle.setMaximumHeight(30)

        transformLayout = QGridLayout()
        transformLayout.addWidget(transformTitle, 0, 0, 1, 2)
        transformLayout.addWidget(self.useDDMOut, 1, 0, 1, 2)
        transformLayout.addWidget(self.ddLat, 2, 0)
        transformLayout.addWidget(self.ddLon, 2, 1)
        transformLayout.addWidget(self.epsgSource, 3, 0)
        transformLayout.addWidget(self.epsgTarget, 3, 1)
        transformLayout.addWidget(self.transformBtn, 4, 0)
        transformLayout.addWidget(self.transformOutputBox, 4, 1)

        transformLayout.setContentsMargins(5,0,0,0)

        self.setLayout(transformLayout)

    
    def use_ddm_out_checked(self, s):
        print(s == Qt.CheckState.Checked.value)
        if s == Qt.CheckState.Checked.value:
            self.ddLat.setText(str(ddmConvert.ddNorthing))
            self.ddLon.setText(str(ddmConvert.ddEasting))
            print(ddmConvert.ddNorthing)
        else:
            self.ddLat.clear()
            self.ddLon.clear()
        

    def transform_btn_pressed(self):
        lon = float(self.ddLon.text())
        lat = float(self.ddLat.text())
        epsgSource = int(self.epsgSource.currentText())
        epsgTarget = int(self.epsgTarget.currentText())
        
        # print("lon: ", lon, "\nlat: ", lat, "\nepsgsource: ", epsgSource, "\nepsgtarget: ", epsgTarget)

        transformedCoords = coord_converter.Conversions.transform_coords(lon, lat, epsgSource, epsgTarget)
        self.transformOutputBox.setText(str(transformedCoords))

class bulkConversion(QWidget):
    def __init__(self):
        super().__init__()

        # create layout with a selector dialog for a text/xyz file
        # user defined easting/northing columns
        # user defined output file and path
        # output new text file with transformed coords
        # option for keeping old coords in column and appending new or replacing old with new
        # option for separator (comma, space, tab)
    
        # input file selection
        self.inputFileBtn = QPushButton("Select input file")
        self.inputFileBtn.pressed.connect(self.input_file_btn_pressed)
        self.inputFileLabel = QLabel("___")
        self.inputFileBtn.setToolTip("select a file with your x,y information to transform.\nhaving column names is helpful.")

        # delimiter selection
        delimLabel = QLabel("Select delimiter")
        self.useCSV = QRadioButton("csv")
        self.useSpace = QRadioButton("space")
        self.useTab = QRadioButton("tab")

        self.useCSV.setChecked(True)

        radioGroup = QVBoxLayout()
        radioGroup.addWidget(delimLabel)
        radioGroup.addWidget(self.useCSV)
        radioGroup.addWidget(self.useSpace)
        radioGroup.addWidget(self.useTab)

        # x,y column selection
        self.easting = QComboBox()
        self.northing = QComboBox()
        self.easting.setPlaceholderText("easting")
        self.easting.setToolTip("select which column contains the easting information")
        self.northing.setPlaceholderText("northing")
        self.northing.setToolTip("select which column contains the northing information")

        columnGroup = QHBoxLayout()
        columnGroup.addWidget(self.easting)
        columnGroup.addWidget(self.northing)

        # page layout
        layout = QGridLayout()
        layout.addWidget(self.inputFileLabel, 0, 1, 1, 1)
        layout.addWidget(self.inputFileBtn, 0, 0, 1, 1)
        layout.addLayout(radioGroup, 1, 0, 1, 1)
        layout.addLayout(columnGroup, 2, 0, 1, 2)
        self.setLayout(layout)

    def input_file_btn_pressed(self):
        inputFile = QFileDialog().getOpenFileUrl(self, "Select File", filter="Text files (*.txt *.csv *.xyz);; All Files(*)") #push towards txt files, but allow any file selection
        fpath = inputFile[0].toString().strip("/") #remove leading slash from path

        if self.useCSV.isChecked():
            print("use csv")
            try:
                df = pd.read_csv(fpath)
                self.inputFileLabel.setText(inputFile[0].fileName())

                self.easting.addItems(df.columns)
                self.northing.addItems(df.columns)
                print(df)
            except:
                print("read failed")
                self.inputFileLabel.setText("file import failed")
                pass
        elif self.useSpace.isChecked():
            print("use space")
            try:
                df = pd.read_table(fpath, sep='\s+')
                self.inputFileLabel.setText(inputFile[0].fileName())

                self.easting.addItems(df.columns)
                self.northing.addItems(df.columns)
                print(df)
            except:
                print("read failed")
                self.inputFileLabel.setText("file import failed")
                pass
        elif self.useTab.isChecked():
            print("use tab")
            try:
                df = pd.read_table(fpath, '/t')
                self.inputFileLabel.setText(inputFile[0].fileName())

                self.easting.addItems(df.columns)
                self.northing.addItems(df.columns)
                print(df)
            except:
                print("read failed")
                self.inputFileLabel.setText("file import failed")
                pass
            
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()