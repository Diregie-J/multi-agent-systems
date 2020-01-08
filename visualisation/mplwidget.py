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
from matplotlib.animation import FFMpegWriter
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
        self.sampleLim = 300
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.vbl = QtWidgets.QVBoxLayout()
        self.vbl.addWidget(self.canvas)
        self.vbl.addWidget(self.toolbar)
        self.setLayout(self.vbl)

    def plot(self, data, x, y):
        # do stuff to fig or axes to plot things
        self.canvas.draw()

    def my_autopct(self, pct):
        return ('%.1f%%' % pct) if pct > 5 else ''

    def my_labels(self, pct, label):
        return label if pct > 5 else ''
    
    def standardTest(self, data, save):
        self.standardInfamyPlot(data, False)

    def standardInfamyDistribution(self, data, save):
        self.clear()

        infamy = data.filter(regex="Infamy$", axis=1)
        infamy.drop(["Average Infamy"], axis=1)
        day = data["CurrentDay"]        

        while len(infamy) > self.sampleLim:
            day = day[::2]
            infamy = infamy[::2]

        self.canvas.axes.plot(day, infamy.quantile(0.9, axis=1), color="indianred")
        #self.canvas.axes.plot(day, infamy.quantile(0.8, axis=1), color="orange")
        self.canvas.axes.plot(day, infamy.quantile(0.7, axis=1), color="gold")
        self.canvas.axes.plot(day, infamy.quantile(0.5, axis=1), color="lightgreen")
        self.canvas.axes.plot(day, infamy.quantile(0.3, axis=1), color="deepskyblue")
        #self.canvas.axes.plot(day, infamy.quantile(0.2, axis=1), color="plum")
        self.canvas.axes.plot(day, infamy.quantile(0.1, axis=1), color="mediumpurple")
        self.canvas.axes.legend()

        self.canvas.axes.set_title('Agent Infamy Distribution')

        # adding horizontal grid lines
        self.canvas.axes.set_xlabel('Day')
        self.canvas.axes.set_ylabel('Infamy')
        self.canvas.axes.set_ylim(0)

        if save:
            return self.canvas.fig
        else:
            self.canvas.draw()

    def standardISE(self, data, save):
        self.clear()

        self.canvas.axes.plot(data["CurrentDay"], data["Average Egotism"], color='#66b3ff')
        self.canvas.axes.plot(data["CurrentDay"], data["Average Idealism"], color='#99ff99')
        self.canvas.axes.plot(data["CurrentDay"], data["Average Susceptibility"], color='#ff9999')
        self.canvas.axes.set_xlabel("Day")
        self.canvas.axes.legend()

        if save:
            return self.canvas.fig
        else:
            self.canvas.draw()

    def standardCrimeRate(self, data, save):
        self.clear()

        crimes = data.filter(regex="LastCrimeDate$", axis=1)
        agentNum = len(crimes.columns)
        crimes["Number of Crimes"] = 0

        for i in crimes.columns:
            crimes["Number of Crimes"] = np.where((data["CurrentDay"] - crimes[i] == 1) & (i != "Number of Crimes") & (crimes[i] != -1), 
                                                    crimes["Number of Crimes"]+1, crimes["Number of Crimes"])

        dead = data.filter(regex="Alive$", axis=1)
        crimes["Number Dead"] = dead.isnull().sum(axis=1)
        crimes["Crime Rate"] = crimes["Number of Crimes"]/(agentNum - crimes["Number Dead"])

        self.canvas.axes.plot(data["CurrentDay"], crimes["Crime Rate"], color='#66b3ff')
        self.canvas.axes.set_xlabel("Day")
        self.canvas.axes.set_ylabel("Crimes Committed per Person", color='#66b3ff')
        self.canvas.axes.set_title("Crime Rate per Person")

        deadAxes = self.canvas.axes.twinx()
        deadAxes.plot(data["CurrentDay"], crimes["Number Dead"], color='#ff9999')
        deadAxes.set_ylabel("Number of Dead Agents", color='#ff9999')
        deadAxes.set_ylim(0)

        if save:
            return self.canvas.fig
        else:
            self.canvas.draw()

    def standardCrimeRaw(self, data, save):
        self.clear()

        crimes = data.filter(regex="LastCrimeDate$", axis=1)
        crimes["Number of Crimes"] = 0

        for i in crimes.columns:
            crimes["Number of Crimes"] = np.where((data["CurrentDay"] - crimes[i] == 1) & (i != "Number of Crimes") & (crimes[i] != -1), 
                                                    crimes["Number of Crimes"]+1, crimes["Number of Crimes"])

        self.canvas.axes.plot(data["CurrentDay"], crimes["Number of Crimes"], color='#66b3ff')
        self.canvas.axes.set_xlabel("Day")
        self.canvas.axes.set_ylabel("Crimes Committed")
        self.canvas.axes.set_title("Crimes Committed per Day")

        if save:
            return self.canvas.fig
        else:
            self.canvas.draw()

    def standardPunishmentRulePie(self, data, save):
        self.clear()

        labels = ['Exile', 'No Food and Shelter', 'Increment', 'Decrement']
        colors = ['#ff9999','#66b3ff','#99ff99', '#ffcc99']
        explode = [0.05,0.05,0.05,0.05]
        sizes = []
        occurences = data["CurrentMaxPunishment"].value_counts()

        try:
            sizes.append(occurences.loc["Exile"])
        except:
            labels.remove('Exile')
            colors.remove('#ff9999')
            explode.pop()

        try:
            sizes.append(occurences.loc["NoFoodAndShelter"])
        except:
            labels.remove('No Food and Shelter')
            colors.remove('#66b3ff')
            explode.pop()

        try:
            sizes.append(occurences.loc["Increment"])
        except:
            labels.remove("Increment")
            colors.remove('#99ff99')
            explode.pop()

        try:
            sizes.append(occurences.loc["Decrement"])
        except:
            labels.remove("Decrement")
            colors.remove('#ffcc99')
            explode.pop()
        
        self.canvas.axes.pie(sizes, colors = colors, labels=labels, autopct=self.my_autopct, startangle=90, pctdistance=0.85, explode = explode)
        centre_circle = matplotlib.patches.Circle((0,0),0.70,fc='white')
        self.canvas.axes.add_patch(centre_circle)
        self.canvas.axes.axis('equal')
        self.canvas.axes.set_title('Maximum Punishment Proportions')

        if save:
            return self.canvas.fig
        else:
            self.canvas.draw()

    def standardWorkRulePie(self, data, save):
        self.clear()

        labels = ['Everyone', 'Strongest', 'By Choice']
        colors = ['#ff9999','#66b3ff','#99ff99']
        explode = [0.05,0.05,0.05]
        sizes = []
        occurences = data["CurrentWorkRule"].value_counts()

        try:
            sizes.append(occurences.loc["Everyone"])
        except:
            labels.remove('Everyone')
            colors.remove('#ff9999')
            explode.pop()

        try:
            sizes.append(occurences.loc["Strongest"])
        except:
            labels.remove('Strongest')
            colors.remove('#66b3ff')
            explode.pop()

        try:
            sizes.append(occurences.loc["ByChoice"])
        except:
            labels.remove("By Choice")
            colors.remove('#99ff99')
            explode.pop()
        
        self.canvas.axes.pie(sizes, colors = colors, labels=labels, autopct=self.my_autopct, startangle=90, pctdistance=0.85, explode = explode)
        centre_circle = matplotlib.patches.Circle((0,0),0.70,fc='white')
        self.canvas.axes.add_patch(centre_circle)
        self.canvas.axes.axis('equal')
        self.canvas.axes.set_title('Work Rule Proportions')

        if save:
            return self.canvas.fig
        else:
            self.canvas.draw()

    def standardVotingRulePie(self, data, save):
        self.clear()

        labels = ['Plurality', 'Borda', 'Approval', 'Instant Runoff']
        colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']
        explode = [0.05,0.05,0.05,0.05]
        sizes = []
        occurences = data["CurrentVotingRule"].value_counts()

        try:
            sizes.append(occurences.loc["Plurality"])
        except:
            labels.remove('Plurality')
            colors.remove('#ff9999')
            explode.pop()

        try:
            sizes.append(occurences.loc["Borda"])
        except:
            labels.remove('Borda')
            colors.remove('#66b3ff')
            explode.pop()

        try:
            sizes.append(occurences.loc["Approval"])
        except:
            labels.remove("Approval")
            colors.remove('#99ff99')
            explode.pop()

        try:
            sizes.append(occurences.loc["InstantRunoff"])
        except:
            labels.remove('Instant Runoff')
            colors.remove('#ffcc99')
            explode.pop()
        
        self.canvas.axes.pie(sizes, colors = colors, labels=labels, autopct=self.my_autopct, startangle=90, pctdistance=0.85, explode = explode)
        centre_circle = matplotlib.patches.Circle((0,0),0.70,fc='white')
        self.canvas.axes.add_patch(centre_circle)
        self.canvas.axes.axis('equal')
        self.canvas.axes.set_title('Voting Rule Proportions')

        if save:
            return self.canvas.fig
        else:
            self.canvas.draw()

    def standardFoodRulePie(self, data, save):
        self.clear()

        labels = ['Communism', 'Oligarchy', 'Meritocracy', 'Socialism']
        colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']
        explode = [0.05,0.05,0.05,0.05]
        sizes = []
        occurences = data["CurrentFoodRule"].value_counts()

        try:
            sizes.append(occurences.loc["Communism"])
        except:
            labels.remove('Communism')
            colors.remove('#ff9999')
            explode.pop()

        try:
            sizes.append(occurences.loc["Oligarchy"])
        except:
            labels.remove('Oligarchy')
            colors.remove('#66b3ff')
            explode.pop()

        try:
            sizes.append(occurences.loc["Meritocracy"])
        except:
            labels.remove("Meritocracy")
            colors.remove('#99ff99')
            explode.pop()

        try:
            sizes.append(occurences.loc["Socialism"])
        except:
            labels.remove('Socialism')
            colors.remove('#ffcc99')
            explode.pop()
        
        self.canvas.axes.pie(sizes, colors = colors, labels=labels, autopct=self.my_autopct, startangle=90, pctdistance=0.85, explode = explode)
        centre_circle = matplotlib.patches.Circle((0,0),0.70,fc='white')
        self.canvas.axes.add_patch(centre_circle)
        self.canvas.axes.axis('equal')
        self.canvas.axes.set_title('Food Rule Proportions')

        if save:
            return self.canvas.fig
        else:
            self.canvas.draw()

    def standardShelterRulePie(self, data, save):
        self.clear()

        labels = ['Random', 'Oligarchy', 'Meritocracy', 'Socialism']
        colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']
        explode = [0.05,0.05,0.05,0.05]
        sizes = []
        occurences = data["CurrentShelterRule"].value_counts()

        try:
            sizes.append(occurences.loc["Random"])
        except:
            labels.remove('Random')
            colors.remove('#ff9999')
            explode.pop()

        try:
            sizes.append(occurences.loc["Oligarchy"])
        except:
            labels.remove('Oligarchy')
            colors.remove('#66b3ff')
            explode.pop()

        try:
            sizes.append(occurences.loc["Meritocracy"])
        except:
            labels.remove("Meritocracy")
            colors.remove('#99ff99')
            explode.pop()

        try:
            sizes.append(occurences.loc["Socialism"])
        except:
            labels.remove('Socialism')
            colors.remove('#ffcc99')
            explode.pop()
        
        self.canvas.axes.pie(sizes, colors = colors, labels=labels, autopct=self.my_autopct, startangle=90, pctdistance=0.85, explode = explode)
        centre_circle = matplotlib.patches.Circle((0,0),0.70,fc='white')
        self.canvas.axes.add_patch(centre_circle)
        self.canvas.axes.axis('equal')
        self.canvas.axes.set_title('Shelter Rule Proportions')  

        if save:
            return self.canvas.fig
        else:
            self.canvas.draw()


    def standardActivity(self, data, save):
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
    
    def standardWorkRule(self, data, save):
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
        
        watch = data.iloc[-1]["CurrentWorkRule"]
        if watch == "Everyone":
            everyone.append((start, count))
        elif watch == "Strongest":
            strongest.append((start, count))
        else:
            byChoice.append((start, count))


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

    def standardPunishmentRule(self, data, save):
        self.clear()

        noFoodAndShelter = []
        exile = []

        watch = data.iloc[0]["CurrentMaxPunishment"]
        start = 1
        count = 0

        for i, x in enumerate(data["CurrentMaxPunishment"]):
            if x != watch:
                if watch == "Exile":
                    exile.append((start, count))
                else:
                    noFoodAndShelter.append((start, count))
                start = i+1
                count = 0
                watch = x
            count += 1
        
        watch = data.iloc[-1]["CurrentMaxPunishment"]
        if watch == "Exile":
            exile.append((start, count))
        else:
            noFoodAndShelter.append((start, count))


        self.canvas.axes.broken_barh(noFoodAndShelter, (13,5), facecolors='#66b3ff')
        self.canvas.axes.broken_barh(exile, (23,5), facecolors='#ff9999')
        self.canvas.axes.set_xlabel("Day")
        self.canvas.axes.set_ylabel("Maximum Punishment")
        self.canvas.axes.set_title("Maximum Punishment During Simulation")
        self.canvas.axes.set_ylim(5, 35)
        self.canvas.axes.set_yticks([15, 25])
        self.canvas.axes.set_yticklabels(["No Food and Shelter", "Exile"])
        self.canvas.fig.tight_layout()

        if save:
            return self.canvas.fig
        else:
            self.canvas.draw()

    def standardVotingRule(self, data, save):
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

    def standardFoodRule(self, data, save):
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

        watch = data.iloc[-1]["CurrentFoodRule"]
        if watch == "Communism":
            communism.append((start, count))
        elif watch == "Socialism":
            socialism.append((start, count))
        elif watch == "Oligarchy":
            meritocracy.append((start, count))
        else:
            oligarchy.append((start, count))
        
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

    def standardShelterRule(self, data, save):
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
        
        watch = data.iloc[-1]["CurrentShelterRule"]
        if watch == "Random":
            random.append((start, count))
        elif watch == "Socialism":
            socialism.append((start, count))
        elif watch == "Oligarchy":
            meritocracy.append((start, count))
        else:
            oligarchy.append((start, count))

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

    def standardInfamy(self, data, save):
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


    def standardEnergy(self, data, save):
        self.clear()

        energy = data.filter(regex="Energy$", axis=1)
        shortSim = True if len(energy) < 150 else False
        if shortSim:
            energy.apply(lambda x: self.canvas.axes.scatter(x.index+1, x, c='g', marker="x"))
        energy["Average"] = data["Average Energy"]
        self.canvas.axes.plot(data["CurrentDay"], energy["Average"], color='blue')
        self.canvas.axes.set_ylim(0,100)
        ybox1 = TextArea("Energy: ", textprops=dict(color="k", rotation=90,ha='left',va='bottom'))
        if shortSim:
            ybox2 = TextArea("Individual/",     textprops=dict(color="g", rotation=90,ha='left',va='bottom'))
        ybox3 = TextArea("Average", textprops=dict(color="b", rotation=90,ha='left',va='bottom'))

        if shortSim:
            ybox = VPacker(children=[ybox3, ybox2, ybox1],align="bottom", pad=0, sep=2)
        else:
            ybox = VPacker(children=[ybox3, ybox1],align="bottom", pad=0, sep=2)

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

    def standardEnergyDistribution(self, data, save):
        self.clear()
        
        energy = data.filter(regex="Energy$", axis=1)
        energy.drop(["Average Energy"], axis=1)
        day = data["CurrentDay"]        

        while len(energy) > self.sampleLim:
            day = day[::2]
            energy = energy[::2]

        self.canvas.axes.plot(day, energy.quantile(0.9, axis=1), color="indianred")
        #self.canvas.axes.plot(day, energy.quantile(0.8, axis=1), color="orange")
        self.canvas.axes.plot(day, energy.quantile(0.7, axis=1), color="gold")
        self.canvas.axes.plot(day, energy.quantile(0.5, axis=1), color="lightgreen")
        self.canvas.axes.plot(day, energy.quantile(0.3, axis=1), color="deepskyblue")
        #self.canvas.axes.plot(day, energy.quantile(0.2, axis=1), color="plum")
        self.canvas.axes.plot(day, energy.quantile(0.1, axis=1), color="mediumpurple")
        self.canvas.axes.legend()

        self.canvas.axes.set_title('Agent Energy Distribution')

        # adding horizontal grid lines
        self.canvas.axes.set_xlabel('Day')
        self.canvas.axes.set_ylabel('Energy')
        self.canvas.axes.set_ylim(0, 100)

        if save:
            return self.canvas.fig
        else:
            self.canvas.draw()

    #def standardEgotism(self, data, save):
    #    self.clear()
    #    self.canvas.axes.plot(data["CurrentDay"], data["Average Egotism"], color='blue')
    #    self.canvas.axes.set_ylim(0,1)
    #    self.canvas.axes.set_xlabel("Day")
    #    self.canvas.axes.set_ylabel("Egotism")
    #    self.canvas.axes.set_title("Average Agent Egotism")
    #    
    #    if save:
    #        return self.canvas.fig
    #    else:
    #        self.canvas.draw()
