import os

import re
from json import loads

from qtpy import QtWidgets

import numpy as np

import pyvista as pv
from pyvistaqt import QtInteractor, MainWindow

class VtkScreen(QtWidgets.QDialog):
    def __init__(self,current_project_directory):
        QtWidgets.QDialog.__init__(self)
        self.current_project_directory=current_project_directory
        self.extract_Vtk()
        self.init_ui()
        
    def init_ui(self, show=True):
        # Add your configuration editing widgets here
        self.layout=QtWidgets.QVBoxLayout()
        self.hlayout=QtWidgets.QHBoxLayout()
        self.ComboSecond=QtWidgets.QComboBox()
        self.button=QtWidgets.QPushButton(text="Plot")
        self.button.clicked.connect(self.open_3D)
        self.plotter = QtInteractor(self)
        
        self.ComboSecond.addItems(self.times)
        self.hlayout.addWidget(self.ComboSecond)
        self.hlayout.addWidget(self.button)
        self.layout.addLayout(self.hlayout)
        self.layout.addWidget(self.plotter.interactor)

        self.setLayout(self.layout)
        if show:
            self.show()
    def extract_Vtk(self):
        dir=os.listdir(os.path.join(self.current_project_directory, 'VTK'))

        #exracting vtk file names
        for i in dir:
            if re.match(".*vtm.series",i):
                vtk_series_file=str(os.path.join(self.current_project_directory, 'VTK'))+"\\"+str(i)
                break
        with open(vtk_series_file ,"r") as vtk_file :
            vtk_series_txt=vtk_file.read()
        #print(vtk_series_txt)
        vtk_series_txt=loads(vtk_series_txt)
        vtk_series_txt=list(vtk_series_txt["files"])
        self.times=[]
        self.names=[]
        for i in vtk_series_txt:
            self.names.append(i["name"])
            self.times.append(str(i["time"]))
        print(self.times)
        #print(vtk_series_txt)
    def open_3D(self):
        
        # OpenFOAM tarafından üretilen VTK dosyasının yolu
        vtk_file_path = str(os.path.join(self.current_project_directory, 'VTK'))+"\\"+self.names[self.times.index(self.ComboSecond.currentText())]
        # VTK dosyasını oku
        mesh = pv.read(vtk_file_path)

        # Paraview tarayıcısını aç ve mesh'i göster
        self.plotter.add_mesh(mesh)

