from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import sys
import coord_converter
from layout_colorwidget import Color

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Coordinate Converter")

        #init coord vars
        self.ddNorthing = ""
        self.ddEasting = ""
        self.ddmEasting = ""
        self.ddmNorthing = "" 

        # widgets for ddm to dd conversion        
        self.ddmEasting = QLineEdit()
        self.ddmEasting.setPlaceholderText("Latitude")
        self.ddmNorthing = QLineEdit()
        self.ddmNorthing.setPlaceholderText("Longitude")
        self.ddmBtn = QPushButton("Submit")

        self.ddmBtn.pressed.connect(self.ddm_button_pressed)

        self.ddmOutputBox = QLabel("____")
        self.ddmOutputBox.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse | Qt.TextInteractionFlag.TextSelectableByKeyboard) #flag for access by mouse and keyboard
        ddmTitle = QLabel("Converter- DDM to DD")
        
        ddmLayout = QGridLayout()
        ddmLayout.addWidget(ddmTitle, 0, 0)
        ddmLayout.addWidget(self.ddmEasting, 1, 0)
        ddmLayout.addWidget(self.ddmNorthing, 1, 1)
        ddmLayout.addWidget(self.ddmBtn, 2, 0)
        ddmLayout.addWidget(self.ddmOutputBox, 2, 1)
        

        #widgets for coord transformation
        self.epsgSource = QComboBox()
        self.epsgSource.addItems(["4326", "26918"])
        self.epsgSource.setEditable(True)
        self.epsgSource.lineEdit().setPlaceholderText("Source EPSG")
        self.epsgSource.setCurrentIndex(-1)

        self.epsgTarget = QComboBox()
        self.epsgTarget.addItems(["26918", "4326"])
        self.epsgTarget.setEditable(True)
        self.epsgTarget.setCurrentIndex(-1)
        self.epsgTarget.lineEdit().setPlaceholderText("Target EPSG")

        self.ddLat = QLineEdit()
        self.ddLat.setPlaceholderText("Latitude (DD)")
        self.ddLon = QLineEdit()
        self.ddLon.setPlaceholderText("Longitude (DD)")
        
        self.useDDMOut = QCheckBox("Use results from ddm converter?")
        self.useDDMOut.setCheckState(Qt.CheckState.Unchecked)
        self.useDDMOut.stateChanged.connect(self.use_ddm_out_checked)

        self.transformBtn = QPushButton("Submit")
        self.transformBtn.pressed.connect(self.transform_btn_pressed)

        self.transformOutputBox = QLabel("____")
        self.transformOutputBox.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse | Qt.TextInteractionFlag.TextSelectableByKeyboard)

        transformTitle = QLabel("Coordinate Transformation")


        transformLayout = QGridLayout()
        transformLayout.addWidget(transformTitle, 0, 0)
        transformLayout.addWidget(self.useDDMOut, 1, 0)
        transformLayout.addWidget(self.ddLat, 2, 0)
        transformLayout.addWidget(self.ddLon, 2, 1)
        transformLayout.addWidget(self.epsgSource, 3, 0)
        transformLayout.addWidget(self.epsgTarget, 3, 1)
        transformLayout.addWidget(self.transformBtn, 4, 0)
        transformLayout.addWidget(self.transformOutputBox, 4, 1)

        layout = QVBoxLayout()
        layout.addLayout(ddmLayout)
        layout.addLayout(transformLayout)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        

    def ddm_button_pressed(self):
        easting = self.ddmEasting.text()
        northing = self.ddmNorthing.text()
        
        self.ddEasting = coord_converter.Conversions.ddm_to_dd(easting)
        self.ddNorthing = coord_converter.Conversions.ddm_to_dd(northing)

    
        self.ddmOutputBox.setText(str(self.ddEasting) + ' ' + str(self.ddNorthing))
        print(self.ddEasting, self.ddNorthing)

    def use_ddm_out_checked(self, s):
        print(s == Qt.CheckState.Checked.value)
        if s == Qt.CheckState.Checked.value:
            self.ddLat.setText(str(self.ddNorthing))
            self.ddLon.setText(str(self.ddEasting))
            print(self.ddNorthing)
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