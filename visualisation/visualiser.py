import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
from matplotlib.offsetbox import AnchoredOffsetbox, TextArea, HPacker, VPacker
import sys
from os import remove as DeleteFile
import argparse
from zipfile import ZipFile

parser = argparse.ArgumentParser()

parser.add_argument('csv', help="input csv filepath from simulation")
parser.add_argument('zip', help="output zip filepath for plots")

args = parser.parse_args()

if not args.csv.endswith(".csv"):
    sys.exit("invalid input file type")

outFile = args.zip

if not outFile.endswith(".zip"):
    outFile += ".zip"

data = pd.read_csv(args.csv)

plot = plt.figure()
axes = plt.subplot(111)

plotNames = []

temp = data.filter(regex="Energy$", axis=1)
averageColumn = temp.mean(axis=1)
data["Average Energy"] = averageColumn

#egotism average
temp = data.filter(regex="Egotism$", axis=1)
averageColumn = temp.mean(axis=1)
data["Average Egotism"] = averageColumn

#susceptibility average
temp = data.filter(regex="Susceptibility$", axis=1)
averageColumn = temp.mean(axis=1)
data["Average Susceptibility"] = averageColumn

#idealism average
temp = data.filter(regex="Idealism$", axis=1)
averageColumn = temp.mean(axis=1)
data["Average Idealism"] = averageColumn

#fairness average
temp = data.filter(regex="Fairness$", axis=1)
averageColumn = temp.mean(axis=1)
data["Average Fairness"] = averageColumn

with ZipFile(outFile, "w") as zip:

    ######################### dead agent/energy plot ####################################

    energy = data.filter(regex="Energy$", axis=1)
    energy.apply(lambda x: axes.scatter(x.index+1, x, c='g', marker="x"))
    energy["Average"] = data["Average Energy"]
    axes.plot(data["CurrentDay"], energy["Average"], color='blue')
    axes.set_ylim(0,100)
    ybox1 = TextArea("Energy: ", textprops=dict(color="k", rotation=90,ha='left',va='bottom'))
    ybox2 = TextArea("Individual/",     textprops=dict(color="g", rotation=90,ha='left',va='bottom'))
    ybox3 = TextArea("Average", textprops=dict(color="b", rotation=90,ha='left',va='bottom'))

    ybox = VPacker(children=[ybox3, ybox2, ybox1],align="bottom", pad=0, sep=2)

    anchored_ybox = AnchoredOffsetbox(loc=8, child=ybox, pad=0., frameon=False, bbox_to_anchor=(-0.08, 0.3), 
                                bbox_transform=axes.transAxes, borderpad=0.)
    axes.add_artist(anchored_ybox)
    axes.set_xlabel("Day")
    axes.set_title('Average Agent Energy with Number of Dead Agents')

    deadAxes = axes.twinx()
    dead = data.filter(regex="Alive$", axis=1)
    dead["Number Dead"] = dead.isnull().sum(axis=1)
    deadAxes.plot(data["CurrentDay"], dead["Number Dead"], color='red')
    deadAxes.set_ylabel("Number of Dead Agents", color='red')
    deadAxes.set_ylim(0)

    fig = (plot, "averageEnergy.png")
    fig[0].savefig(fig[1])
    zip.write(fig[1])
    plotNames.append(fig[1])

    ############## energy distribution plot ##############################

    plot.clear()
    axes = plt.subplot(111)

    filtered_col = []

    energy = data.filter(regex="Energy$", axis=1)
    for x in range(len(energy.T.columns)):
        col = energy.T[x]
        filtered_col.append(col.dropna())

    axes.boxplot(filtered_col, vert=True, patch_artist=True)

    axes.set_title('Agent Energy Distribution')

    # adding horizontal grid lines
    axes.yaxis.grid(True)
    axes.set_xlabel('Day')
    axes.set_ylabel('Agent Energy')
    axes.set_ylim(0, 100)

    fig = (plot, "boxPlotEnergy.png")
    fig[0].savefig(fig[1])
    zip.write(fig[1])
    plotNames.append(fig[1])

    ################### egotism plot #####################################
    
    plot.clear()
    axes = plt.subplot(111)

    axes.plot(data["CurrentDay"], data["Average Egotism"], color='blue')
    axes.set_ylim(0,1)
    axes.set_xlabel("Day")
    axes.set_ylabel("Egotism")
    axes.set_title("Average Agent Egotism")

    fig = (plot, "egotism.png")
    fig[0].savefig(fig[1])
    zip.write(fig[1])
    plotNames.append(fig[1])

    ################### Susceptibilty plot #####################################

    plot.clear()
    axes = plt.subplot(111)

    axes.plot(data["CurrentDay"], data["Average Susceptibility"], color='blue')
    axes.set_ylim(0,1)
    axes.set_xlabel("Day")
    axes.set_ylabel("Susceptibility")
    axes.set_title("Average Agent Susceptibility")

    fig = (plot, "susceptibility.png")
    fig[0].savefig(fig[1])
    zip.write(fig[1])
    plotNames.append(fig[1])

    ################### Idealism plot #####################################

    plot.clear()
    axes = plt.subplot(111)

    axes.plot(data["CurrentDay"], data["Average Idealism"], color='blue')
    axes.set_ylim(0,1)
    axes.set_xlabel("Day")
    axes.set_ylabel("Idealism")
    axes.set_title("Average Agent Idealism")

    fig = (plot, "idealism.png")
    fig[0].savefig(fig[1])
    zip.write(fig[1])
    plotNames.append(fig[1])

    ################### Fairness plot #####################################

    plot.clear()
    axes = plt.subplot(111)

    filtered_col = []

    fairness = data.filter(regex="Fairness$", axis=1)
    for x in range(len(fairness.T.columns)):
        col = fairness.T[x]
        filtered_col.append(col.dropna())

    axes.boxplot(filtered_col, vert=True, patch_artist=True)

    axes.set_title('Agent Fairness Distribution')

    # adding horizontal grid lines
    axes.yaxis.grid(True)
    axes.set_xlabel('Day')
    axes.set_ylabel('Agent Fairness')

    fig = (plot, "fairness.png")
    fig[0].savefig(fig[1])
    zip.write(fig[1])
    plotNames.append(fig[1])

for plot in plotNames:
    DeleteFile(plot)