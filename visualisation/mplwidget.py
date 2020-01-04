# mplwidget.py

import matplotlib
import pandas as pd
import numpy as np
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

    def defaultTestPlot(self, data, save):
        self.defaultShelterRulePie(data, False)

    def defaultShelterRulePie(self, data, save):
        self.clear()

        labels = ['Random', 'Oligarchy', 'Meritocracy', 'Socialism']
        colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']
        explode = (0.05,0.05,0.05,0.05)
        sizes = []
        occurences = data["CurrentShelterRule"].value_counts()

        try:
            sizes.append(occurences.loc["Random"])
        except:
            temp = 0
        sizes.append(temp)

        try:
            temp = occurences.loc["Oligarchy"]
        except:
            temp = 0
        sizes.append(temp)

        try:
            temp = occurences.loc["Meritocracy"]
        except:
            temp = 0
        sizes.append(temp)

        try:
            temp = occurences.loc["Socialism"]
        except:
            temp = 0
        sizes.append(temp)
        
        self.canvas.axes.pie(sizes, colors = colors, labels=labels, autopct='%1.1f%%', startangle=90, pctdistance=0.85, explode = explode)
        centre_circle = matplotlib.patches.Circle((0,0),0.70,fc='white')
        self.canvas.axes.add_patch(centre_circle)
        self.canvas.axes.axis('equal')  
        self.canvas.fig.tight_layout()

        if save:
            return self.canvas.fig
        else:
            self.canvas.draw()


    def defaultActivityPlot(self, data, save):
        self.clear()

        activity = data.filter(regex="Today'sActivity$", axis=1)
        
        none = []
        hunting = []
        building = []

        for x in range(len(activity.T.columns)):
            occurences = activity.T[x].value_counts()
            
            try:
                temp = occurences.loc["NONE"]
            except:
                temp = 0
            none.append(temp)

            try:
                temp = occurences.loc["HUNTING"]
            except:
                temp = 0
            hunting.append(temp)

            try:
                temp = occurences.loc["BUILDING"]
            except:
                temp = 0
            building.append(temp)

        noneBar = self.canvas.axes.bar(data["CurrentDay"], none, 0.85, color="#ff9999")
        huntingBar = self.canvas.axes.bar(data["CurrentDay"], hunting, 0.85, bottom=none, color="#99ff99")
        buildingBar = self.canvas.axes.bar(data["CurrentDay"], building, 0.85, bottom=np.array(none)+np.array(hunting), color="#66b3ff")
        self.canvas.axes.set_ylabel("Number of Agents")
        self.canvas.axes.set_xlabel("Day")
        self.canvas.axes.set_title("Agent Activity Breakdown per Day")
        self.canvas.axes.legend((noneBar[0], huntingBar[0], buildingBar[0]), ("None", "Hunting", "Building"))

        if save:
            return self.canvas.fig
        else:
            self.canvas.draw()
    
    def defaultWorkRulePlot(self, data, save):
        self.clear()

        everyone = []
        strongest = []
        byChoice = []

        watch = data.iloc[0]["CurrentWorkRule"]
        start = 1
        count = 0

        for i, x in enumerate(data["CurrentWorkRule"]):
            if x != watch:
                if watch == "Everyone":
                    everyone.append((start, count))
                elif watch == "Strongest":
                    strongest.append((start, count))
                else:
                    byChoice.append((start, count))
                start = i+1
                count = 0
                watch = x
            count += 1
        
        self.canvas.axes.broken_barh(strongest, (13,5), facecolors='#66b3ff')
        self.canvas.axes.broken_barh(byChoice, (23,5), facecolors='#99ff99')
        self.canvas.axes.broken_barh(everyone, (33,5), facecolors='#ff9999')
        self.canvas.axes.set_xlabel("Day")
        self.canvas.axes.set_ylabel("Work Rule")
        self.canvas.axes.set_title("Work Rule During Simulation")
        self.canvas.axes.set_ylim(5, 45)
        self.canvas.axes.set_yticks([15, 25, 35])
        self.canvas.axes.set_yticklabels(["Strongest", "By Choice", "Everyone"])
        self.canvas.fig.tight_layout()

        if save:
            return self.canvas.fig
        else:
            self.canvas.draw()

    def defaultPunishmentRulePlot(self, data, save):
        self.clear()

        noFoodAndShelter = []
        exile = []
        increment = []
        decrement = []

        watch = data.iloc[0]["CurrentMaxPunishment"]
        start = 1
        count = 0

        for i, x in enumerate(data["CurrentMaxPunishment"]):
            if x != watch:
                if watch == "Exile":
                    exile.append((start, count))
                elif watch == "Increment":
                    increment.append((start, count))
                elif watch == "Decrement":
                    decrement.append((start, count))
                else:
                    noFoodAndShelter.append((start, count))
                start = i+1
                count = 0
                watch = x
            count += 1
        
        self.canvas.axes.broken_barh(noFoodAndShelter, (13,5), facecolors='#66b3ff')
        self.canvas.axes.broken_barh(increment, (23,5), facecolors='#99ff99')
        self.canvas.axes.broken_barh(decrement, (33,5), facecolors='#ffcc99')
        self.canvas.axes.broken_barh(exile, (43,5), facecolors='#ff9999')
        self.canvas.axes.set_xlabel("Day")
        self.canvas.axes.set_ylabel("Maximum Punishment")
        self.canvas.axes.set_title("Maximum Punishment During Simulation")
        self.canvas.axes.set_ylim(5, 55)
        self.canvas.axes.set_yticks([15, 25, 35, 45])
        self.canvas.axes.set_yticklabels(["No Food and Shelter", "Increment", "Decrement", "Exile"])
        self.canvas.fig.tight_layout()

        if save:
            return self.canvas.fig
        else:
            self.canvas.draw()

    def defaultVotingRulePlot(self, data, save):
        self.clear()

        borda = []
        instantRunoff = []
        plurality = []
        approval = []

        watch = data.iloc[0]["CurrentVotingRule"]
        start = 1
        count = 0

        for i, x in enumerate(data["CurrentVotingRule"]):
            if x != watch:
                if watch == "Borda":
                    borda.append((start, count))
                elif watch == "Approval":
                    approval.append((start, count))
                elif watch == "Plurality":
                    plurality.append((start, count))
                else:
                    instantRunoff.append((start, count))
                start = i+1
                count = 0
                watch = x
            count += 1

        watch = data.iloc[-1]["CurrentVotingRule"]
        if watch == "Borda":
            borda.append((start, count))
        elif watch == "Approval":
            approval.append((start, count))
        elif watch == "Plurality":
            plurality.append((start, count))
        else:
            instantRunoff.append((start, count))
        
        self.canvas.axes.broken_barh(borda, (13,5), facecolors='#66b3ff')
        self.canvas.axes.broken_barh(approval, (23,5), facecolors='#99ff99')
        self.canvas.axes.broken_barh(instantRunoff, (33,5), facecolors='#ffcc99')
        self.canvas.axes.broken_barh(plurality, (43,5), facecolors='#ff9999')
        self.canvas.axes.set_xlabel("Day")
        self.canvas.axes.set_ylabel("Voting Rule")
        self.canvas.axes.set_title("Voting Rule During Simulation")
        self.canvas.axes.set_ylim(5, 55)
        self.canvas.axes.set_yticks([15, 25, 35, 45])
        self.canvas.axes.set_yticklabels(["Borda", "Approval", "Instant Runoff", "Plurality"])
        self.canvas.fig.tight_layout()

        if save:
            return self.canvas.fig
        else:
            self.canvas.draw()

    def defaultFoodRulePlot(self, data, save):
        self.clear()

        communism = []
        oligarchy = []
        meritocracy = []
        socialism = []

        watch = data.iloc[0]["CurrentFoodRule"]
        start = 1
        count = 0

        for i, x in enumerate(data["CurrentFoodRule"]):
            if x != watch:
                if watch == "Communism":
                    communism.append((start, count))
                elif watch == "Socialism":
                    socialism.append((start, count))
                elif watch == "Oligarchy":
                    meritocracy.append((start, count))
                else:
                    oligarchy.append((start, count))
                start = i+1
                count = 0
                watch = x
            count += 1
        
        self.canvas.axes.broken_barh(socialism, (13,5), facecolors='#66b3ff')
        self.canvas.axes.broken_barh(meritocracy, (23,5), facecolors='#99ff99')
        self.canvas.axes.broken_barh(oligarchy, (33,5), facecolors='#ffcc99')
        self.canvas.axes.broken_barh(communism, (43,5), facecolors='#ff9999')
        self.canvas.axes.set_xlabel("Day")
        self.canvas.axes.set_ylabel("Food Rule")
        self.canvas.axes.set_title("Food Rule During Simulation")
        self.canvas.axes.set_ylim(5, 55)
        self.canvas.axes.set_yticks([15, 25, 35, 45])
        self.canvas.axes.set_yticklabels(["Socialism", "Meritocracy", "Oligarchy", "Communism"])
        self.canvas.fig.tight_layout()

        if save:
            return self.canvas.fig
        else:
            self.canvas.draw()

    def defaultShelterRulePlot(self, data, save):
        self.clear()

        random = []
        oligarchy = []
        meritocracy = []
        socialism = []

        watch = data.iloc[0]["CurrentShelterRule"]
        start = 1
        count = 0

        for i, x in enumerate(data["CurrentShelterRule"]):
            if x != watch:
                if watch == "Random":
                    random.append((start, count))
                elif watch == "Socialism":
                    socialism.append((start, count))
                elif watch == "Oligarchy":
                    meritocracy.append((start, count))
                else:
                    oligarchy.append((start, count))
                start = i+1
                count = 0
                watch = x
            count += 1
        
        self.canvas.axes.broken_barh(socialism, (13,5), facecolors='#66b3ff')
        self.canvas.axes.broken_barh(meritocracy, (23,5), facecolors='#99ff99')
        self.canvas.axes.broken_barh(oligarchy, (33,5), facecolors='#ffcc99')
        self.canvas.axes.broken_barh(random, (43,5), facecolors='#ff9999')
        self.canvas.axes.set_xlabel("Day")
        self.canvas.axes.set_ylabel("Shelter Rule")
        self.canvas.axes.set_title("Shelter Rule During Simulation")
        self.canvas.axes.set_ylim(5, 55)
        self.canvas.axes.set_yticks([15, 25, 35, 45])
        self.canvas.axes.set_yticklabels(["Socialism", "Meritocracy", "Oligarchy", "Random"])
        self.canvas.fig.tight_layout()

        if save:
            return self.canvas.fig
        else:
            self.canvas.draw()

    def defaultInfamyPlot(self, data, save):
        self.clear()
        self.canvas.axes.plot(data["CurrentDay"], data["Average Infamy"], color='blue')
        self.canvas.axes.set_ylim(0,1)
        self.canvas.axes.set_xlabel("Day")
        self.canvas.axes.set_ylabel("Infamy")
        self.canvas.axes.set_title("Average Agent Infamy")

        if save:
            return self.canvas.fig
        else:
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

            fig = ((self.defaultInfamyPlot(data, True), "infamy.png"))
            fig[0].savefig(fig[1])
            zip.write(fig[1])
            plotNames.append(fig[1])
            
        self.clear()
        self.canvas.draw()
        return plotNames
