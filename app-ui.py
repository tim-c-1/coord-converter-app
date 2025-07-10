from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import sys, os
import coord_converter

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
        tabBar.setTabPosition(QTabWidget.TabPosition.West)
        tabBar.setMovable(False)

        tabBar.addTab(ddmConvert(), "DDM to DD")
        tabBar.addTab(transformCoords(), "Transform Coords")

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()