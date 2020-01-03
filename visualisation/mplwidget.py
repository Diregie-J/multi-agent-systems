# mplwidget.py

import matplotlib
import pandas as pd
matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.offsetbox import AnchoredOffsetbox, TextArea, HPacker, VPacker
from PyQt5 import QtWidgets
from matplotlib.figure import Figure
from model import Model
from zipfile import ZipFile

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

    def defaultEnergyPlot(self, data, save):
        self.clear()
        energy = data.filter(regex="Energy$", axis=1)
        energy.apply(lambda x: self.canvas.axes.scatter(x.index+1, x, c='g', marker="x"))
        energy["Average"] = data["Average Energy"]
        self.canvas.axes.plot(data["CurrentDay"], energy["Average"], color='blue')
        self.canvas.axes.set_ylim(0,100)
        ybox1 = TextArea("Energy: ", textprops=dict(color="k", rotation=90,ha='left',va='bottom'))
        ybox2 = TextArea("Individual/",     textprops=dict(color="g", rotation=90,ha='left',va='bottom'))
        ybox3 = TextArea("Average", textprops=dict(color="b", rotation=90,ha='left',va='bottom'))

        ybox = VPacker(children=[ybox3, ybox2, ybox1],align="bottom", pad=0, sep=2)

        anchored_ybox = AnchoredOffsetbox(loc=8, child=ybox, pad=0., frameon=False, bbox_to_anchor=(-0.08, 0.3), 
                                  bbox_transform=self.canvas.axes.transAxes, borderpad=0.)
        self.canvas.axes.add_artist(anchored_ybox)
        self.canvas.axes.set_xlabel("Day")
        self.canvas.axes.set_title('Average Agent Energy with Number of Dead Agents')

        deadAxes = self.canvas.axes.twinx()
        dead = data.filter(regex="Alive$", axis=1)
        dead["Number Dead"] = dead.isnull().sum(axis=1)
        deadAxes.plot(data["CurrentDay"], dead["Number Dead"], color='red')
        deadAxes.set_ylabel("Number of Dead Agents", color='red')
        deadAxes.set_ylim(0)

        if save:
            fig = self.canvas.fig
            return fig
        else:
            self.canvas.draw()

    def defaultEnergyBoxPlot(self, data, save):
        self.clear()

        filtered_col = []

        energy = data.filter(regex="Energy$", axis=1)
        for x in range(len(energy.T.columns)):
            col = energy.T[x]
            filtered_col.append(col.dropna())

        self.canvas.axes.boxplot(filtered_col, vert=True, patch_artist=True)

        self.canvas.axes.set_title('Agent Energy Distribution')

        # adding horizontal grid lines
        self.canvas.axes.yaxis.grid(True)
        self.canvas.axes.set_xlabel('Day')
        self.canvas.axes.set_ylabel('Agent Energy')
        self.canvas.axes.set_ylim(0, 100)

        if save:
            return self.canvas.fig
        else:
            self.canvas.draw()

    def defaultEgotismPlot(self, data, save):
        self.clear()
        self.canvas.axes.plot(data["CurrentDay"], data["Average Egotism"], color='blue')
        self.canvas.axes.set_ylim(0,1)
        self.canvas.axes.set_xlabel("Day")
        self.canvas.axes.set_ylabel("Egotism")
        self.canvas.axes.set_title("Average Agent Egotism")
        
        if save:
            return self.canvas.fig
        else:
            self.canvas.draw()

    def defaultSusceptibilityPlot(self, data, save):
        self.clear()
        self.canvas.axes.plot(data["CurrentDay"], data["Average Susceptibility"], color='blue')
        self.canvas.axes.set_ylim(0,1)
        self.canvas.axes.set_xlabel("Day")
        self.canvas.axes.set_ylabel("Susceptibility")
        self.canvas.axes.set_title("Average Agent Susceptibility")

        if save:
            return self.canvas.fig
        else:
            self.canvas.draw()

    def defaultIdealismPlot(self, data, save):
        self.clear()
        self.canvas.axes.plot(data["CurrentDay"], data["Average Idealism"], color='blue')
        self.canvas.axes.set_ylim(0,1)
        self.canvas.axes.set_xlabel("Day")
        self.canvas.axes.set_ylabel("Idealism")
        self.canvas.axes.set_title("Average Agent Idealism")

        if save:
            return self.canvas.fig
        else:
            self.canvas.draw()

    def defaultFairnessPlot(self, data, save):
        self.clear()
        filtered_col = []

        fairness = data.filter(regex="Fairness$", axis=1)
        for x in range(len(fairness.T.columns)):
            col = fairness.T[x]
            filtered_col.append(col.dropna())

        self.canvas.axes.boxplot(filtered_col, vert=True, patch_artist=True)

        self.canvas.axes.set_title('Agent Fairness Distribution')

        # adding horizontal grid lines
        self.canvas.axes.yaxis.grid(True)
        self.canvas.axes.set_xlabel('Day')
        self.canvas.axes.set_ylabel('Agent Fairness')

        if save:
            return self.canvas.fig
        else:
            self.canvas.draw()

    def clear(self):
        self.canvas.fig.clear(keep_observers=True)
        self.canvas.axes = self.canvas.fig.add_subplot(111)

    def exportAll(self, data, fileName):
        plotNames = []
        with ZipFile(fileName, "w") as zip:
            fig = ((self.defaultEnergyPlot(data, True), "averageEnergy.png"))
            fig[0].savefig(fig[1])
            zip.write(fig[1])
            plotNames.append(fig[1])

            fig = ((self.defaultEnergyBoxPlot(data, True), "boxPlotEnergy.png"))
            fig[0].savefig(fig[1])
            zip.write(fig[1])
            plotNames.append(fig[1])

            fig = ((self.defaultEgotismPlot(data, True), "egotism.png"))
            fig[0].savefig(fig[1])
            zip.write(fig[1])
            plotNames.append(fig[1])

            fig = ((self.defaultSusceptibilityPlot(data, True), "susceptibility.png"))
            fig[0].savefig(fig[1])
            zip.write(fig[1])
            plotNames.append(fig[1])

            fig = ((self.defaultIdealismPlot(data, True), "idealism.png"))
            fig[0].savefig(fig[1])
            zip.write(fig[1])
            plotNames.append(fig[1])

            fig = ((self.defaultFairnessPlot(data, True), "fairness.png"))
            fig[0].savefig(fig[1])
            zip.write(fig[1])
            plotNames.append(fig[1])
        self.clear()
        self.canvas.draw()
        return plotNames
