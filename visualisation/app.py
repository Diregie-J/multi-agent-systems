# app.py

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSlot
from gui import Ui_MainWindow
from zipfile import ZipFile
import sys
from os import remove as DeleteFile
import pandas as pd
import matplotlib
from matplotlib.figure import Figure
from model import Model

class MainWindowUiClass(Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.model = Model()

    def setupUi(self, mw):
        super().setupUi(mw)

    def runSimulationPressedSlot(self):
        self.runSimulation(runs, days, balanced, idealist, egotist, susceptible, idealistN, egotistN, suscpetibleN)

    def runSimulation(self, runs, days, balanced, idealist, egotist, susceptible, idealistN, egotistN, suscpetibleN):
        agent_init = f"from agent import *\n\nTotalProfiles = [(Balanced, {balanced}), (Egotist, {egotist}), (Idealist, {idealist}), (Susceptible, {susceptible}), (NotIdealist, {idealistN}), (NotEgotist, {egotistN}), (NotSusceptible, {suscpetibleN})]"
        total_agents = balanced + idealist + egotist + susceptible + idealistN + egotistN + suscpetibleN
        cmd = f"cd ../multi-agent-systems/Agent-Config ; printf \"{agent_init}\" > total_profiles.py ; python3 agent_init.py ; cd ../bin/Debug/netcoreapp3.0/ ; ./multi-agent-systems  --number-days {days} --number-profiles 7 --number-agents {total_agents} --number-runs {runs}"

        os.system(cmd)

    def filterPrint(self, msg):
        self.filterBrowser.append(msg)

    def refreshAll(self):
        self.populateStandardComboBox()
        self.saveCsvPushButton.setEnabled(True)
        self.standardPlotComboBox.setEnabled(True)
        self.selectCsvComboBox.setEnabled(True)
        self.addToCsvSelect()
        self.addAgentPushButton.setEnabled(True)
        self.saveAllPushButton.setEnabled(True)
        self.gifButton.setEnabled(True)
        self.daySpinBox.setEnabled(True)
        self.clearAgentsPushButton.setEnabled(True)
        self.plotTypeComboBox.setEnabled(True)
        self.colourComboBox.setEnabled(True)
        self.agentAverageRadio.setEnabled(True)
        self.timeAverageRadio.setEnabled(True)
        self.xComboBox.setEnabled(True)
        self.yComboBox.setEnabled(True)
        self.filterComboBox.setEnabled(True)
        self.comboBox.setEnabled(True)
        self.horizontalSlider.setEnabled(True)
        self.xComboBox.clear()
        self.xComboBox.addItems(self.model.getColumns())
        self.yComboBox.clear()
        self.yComboBox.addItems(self.model.getColumns())
        self.comboBox.clear()
        self.comboBox.addItems(self.model.getColumns())
        self.filterComboBox.clear()
        self.filterComboBox.addItems(["greater than", "equal to", "less than"])
        self.plotTypeComboBox.clear()
        self.plotTypeComboBox.addItems(["line", "bar", "pie", "scatter", "histogram"])
        self.colourComboBox.clear()
        self.colourComboBox.addItems(self.model.getColumns())
        self.lineEdit.setText(self.model.getFileName())
        self.standardPlotWidget.clear()
        self.customPlotWidget.clear()

    def addToCsvSelect(self):
        self.selectCsvComboBox.clear()
        lst = []
        for x in self.model.csvFileSelection:
            lst.append(x[0])
        self.selectCsvComboBox.addItems(lst)


    ######### slots ###########

    def returnPressedSlot(self):
        #self.debugPrint("enter pressed in line edit")
        fileName = self.lineEdit.text()
        if self.model.setFileName(fileName):
            self.model.setFileName(fileName)
            self.refreshAll()
        else:
            m = QtWidgets.QMessageBox()
            m.setText("Invalid file name!\n" + fileName)
            m.setIcon(QtWidgets.QMessageBox.Warning)
            m.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            m.setDefaultButton(QtWidgets.QMessageBox.Cancel)
            ret = m.exec_()
            self.lineEdit.setText("")
            self.refreshAll()
            self.debugPrint("Invalid file specified: " + fileName)

    def loadCsvSlot(self):
        #self.debugPrint("browse button pressed")
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
                        None,
                        "Load CSV",
                        "",
                        "CSV Files (*.csv);;All Files (*)",
                        options=options)
        if fileName:
            self.model.setFileName(fileName)
            self.refreshAll()
            
    def dayChangedSlot(self, value):
        self.model.updateDay(value)

    def noneAverageSelected(self):
        # can do push button setEnabled(True/False)
        pass

    def agentAverageSelected(self):
        pass

    def timeAverageSelected(self):
        pass

    def addAgentSlot(self):
        pass

    def exportGifSlot(self):
        pass

    def saveAllSlot(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(None,
                                                'Save Figures',
                                                "",
                                                "ZIP archive (*.zip);;All Files (*)",
                                                options=options)
        
        if not fileName.endswith(".zip"):
            fileName += ".zip"

        plotNames = self.standardPlotWidget.exportAll(self.model.fileContent, fileName)
        for plot in plotNames:
            DeleteFile(plot)

    def plotColourSlot(self):
        pass

    def plotTypeSlot(self):
        pass

    def xAxisSlot(self):
        pass

    def yAxisSlot(self):
        pass

    def addFilterSlot(self):
        # msg is the filter setting to print
        # pull values
        parameter = str(self.comboBox.currentText())
        dataType = getattr(self.model.fileContent, parameter)
        dataType = dataType.dtype
        msg = parameter
        if dataType == "object":
            value = str(self.filterComboBox.currentText())
            include = self.withRadioButton.isChecked()
            msg += " == " if include else " != "
            msg += value
            self.model.addFilter(parameter, include=include, value=value)

        else:
            num = int(self.filterNumSpinBox.value())
            greater = self.filterComboBox.currentIndex()
            if greater == 0:
                msg += " > "
            elif greater == 1:
                msg += " == "
            else:
                msg += " < " 
            self.model.addFilter(parameter, num=num, greater=greater)
        msg += "\n"
        self.filterPrint(msg)
        pass

    def removeAllFiltersSlot(self):
        self.textBrowser.clear()
        self.model.plotContent = self.model.getFileContents()

    def filterParameterSelectedSlot(self):
        parameter = str(self.comboBox.currentText())
        dataType = getattr(self.model.fileContent, parameter)
        dataType = dataType.dtype
        if dataType == "object":
            self.filterComboBox.clear()
            items = getattr(self.model.plotContent, parameter)
            items = items.unique()
            self.filterComboBox.addItems(items)
            self.filterComboBox.setEnabled(True)
            self.filterNumSpinBox.setEnabled(False)
        else:
            self.filterComboBox.clear()
            self.filterComboBox.addItems(["greater than", "equal to", "less than"])
            self.filterComboBox.setEnabled(True)
            self.filterNumSpinBox.setEnabled(True)


    ############# standard plots ###############

    def populateStandardPlotBox(self):
        self.standardPlotBox.clear()
        self.standardPlotBox.addItem("Average Energy and Agent Death")
        self.standardPlotBox.addItem("Energy Distribution")
        self.standardPlotBox.addItem("Idealism, Susceptibility and Egotism")
        self.standardPlotBox.addItem("Fairness Distribution")
        self.standardPlotBox.addItem("Average Infamy")
        self.standardPlotBox.addItem("Infamy Distribution")
        self.standardPlotBox.addItem("Crime Rate")
        self.standardPlotBox.addItem("Crimes Committed")
        self.standardPlotBox.addItem("Agent Activity")
        self.standardPlotBox.addItem("Maximum Punishment Timeline")
        self.standardPlotBox.addItem("Work Rule Timeline")
        self.standardPlotBox.addItem("Food Rule Timeline")
        self.standardPlotBox.addItem("Shelter Rule Timeline")
        self.standardPlotBox.addItem("Voting Rule Timeline")
        self.standardPlotBox.addItem("Maximum Punishment Distribution")
        self.standardPlotBox.addItem("Work Rule Distribution")
        self.standardPlotBox.addItem("Food Rule Distribution")
        self.standardPlotBox.addItem("Shelter Rule Distribution")
        self.standardPlotBox.addItem("Voting Rule Distribution")
        

    def standardPlotSelectSlot(self, plot):
        plot = str(plot)
        if plot == "Average Energy and Agent Death":
            self.standardPlotWidget.standardEnergy(self.model.fileContent, False)
        elif plot == "Energy Distribution":
            self.standardPlotWidget.standardEnergyDistribution(self.model.fileContent, False)
        elif plot == "Idealism, Susceptibility and Egotism":
            self.standardPlotWidget.standardISE(self.model.fileContent, False)
        elif plot == "Fairness Distribution":
            self.standardPlotWidget.standardFairness(self.model.fileContent, False)
        elif plot == "Average Infamy":
            self.standardPlotWidget.standardInfamy(self.model.fileContent, False)
        elif plot == "Infamy Distribution":
            self.standardPlotWidget.standardInfamyDistribution(self.model.fileContent, False)
        elif plot == "Crime Rate":
            self.standardPlotWidget.standardCrimeRate(self.model.fileContent, False)
        elif plot == "Crimes Committed":
            self.standardPlotWidget.standardCrimeRaw(self.model.fileContent, False)
        elif plot == "Agent Activity":
            self.standardPlotWidget.standardActivity(self.model.fileContent, False)
        elif plot == "Maximum Punishment Timeline":
            self.standardPlotWidget.standardPunishmentRule(self.model.fileContent, False)
        elif plot == "Work Rule Timeline":
            self.standardPlotWidget.standardWorkRule(self.model.fileContent, False)
        elif plot == "Food Rule Timeline":
            self.standardPlotWidget.standardFoodRule(self.model.fileContent, False)
        elif plot == "Shelter Rule Timeline":
            self.standardPlotWidget.standardShelterRule(self.model.fileContent, False)
        elif plot == "Voting Rule Timeline":
            self.standardPlotWidget.standardVotingRule(self.model.fileContent, False)
        elif plot == "Maximum Punishment Distribution":
            self.standardPlotWidget.standardPunishmentRulePie(self.model.fileContent, False)
        elif plot == "Work Rule Distribution":
            self.standardPlotWidget.standardWorkRulePie(self.model.fileContent, False)
        elif plot == "Food Rule Distribution":
            self.standardPlotWidget.standardFoodRulePie(self.model.fileContent, False)
        elif plot == "Shelter Rule Distribution":
            self.standardPlotWidget.standardShelterRulePie(self.model.fileContent, False)
        elif plot == "Voting Rule Distribution":
            self.standardPlotWidget.standardVotingRulePie(self.model.fileContent, False)

    def defaultEnergySlot(self):
        self.standardPlotWidget.defaultEnergyPlot(self.model.fileContent, False)

    def defaultShelterSlot(self):
        pass
        #self.standardPlotWidget.defaultShelterPlot(self.model.fileContent, False)

    def defaultFoodSlot(self):
        pass
        #self.standardPlotWidget.defaultFoodPlot(self.model.fileContent, False)

    def defaultEnergyBoxSlot(self):
        self.standardPlotWidget.defaultEnergyBoxPlot(self.model.fileContent, False)

    def defaultEgotismSlot(self):
        self.standardPlotWidget.defaultEgotismPlot(self.model.fileContent, False)

    def defaultSusceptibilitySlot(self):
        self.standardPlotWidget.defaultSusceptibilityPlot(self.model.fileContent, False)

    def defaultIdealismSlot(self):
        self.standardPlotWidget.defaultIdealismPlot(self.model.fileContent, False)

    def defaultFairnessSlot(self):
        self.standardPlotWidget.defaultFairnessPlot(self.model.fileContent, False)

    def defaultPlaceholderSlot(self):
        self.standardPlotWidget.defaultTestPlot(self.model.fileContent, False)

        

def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon("./build/icon.png"))
    MainWindow = QtWidgets.QMainWindow()
    ui = MainWindowUiClass()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
