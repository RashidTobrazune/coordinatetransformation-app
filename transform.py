# -*- coding: utf-8 -*-
"""
Created on Fri May  3 09:57:14 2024

@author: Admin
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox, QLabel, QLineEdit, QPushButton
import pyproj

class CoordinateTransformationApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(' Rashid Coordinate Transformation App')
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.lat_label = QLabel('Latitude/Northing:')
        layout.addWidget(self.lat_label)

        self.lat_input = QLineEdit()
        layout.addWidget(self.lat_input)

        self.lon_label = QLabel('Longitude/Easting:')
        layout.addWidget(self.lon_label)

        self.lon_input = QLineEdit()
        layout.addWidget(self.lon_input)

        self.coord_type = QComboBox()
        self.coord_type.addItems(['WGS 84 to Ghana Meter Grid', 'Ghana Meter Grid to WGS 84',
                                  'WGS 84 to Ghana National Grid', 'Ghana National Grid to WGS 84'])
        layout.addWidget(self.coord_type)

        self.convert_button = QPushButton('Convert')
        self.convert_button.clicked.connect(self.convert_coordinates)
        layout.addWidget(self.convert_button)

        self.result_label = QLabel()
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def convert_coordinates(self):
        latitude = float(self.lat_input.text())
        longitude = float(self.lon_input.text())
        transformation = self.coord_type.currentText()

        if transformation == 'WGS 84 to Ghana Meter Grid':
            result = self.wgs_to_gmg(latitude, longitude)
        elif transformation == 'Ghana Meter Grid to WGS 84':
            result = self.gmg_to_wgs(latitude, longitude)
        elif transformation == 'WGS 84 to Ghana National Grid':
            result = self.wgs_to_gng(latitude, longitude)
        elif transformation == 'Ghana National Grid to WGS 84':
            result = self.gng_to_wgs(latitude, longitude)

        self.result_label.setText(result)

    def wgs_to_gmg(self, latitude, longitude):
        transformer = pyproj.Transformer.from_crs(4326, 25000)
        gmg_values = transformer.transform(latitude, longitude)
        return f"Ghana Meter Grid: Easting = {gmg_values[0]}, Northing = {gmg_values[1]}"

    def gmg_to_wgs(self, latitude, longitude):
        transformer = pyproj.Transformer.from_crs(25000, 4326)
        wgs_values = transformer.transform(latitude, longitude)
        return f"WGS 84: Latitude = {wgs_values[0]}, Longitude = {wgs_values[1]}"

    def wgs_to_gng(self, latitude, longitude):
        transformer = pyproj.Transformer.from_crs(4326, 2136)
        gng_values = transformer.transform(latitude, longitude)
        return f"Ghana National Grid: Easting = {gng_values[0]}, Northing = {gng_values[1]}"

    def gng_to_wgs(self, latitude, longitude):
        transformer = pyproj.Transformer.from_crs(2136, 4326)
        wgs_values = transformer.transform(latitude, longitude)
        return f"WGS 84: Latitude = {wgs_values[0]}, Longitude = {wgs_values[1]}"

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CoordinateTransformationApp()
    ex.show() 
    sys.exit(app.exec_())
