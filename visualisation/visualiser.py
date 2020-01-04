import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import numpy as np
from matplotlib.offsetbox import AnchoredOffsetbox, TextArea, HPacker, VPacker
import sys
from os import remove as DeleteFile
import argparse
from zipfile import ZipFile
import os.path
import os

parser = argparse.ArgumentParser()

parser.add_argument('numRuns', help="number of sim runs")

args = parser.parse_args()

numRuns = int(args.numRuns)

for i in range(0, numRuns):
    inputPath = os.path.join('..', 'csv', 'test' + str(i) + '.csv')
    data = pd.read_csv(inputPath)

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

    #infamy average
    temp = data.filter(regex="Fairness$", axis=1)
    averageColumn = temp.mean(axis=1)
    data["Average Infamy"] = averageColumn

    outName = os.path.join('..', 'csv', str(i) + '.zip')
    with ZipFile(outName, "w") as zip:

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

        ###################### Infamy plot ####################################

        plot.clear()
        axes = plt.subplot(111)

        axes.plot(data["CurrentDay"], data["Average Infamy"], color='blue')
        axes.set_ylim(0,1)
        axes.set_xlabel("Day")
        axes.set_ylabel("Infamy")
        axes.set_title("Average Agent Infamy")

        fig = (plot, "infamy.png")
        fig[0].savefig(fig[1])
        zip.write(fig[1])
        plotNames.append(fig[1])

        ######################## Shelter rule plot ############################

        plot.clear()
        axes = plt.subplot(111)

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

        axes.broken_barh(socialism, (13,5), facecolors='tab:blue')
        axes.broken_barh(meritocracy, (23,5), facecolors='tab:green')
        axes.broken_barh(oligarchy, (33,5), facecolors='tab:orange')
        axes.broken_barh(random, (43,5), facecolors='tab:red')
        axes.set_xlabel("Day")
        axes.set_ylabel("Shelter Rule")
        axes.set_title("Shelter Rule During Simulation")
        axes.set_ylim(5, 55)
        axes.set_yticks([15, 25, 35, 45])
        axes.set_yticklabels(["Socialism", "Meritocracy", "Oligarchy", "Random"])
        plt.tight_layout()

        fig = (plot, "shelterRule.png")
        fig[0].savefig(fig[1])
        zip.write(fig[1])
        plotNames.append(fig[1])

        ################### Shelter rule pie #############################

        ################### Food rule plot ###############################

        plot.clear()
        axes = plt.subplot(111)

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

        axes.broken_barh(socialism, (13,5), facecolors='tab:blue')
        axes.broken_barh(meritocracy, (23,5), facecolors='tab:green')
        axes.broken_barh(oligarchy, (33,5), facecolors='tab:orange')
        axes.broken_barh(communism, (43,5), facecolors='tab:red')
        axes.set_xlabel("Day")
        axes.set_ylabel("Food Rule")
        axes.set_title("Food Rule During Simulation")
        axes.set_ylim(5, 55)
        axes.set_yticks([15, 25, 35, 45])
        axes.set_yticklabels(["Socialism", "Meritocracy", "Oligarchy", "Communism"])
        plt.tight_layout()

        fig = (plot, "foodRule.png")
        fig[0].savefig(fig[1])
        zip.write(fig[1])
        plotNames.append(fig[1])

        ######################### food rule pie ##################################

        ######################### work rule plot #################################

        plot.clear()
        axes = plt.subplot(111)

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

        axes.broken_barh(strongest, (13,5), facecolors='tab:blue')
        axes.broken_barh(byChoice, (23,5), facecolors='tab:green')
        axes.broken_barh(everyone, (33,5), facecolors='tab:red')
        axes.set_xlabel("Day")
        axes.set_ylabel("Work Rule")
        axes.set_title("Work Rule During Simulation")
        axes.set_ylim(5, 45)
        axes.set_yticks([15, 25, 35])
        axes.set_yticklabels(["Strongest", "By Choice", "Everyone"])
        plt.tight_layout()

        fig = (plot, "workRule.png")
        fig[0].savefig(fig[1])
        zip.write(fig[1])
        plotNames.append(fig[1])

        ############################## work rule pie #############################

        ######################### voting rule plot ###############################

        plot.clear()
        axes = plt.subplot(111)

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
        
        axes.broken_barh(borda, (13,5), facecolors='tab:blue')
        axes.broken_barh(approval, (23,5), facecolors='tab:green')
        axes.broken_barh(instantRunoff, (33,5), facecolors='tab:orange')
        axes.broken_barh(plurality, (43,5), facecolors='tab:red')
        axes.set_xlabel("Day")
        axes.set_ylabel("Voting Rule")
        axes.set_title("Voting Rule During Simulation")
        axes.set_ylim(5, 55)
        axes.set_yticks([15, 25, 35, 45])
        axes.set_yticklabels(["Borda", "Approval", "Instant Runoff", "Plurality"])
        plt.tight_layout()

        fig = (plot, "votingRule.png")
        fig[0].savefig(fig[1])
        zip.write(fig[1])
        plotNames.append(fig[1])

        ########################### voting rule pie ###############################

        ##################### punishment rule plot ################################

        plot.clear()
        axes = plt.subplot(111)

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

        watch = data.iloc[-1]["CurrentMaxPunishment"]
        if watch == "Exile":
            exile.append((start, count))
        elif watch == "Increment":
            increment.append((start, count))
        elif watch == "Decrement":
            decrement.append((start, count))
        else:
            noFoodAndShelter.append((start, count))
        
        axes.broken_barh(noFoodAndShelter, (13,5), facecolors='tab:blue')
        axes.broken_barh(increment, (23,5), facecolors='tab:green')
        axes.broken_barh(decrement, (33,5), facecolors='tab:orange')
        axes.broken_barh(exile, (43,5), facecolors='tab:red')
        axes.set_xlabel("Day")
        axes.set_ylabel("Maximum Punishment")
        axes.set_title("Maximum Punishment During Simulation")
        axes.set_ylim(5, 55)
        axes.set_yticks([15, 25, 35, 45])
        axes.set_yticklabels(["No Food and Shelter", "Increment", "Decrement", "Exile"])
        plt.tight_layout()

        fig = (plot, "punishmentRule.png")
        fig[0].savefig(fig[1])
        zip.write(fig[1])
        plotNames.append(fig[1])

        ############################## activity breakdown ###############################

        plot.clear()
        axes = plt.subplot(111)

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

        noneBar = axes.bar(data["CurrentDay"], none, 0.85, color="tab:red")
        huntingBar = axes.bar(data["CurrentDay"], hunting, 0.85, bottom=none, color="tab:green")
        buildingBar = axes.bar(data["CurrentDay"], building, 0.85, bottom=np.array(none)+np.array(hunting), color="tab:blue")
        axes.set_ylabel("Number of Agents")
        axes.set_xlabel("Day")
        axes.set_title("Agent Activity Breakdown per Day")
        axes.legend((noneBar[0], huntingBar[0], buildingBar[0]), ("None", "Hunting", "Building"))

        fig = (plot, "activityBreakdown.png")
        fig[0].savefig(fig[1])
        zip.write(fig[1])
        plotNames.append(fig[1])

    for plot in plotNames:
        DeleteFile(plot)
