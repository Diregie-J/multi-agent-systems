# mplwidget.py

import matplotlib
import pandas as pd
matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5 import QtWidgets
from matplotlib.figure import Figure
from model import Model

class MplCanvas(Canvas):
    def __init__(self):
        self.fig = Figure()
        self.axes = self.fig.add_subplot(111)
        Canvas.__init__(self, self.fig)
        Canvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        Canvas.updateGeometry(self)

class MplWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.canvas = MplCanvas()
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.vbl = QtWidgets.QVBoxLayout()
        self.vbl.addWidget(self.canvas)
        self.vbl.addWidget(self.toolbar)
        self.setLayout(self.vbl)

    def plot(self, data, x, y):
        # do stuff to fig or axes to plot things
        self.canvas.draw()

    def defaultEnergyPlot(self, data):
        self.canvas.fig.clear(keep_observers=True)
        self.canvas.axes = self.canvas.fig.add_subplot(111)
        energy = data.filter(regex="Energy$", axis=1)

        energy.apply(lambda x: self.canvas.axes.scatter(x.index, x, c='g'))

        #energy["Average"] = data["Average Energy"]
        
        #for x in range(numAgents):
        #    columnTitle = str(x) + "Energy"
        #    energy.plot(kind="scatter", x="CurrentDay", y=columnTitle, ax=self.axes)


        self.canvas.draw()