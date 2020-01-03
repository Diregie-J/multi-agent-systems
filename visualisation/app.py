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

    def filterPrint(self, msg):
        self.filterBrowser.append(msg)

    def refreshAll(self):
        self.addAgentPushButton.setEnabled(True)
        self.exportAllPushButton.setEnabled(True)
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

    #slots
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

    def browseSlot(self):
        #self.debugPrint("browse button pressed")
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
                        None,
                        "QFileDialog.getOpenFileName()",
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

    def exportAllSlot(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(None,
                                                'QFileDialog.getSaveFileName()',
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

    # default plots

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
        pass

        

def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MainWindowUiClass()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

main()
