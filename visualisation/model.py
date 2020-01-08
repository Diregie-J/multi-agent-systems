# model.py

import matplotlib
import pandas as pd
import os
from zipfile import ZipFile
from matplotlib.figure import Figure

class Model:
    def __init__(self):
        self.fileName = None
        self.fileContent = ""
        self.maxDays = "0"
        self.plotContent = ""
        self.columns = ""
        self.csvFileSelection = []
        self.simRuns = 1
        self.simDays = -1
        self.balancedAgents = 0
        self.egotistAgents = 0
        self.egotistNAgents = 0
        self.idealistAgents = 0
        self.idealistNAgents = 0
        self.susceptibleAgents = 0
        self.susceptibleNAgents = 0

    def isValid(self, fileName):
        if fileName.endswith('.csv'):
            try:
                file = open(fileName, 'r')
                file.close()
                return True
            except:
                return False
        else:
            return False

    def numDays(self, log):
        with open(log) as f:
            i = -1
            for i, l in enumerate(f):
                pass
        return i

    def setFileName(self, fileName, new):
        if self.isValid(fileName):
            self.fileName = fileName
            self.fileContent = pd.read_csv(fileName)
            self.addAverageColumns()
            self.maxDays = len(self.fileContent.index)
            self.columns = self.fileContent.columns.values.tolist()
            if new:
                self.csvFileSelection.append((os.path.basename(fileName) + " (" + str(self.getMaxDays()) + " days)", fileName))
        else:
            self.fileContent = ""
            self.fileName = ""
            self.plotContent = ""

    def addCurrentSimulation(self, runs):
        for x in range(runs):
            fileName = os.path.join("..", "csv", "test" + str(x) + ".csv")
            self.csvFileSelection.append(("Run " + str(x) + " (" + str(self.numDays(fileName)) + " days)", fileName))

    def clearLastSimulation(self):
        removals = []
        for x in self.csvFileSelection:
            if x[1].startswith(os.path.join("..", "csv", "")):
                if os.path.basename(x[1]).startswith("test"):
                    removals.append(x)
        
        for y in removals:
            self.csvFileSelection.remove(y)

    def addAverageColumns(self):
        #energy average
        temp = self.fileContent.filter(regex="Energy$", axis=1)
        averageColumn = temp.mean(axis=1)
        self.fileContent["Average Energy"] = averageColumn

        #egotism average
        temp = self.fileContent.filter(regex="Egotism$", axis=1)
        averageColumn = temp.mean(axis=1)
        self.fileContent["Average Egotism"] = averageColumn

        #susceptibility average
        temp = self.fileContent.filter(regex="Susceptibility$", axis=1)
        averageColumn = temp.mean(axis=1)
        self.fileContent["Average Susceptibility"] = averageColumn

        #idealism average
        temp = self.fileContent.filter(regex="Idealism$", axis=1)
        averageColumn = temp.mean(axis=1)
        self.fileContent["Average Idealism"] = averageColumn

        #fairness average
        temp = self.fileContent.filter(regex="Fairness$", axis=1)
        averageColumn = temp.mean(axis=1)
        self.fileContent["Average Fairness"] = averageColumn

        #infamy average
        temp = self.fileContent.filter(regex="Infamy$", axis=1)
        averageColumn = temp.mean(axis=1)
        self.fileContent["Average Infamy"] = averageColumn

    def addFilter(self, parameter, include=True, value='', num=0, greater=0):
        #gets datatype of column
        dataType = getattr(self.plotContent, parameter)
        dataType = getattr(dataType, 'dtype')
        if dataType == 'object':
            # filter strings
            if include:
                self.plotContent = self.plotContent[getattr(self.plotContent, parameter) == value]
            else:
                self.plotContent = self.plotContent[getattr(self.plotContent, parameter) != value]
        else:
            # filter numeric data
            if greater == 0:
                self.plotContent = self.plotContent[getattr(self.plotContent, parameter) > num]
            elif greater == 1:
                self.plotContent = self.plotContent[getattr(self.plotContent, parameter) == num]
            else:
                self.plotContent = self.plotContent[getattr(self.plotContent, parameter) < num]


    def getFileName(self):
        return self.fileName
        
    def getFileContents(self):
        return self.fileContent

    def getPlotContents(self):
        return self.plotContent

    def getCsvPath(self, index):
        return self.csvFileSelection[index][1]

    def getColumns(self):
        return self.columns

    def getMaxDays(self):
        return self.maxDays

    def getSimRuns(self):
        return self.simRuns

    def getSimDays(self):
        return self.simDays

    def getBalancedAgents(self):
        return self.balancedAgents

    def getEgotistAgents(self):
        return self.egotistAgents

    def getEgotistNAgents(self):
        return self.egotistNAgents

    def getIdealistAgents(self):
        return self.idealistAgents
    
    def getIdealistNAgents(self):
        return self.idealistNAgents

    def getSusceptibleAgents(self):
        return self.susceptibleAgents

    def getSusceptibleNAgents(self):
        return self.susceptibleNAgents
    
    def updateSimRuns(self, value):
        self.simRuns = value

    def updateSimDays(self, value):
        self.simDays = value

    def updateBalancedAgents(self, value):
        self.balancedAgents = value

    def updateEgotistAgents(self, value):
        self.egotistAgents = value

    def updateEgotistNAgents(self, value):
        self.egotistNAgents = value

    def updateIdealistAgents(self, value):
        self.idealistAgents = value
    
    def updateIdealistNAgents(self, value):
        self.idealistNAgents = value

    def updateSusceptibleAgents(self, value):
        self.susceptibleAgents = value

    def updateSusceptibleNAgents(self, value):
        self.susceptibleNAgents = value

    def updateDay(self, value):
        pass