#
    #def standardSusceptibility(self, data, save):
    #    self.clear()
    #    self.canvas.axes.plot(data["CurrentDay"], data["Average Susceptibility"], color='blue')
    #    self.canvas.axes.set_ylim(0,1)
    #    self.canvas.axes.set_xlabel("Day")
    #    self.canvas.axes.set_ylabel("Susceptibility")
    #    self.canvas.axes.set_title("Average Agent Susceptibility")
#
    #    if save:
    #        return self.canvas.fig
    #    else:
    #        self.canvas.draw()
#
    #def standardIdealism(self, data, save):
    #    self.clear()
    #    self.canvas.axes.plot(data["CurrentDay"], data["Average Idealism"], color='blue')
    #    self.canvas.axes.set_ylim(0,1)
    #    self.canvas.axes.set_xlabel("Day")
    #    self.canvas.axes.set_ylabel("Idealism")
    #    self.canvas.axes.set_title("Average Agent Idealism")
#
    #    if save:
    #        return self.canvas.fig
    #    else:
    #        self.canvas.draw()

    def standardFairness(self, data, save):
        self.clear()

        fairness = data.filter(regex="Fairness$", axis=1)
        fairness.drop(["Average Fairness"], axis=1)
        day = data["CurrentDay"]

        while len(fairness) > self.sampleLim:
            day = day[::2]
            fairness = fairness[::2]

        self.canvas.axes.plot(day, fairness.quantile(0.9, axis=1), color="indianred")
        #self.canvas.axes.plot(day, fairness.quantile(0.8, axis=1), color="orange")
        self.canvas.axes.plot(day, fairness.quantile(0.7, axis=1), color="gold")
        self.canvas.axes.plot(day, fairness.quantile(0.5, axis=1), color="lightgreen")
        self.canvas.axes.plot(day, fairness.quantile(0.3, axis=1), color="deepskyblue")
        #self.canvas.axes.plot(day, fairness.quantile(0.2, axis=1), color="plum")
        self.canvas.axes.plot(day, fairness.quantile(0.1, axis=1), color="mediumpurple")
        self.canvas.axes.legend()

        self.canvas.axes.set_title('Agent Fairness Distribution')

        # adding horizontal grid lines
        self.canvas.axes.set_xlabel('Day')
        self.canvas.axes.set_ylabel('Fairness')

        if save:
            return self.canvas.fig
        else:
            self.canvas.draw()

    def agentDistribution(self, balanced, idealist, egotist, susceptible, idealistN, egotistN, susceptibleN, save):
        self.clear()

        agents = []

        labels = ['Balanced', 'Idealist', 'Egotist', 'Susceptible', 'Not Idealist', 'Not Egotist', 'Not Susceptible']
        colors = ['indianred','orange','gold','lightgreen', 'deepskyblue', 'plum', 'mediumpurple']

        if balanced == 0:
            labels.remove('Balanced')
            colors.remove('indianred')
        else:
            agents.append(balanced)
        
        if idealist == 0:
            labels.remove("Idealist")
            colors.remove("orange")
        else:
            agents.append(idealist)
        
        if egotist == 0:
            labels.remove("Egotist")
            colors.remove("gold")
        else:
            agents.append(egotist)

        if susceptible == 0:
            labels.remove("Susceptible")
            colors.remove("lightgreen")
        else:
            agents.append(susceptible)

        if idealistN == 0:
            labels.remove("Not Idealist")
            colors.remove("deepskyblue")
        else:
            agents.append(idealistN)

        if egotistN == 0:
            labels.remove("Not Egotist")
            colors.remove("plum")
        else:
            agents.append(egotistN)

        if susceptibleN == 0:
            labels.remove("Not Susceptible")
            colors.remove("mediumpurple")
        else:
            agents.append(susceptibleN)

        if len(colors) == 0:
            return

        explode = [0.05]*len(colors)

        self.canvas.axes.pie(agents, colors = colors, labels=labels, autopct=self.my_autopct, startangle=90, pctdistance=0.85, explode = explode)
        centre_circle = matplotlib.patches.Circle((0,0),0.70,fc='white')
        self.canvas.axes.add_patch(centre_circle)
        self.canvas.axes.axis('equal')
        self.canvas.axes.set_title('Agent Profiles')

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
            fig = ((self.standardEnergy(data, True), "averageEnergy.png"))
            fig[0].savefig(fig[1])
            zip.write(fig[1])
            plotNames.append(fig[1])

            fig = ((self.standardEnergyDistribution(data, True), "energyDistribution.png"))
            fig[0].savefig(fig[1])
            zip.write(fig[1])
            plotNames.append(fig[1])

            fig = ((self.standardISE(data, True), "ISE.png"))
            fig[0].savefig(fig[1])
            zip.write(fig[1])
            plotNames.append(fig[1])

            fig = ((self.standardFairness(data, True), "fairness.png"))
            fig[0].savefig(fig[1])
            zip.write(fig[1])
            plotNames.append(fig[1])

            fig = ((self.standardInfamy(data, True), "infamy.png"))
            fig[0].savefig(fig[1])
            zip.write(fig[1])
            plotNames.append(fig[1])

            fig = ((self.standardCrimeRate(data, True), "crimeRate.png"))
            fig[0].savefig(fig[1])
            zip.write(fig[1])
            plotNames.append(fig[1])

            fig = ((self.standardCrimeRaw(data, True), "crimeRaw.png"))
            fig[0].savefig(fig[1])
            zip.write(fig[1])
            plotNames.append(fig[1])

            fig = ((self.standardPunishmentRulePie(data, True), "punishmentRulePie.png"))
            fig[0].savefig(fig[1])
            zip.write(fig[1])
            plotNames.append(fig[1])

            fig = ((self.standardWorkRulePie(data, True), "workRulePie.png"))
            fig[0].savefig(fig[1])
            zip.write(fig[1])
            plotNames.append(fig[1])

            fig = ((self.standardVotingRulePie(data, True), "votingRulePie.png"))
            fig[0].savefig(fig[1])
            zip.write(fig[1])
            plotNames.append(fig[1])

            fig = ((self.standardFoodRulePie(data, True), "foodRulePie.png"))
            fig[0].savefig(fig[1])
            zip.write(fig[1])
            plotNames.append(fig[1])

            fig = ((self.standardShelterRulePie(data, True), "shelterRulePie.png"))
            fig[0].savefig(fig[1])
            zip.write(fig[1])
            plotNames.append(fig[1])

            fig = ((self.standardPunishmentRule(data, True), "punishmentRule.png"))
            fig[0].savefig(fig[1])
            zip.write(fig[1])
            plotNames.append(fig[1])

            fig = ((self.standardWorkRule(data, True), "workRule.png"))
            fig[0].savefig(fig[1])
            zip.write(fig[1])
            plotNames.append(fig[1])

            fig = ((self.standardVotingRule(data, True), "votingRule.png"))
            fig[0].savefig(fig[1])
            zip.write(fig[1])
            plotNames.append(fig[1])

            fig = ((self.standardFoodRule(data, True), "foodRule.png"))
            fig[0].savefig(fig[1])
            zip.write(fig[1])
            plotNames.append(fig[1])

            fig = ((self.standardShelterRule(data, True), "shelterRule.png"))
            fig[0].savefig(fig[1])
            zip.write(fig[1])
            plotNames.append(fig[1])

            fig = ((self.standardActivity(data, True), "activity.png"))
            fig[0].savefig(fig[1])
            zip.write(fig[1])
            plotNames.append(fig[1])
            
        self.clear()
        self.canvas.draw()
        return plotNames
