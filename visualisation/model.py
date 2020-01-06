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

    def setFileName(self, fileName):
        if self.isValid(fileName):
            self.fileName = fileName
            self.fileContent = pd.read_csv(fileName)
            self.addAverageColumns()
            self.maxDays = len(self.fileContent.index)
            self.columns = self.fileContent.columns.values.tolist()
            self.csvFileSelection.append((os.path.basename(fileName) + " (" + str(self.getMaxDays()) + " days)", fileName))
        else:
            self.fileContent = ""
            self.fileName = ""
            self.plotContent = ""

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

    def getColumns(self):
        return self.columns

    def getMaxDays(self):
        return self.maxDays
    
    def updateDay(self, value):
        pass