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

energyDayThreshold = 100

parser = argparse.ArgumentParser()

parser.add_argument('numRuns', help="number of sim runs")

args = parser.parse_args()

numRuns = int(args.numRuns)

def my_autopct(pct):
    return ('%.1f%%' % pct) if pct > 5 else ''

for k in range(0, numRuns):
    inputPath = os.path.join('..', 'csv', 'test' + str(k) + '.csv')
    data = pd.read_csv(inputPath)

    simulationDays = len(data.index)

    plot = plt.figure()
    axes = plt.subplot(111)

    plotNames = []

    #energy average
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
    temp = data.filter(regex="Infamy$", axis=1)
    averageColumn = temp.mean(axis=1)
    data["Average Infamy"] = averageColumn

    outName = os.path.join('..', 'csv', str(k) + '.zip')
    with ZipFile(outName, "w") as zip:

        ######################### crime rate plot #####################

        plot.clear()
        axes = plt.subplot(111)

        crimes = data.filter(regex="LastCrimeDate$", axis=1)
        agentNum = len(crimes.columns)
        crimes["Number of Crimes"] = 0

        for i in crimes.columns:
            crimes["Number of Crimes"] = np.where((data["CurrentDay"] - crimes[i] == 1) & (i != "Number of Crimes") & (crimes[i] != -1), 
                                                    crimes["Number of Crimes"]+1, crimes["Number of Crimes"])

        dead = data.filter(regex="Alive$", axis=1)
        crimes["Number Dead"] = dead.isnull().sum(axis=1)
        crimes["Crime Rate"] = crimes["Number of Crimes"]/(agentNum - crimes["Number Dead"])

        axes.plot(data["CurrentDay"], crimes["Crime Rate"], color='#66b3ff')
        axes.set_xlabel("Day")
        axes.set_ylabel("Crimes Committed per Person", color='#66b3ff')
        axes.set_title("Crime Rate per Person")

        deadAxes = axes.twinx()
        deadAxes.plot(data["CurrentDay"], crimes["Number Dead"], color='#ff9999')
        deadAxes.set_ylabel("Number of Dead Agents", color='#ff9999')
        deadAxes.set_ylim(0)

        fig = (plot, "crimeRate" + str(k) + ".png")
        fig[0].savefig(fig[1])
        zip.write(fig[1])
        plotNames.append(fig[1])

        ######################### crime raw plot ######################

        plot.clear()
        axes = plt.subplot(111)

        crimes = data.filter(regex="LastCrimeDate$", axis=1)
        crimes["Number of Crimes"] = 0

        for i in crimes.columns:
            crimes["Number of Crimes"] = np.where((data["CurrentDay"] - crimes[i] == 1) & (i != "Number of Crimes") & (crimes[i] != -1), 
                                                    crimes["Number of Crimes"]+1, crimes["Number of Crimes"])

        axes.plot(data["CurrentDay"], crimes["Number of Crimes"], color='#66b3ff')
        axes.set_xlabel("Day")
        axes.set_title("Crimes Committed per Day")

        fig = (plot, "crimeRaw" + str(k) + ".png")
        fig[0].savefig(fig[1])
        zip.write(fig[1])
        plotNames.append(fig[1])

        ######################### ISE plot ############################

        plot.clear()
        axes = plt.subplot(111)

        axes.plot(data["CurrentDay"], data["Average Egotism"], color='#66b3ff')
        axes.plot(data["CurrentDay"], data["Average Idealism"], color='#99ff99')
        axes.plot(data["CurrentDay"], data["Average Susceptibility"], color='#ff9999')
        axes.set_xlabel("Day")
        axes.legend()

        fig = (plot, "ISE" + str(k) + ".png")
        fig[0].savefig(fig[1])
        zip.write(fig[1])
        plotNames.append(fig[1])

        ######################### dead agent/energy plot ####################################

        plot.clear()
        axes = plt.subplot(111)

        energy = data.filter(regex="Energy$", axis=1)
        if len(energy) < energyDayThreshold:
            energy.apply(lambda x: axes.scatter(x.index+1, x, c='g', marker="x"))
        energy["Average"] = data["Average Energy"]
        axes.plot(data["CurrentDay"], energy["Average"], color='blue')
        axes.set_ylim(0,100)
        ybox1 = TextArea("Energy: ", textprops=dict(color="k", rotation=90,ha='left',va='bottom'))
        if len(energy) < energyDayThreshold:
            ybox2 = TextArea("Individual/",     textprops=dict(color="g", rotation=90,ha='left',va='bottom'))
        ybox3 = TextArea("Average", textprops=dict(color="b", rotation=90,ha='left',va='bottom'))

        if len(energy) < energyDayThreshold:
            ybox = VPacker(children=[ybox3, ybox2, ybox1],align="bottom", pad=0, sep=2)
        else:
            ybox = VPacker(children=[ybox3, ybox1],align="bottom", pad=0, sep=2)

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

        fig = (plot, "averageEnergy" + str(k) + ".png")
        fig[0].savefig(fig[1])
        zip.write(fig[1])
        plotNames.append(fig[1])

        ############## energy distribution plot ##############################

        plot.clear()
        axes = plt.subplot(111)

        energy = data.filter(regex="Energy$", axis=1)
        energy.drop(["Average Energy"], axis=1)
        day = data["CurrentDay"]        

        while len(energy) > 300:
            day = day[::2]
            energy = energy[::2]

        axes.plot(day, energy.quantile(0.9, axis=1), color="indianred")
        #axes.plot(day, energy.quantile(0.8, axis=1), color="orange")
        axes.plot(day, energy.quantile(0.7, axis=1), color="gold")
        axes.plot(day, energy.quantile(0.5, axis=1), color="lightgreen")
        axes.plot(day, energy.quantile(0.3, axis=1), color="deepskyblue")
        #axes.plot(day, energy.quantile(0.2, axis=1), color="plum")
        axes.plot(day, energy.quantile(0.1, axis=1), color="mediumpurple")
        axes.legend()

        axes.set_title('Agent Energy Distribution')

        # adding horizontal grid lines
        axes.set_xlabel('Day')
        axes.set_ylabel('Energy')
        axes.set_ylim(0, 100)


        fig = (plot, "energyDistribution" + str(k) + ".png")
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

        fig = (plot, "egotism" + str(k) + ".png")
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

        fig = (plot, "susceptibility" + str(k) + ".png")
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

        fig = (plot, "idealism" + str(k) + ".png")
        fig[0].savefig(fig[1])
        zip.write(fig[1])
        plotNames.append(fig[1])

        ################### Fairness plot #####################################

        plot.clear()
        axes = plt.subplot(111)

        fairness = data.filter(regex="Fairness$", axis=1)
        fairness.drop(["Average Fairness"], axis=1)
        day = data["CurrentDay"]        

        while len(fairness) > 300:
            day = day[::2]
            fairness = fairness[::2]

        axes.plot(day, fairness.quantile(0.9, axis=1), color="indianred")
        #axes.plot(day, fairness.quantile(0.8, axis=1), color="orange")
        axes.plot(day, fairness.quantile(0.7, axis=1), color="gold")
        axes.plot(day, fairness.quantile(0.5, axis=1), color="lightgreen")
        axes.plot(day, fairness.quantile(0.3, axis=1), color="deepskyblue")
        #axes.plot(day, fairness.quantile(0.2, axis=1), color="plum")
        axes.plot(day, fairness.quantile(0.1, axis=1), color="mediumpurple")
        axes.legend()

        axes.set_title('Agent Fairness Distribution')

        # adding horizontal grid lines
        axes.set_xlabel('Day')
        axes.set_ylabel('Fairness')

        fig = (plot, "fairnessDistribution" + str(k) + ".png")
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

        fig = (plot, "infamy" + str(k) + ".png")
        fig[0].savefig(fig[1])
        zip.write(fig[1])
        plotNames.append(fig[1])

        ####################### infamy box plot ###############################

        plot.clear()
        axes = plt.subplot(111)

        infamy = data.filter(regex="Infamy$", axis=1)
        infamy.drop(["Average Infamy"], axis=1)
        day = data["CurrentDay"]        

        while len(infamy) > 300:
            day = day[::2]
            infamy = infamy[::2]

        axes.plot(day, infamy.quantile(0.9, axis=1), color="indianred")
        #axes.plot(day, infamy.quantile(0.8, axis=1), color="orange")
        axes.plot(day, infamy.quantile(0.7, axis=1), color="gold")
        axes.plot(day, infamy.quantile(0.5, axis=1), color="lightgreen")
        axes.plot(day, infamy.quantile(0.3, axis=1), color="deepskyblue")
        #axes.plot(day, infamy.quantile(0.2, axis=1), color="plum")
        axes.plot(day, infamy.quantile(0.1, axis=1), color="mediumpurple")
        axes.legend()

        axes.set_title('Agent Infamy Distribution')

        # adding horizontal grid lines
        axes.set_xlabel('Day')
        axes.set_ylabel('Infamy')
        axes.set_ylim(0)


        fig = (plot, "infamyDistribution" + str(k) + ".png")
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

        axes.broken_barh(socialism, (13,5), facecolors='#66b3ff')
        axes.broken_barh(meritocracy, (23,5), facecolors='#99ff99')
        axes.broken_barh(oligarchy, (33,5), facecolors='#ffcc99')
        axes.broken_barh(random, (43,5), facecolors='#ff9999')
        axes.set_xlabel("Day")
        axes.set_ylabel("Shelter Rule")
        axes.set_title("Shelter Rule During Simulation")
        axes.set_ylim(5, 55)
        axes.set_yticks([15, 25, 35, 45])
        axes.set_yticklabels(["Socialism", "Meritocracy", "Oligarchy", "Random"])
        plt.tight_layout()

        fig = (plot, "shelterRule" + str(k) + ".png")
        fig[0].savefig(fig[1])
        zip.write(fig[1])
        plotNames.append(fig[1])

        ################### Shelter rule pie #############################

        plot.clear()
        axes = plt.subplot(111)

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
        
        axes.pie(sizes, colors = colors, labels=labels, autopct=my_autopct, startangle=90, pctdistance=0.85, explode = explode)
        centre_circle = matplotlib.patches.Circle((0,0),0.70,fc='white')
        axes.add_patch(centre_circle)
        axes.axis('equal')
        axes.set_title('Shelter Rule Proportions')

        fig = (plot, "shelterRulePie" + str(k) + ".png")
        fig[0].savefig(fig[1])
        zip.write(fig[1])
        plotNames.append(fig[1])

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

        axes.broken_barh(socialism, (13,5), facecolors='#66b3ff')
        axes.broken_barh(meritocracy, (23,5), facecolors='#99ff99')
        axes.broken_barh(oligarchy, (33,5), facecolors='#ffcc99')
        axes.broken_barh(communism, (43,5), facecolors='#ff9999')
        axes.set_xlabel("Day")
        axes.set_ylabel("Food Rule")
        axes.set_title("Food Rule During Simulation")
        axes.set_ylim(5, 55)
        axes.set_yticks([15, 25, 35, 45])
        axes.set_yticklabels(["Socialism", "Meritocracy", "Oligarchy", "Communism"])
        plt.tight_layout()

        fig = (plot, "foodRule" + str(k) + ".png")
        fig[0].savefig(fig[1])
        zip.write(fig[1])
        plotNames.append(fig[1])

        ######################### food rule pie ##################################

        plot.clear()
        axes = plt.subplot(111)

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
        
        axes.pie(sizes, colors = colors, labels=labels, autopct=my_autopct, startangle=90, pctdistance=0.85, explode = explode)
        centre_circle = matplotlib.patches.Circle((0,0),0.70,fc='white')
        axes.add_patch(centre_circle)
        axes.axis('equal')
        axes.set_title('Food Rule Proportions')

        fig = (plot, "foodRulePie" + str(k) + ".png")
        fig[0].savefig(fig[1])
        zip.write(fig[1])
        plotNames.append(fig[1])

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

        axes.broken_barh(strongest, (13,5), facecolors='#66b3ff')
        axes.broken_barh(byChoice, (23,5), facecolors='#99ff99')
        axes.broken_barh(everyone, (33,5), facecolors='#ff9999')
        axes.set_xlabel("Day")
        axes.set_ylabel("Work Rule")
        axes.set_title("Work Rule During Simulation")
        axes.set_ylim(5, 45)
        axes.set_yticks([15, 25, 35])
        axes.set_yticklabels(["Strongest", "By Choice", "Everyone"])
        plt.tight_layout()

        fig = (plot, "workRule" + str(k) + ".png")
        fig[0].savefig(fig[1])
        zip.write(fig[1])
        plotNames.append(fig[1])

        ############################## work rule pie #############################

        plot.clear()
        axes = plt.subplot(111)

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
        
        axes.pie(sizes, colors = colors, labels=labels, autopct=my_autopct, startangle=90, pctdistance=0.85, explode = explode)
        centre_circle = matplotlib.patches.Circle((0,0),0.70,fc='white')
        axes.add_patch(centre_circle)
        axes.axis('equal')
        axes.set_title('Work Rule Proportions')

        fig = (plot, "workRulePie" + str(k) + ".png")
        fig[0].savefig(fig[1])
        zip.write(fig[1])
        plotNames.append(fig[1])

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
        
        axes.broken_barh(borda, (13,5), facecolors='#66b3ff')
        axes.broken_barh(approval, (23,5), facecolors='#99ff99')
        axes.broken_barh(instantRunoff, (33,5), facecolors='#ffcc99')
        axes.broken_barh(plurality, (43,5), facecolors='#ff9999')
        axes.set_xlabel("Day")
        axes.set_ylabel("Voting Rule")
        axes.set_title("Voting Rule During Simulation")
        axes.set_ylim(5, 55)
        axes.set_yticks([15, 25, 35, 45])
        axes.set_yticklabels(["Borda", "Approval", "Instant Runoff", "Plurality"])
        plt.tight_layout()

        fig = (plot, "votingRule" + str(k) + ".png")
        fig[0].savefig(fig[1])
        zip.write(fig[1])
        plotNames.append(fig[1])

        ########################### voting rule pie ###############################

        plot.clear()
        axes = plt.subplot(111)

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
        
        axes.pie(sizes, colors = colors, labels=labels, autopct=my_autopct, startangle=90, pctdistance=0.85, explode = explode)
        centre_circle = matplotlib.patches.Circle((0,0),0.70,fc='white')
        axes.add_patch(centre_circle)
        axes.axis('equal')
        axes.set_title('Voting Rule Proportions')

        fig = (plot, "votingRulePie" + str(k) + ".png")
        fig[0].savefig(fig[1])
        zip.write(fig[1])
        plotNames.append(fig[1])

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
        
        axes.broken_barh(noFoodAndShelter, (13,5), facecolors='#66b3ff')
        axes.broken_barh(increment, (23,5), facecolors='#99ff99')
        axes.broken_barh(decrement, (33,5), facecolors='#ffcc99')
        axes.broken_barh(exile, (43,5), facecolors='#ff9999')
        axes.set_xlabel("Day")
        axes.set_ylabel("Maximum Punishment")
        axes.set_title("Maximum Punishment During Simulation")
        axes.set_ylim(5, 55)
        axes.set_yticks([15, 25, 35, 45])
        axes.set_yticklabels(["No Food and Shelter", "Increment", "Decrement", "Exile"])
        plt.tight_layout()

        fig = (plot, "punishmentRule" + str(k) + ".png")
        fig[0].savefig(fig[1])
        zip.write(fig[1])
        plotNames.append(fig[1])

        ############################# punishment rule pie ##########################

        plot.clear()
        axes = plt.subplot(111)

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
            sizes.append(occurences.loc["No Food and Shelter"])
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
        
        axes.pie(sizes, colors = colors, labels=labels, autopct=my_autopct, startangle=90, pctdistance=0.85, explode = explode)
        centre_circle = matplotlib.patches.Circle((0,0),0.70,fc='white')
        axes.add_patch(centre_circle)
        axes.axis('equal')
        axes.set_title('Maximum Punishment Proportions')

        fig = (plot, "punishmentRulePie" + str(k) + ".png")
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

        noneBar = axes.bar(data["CurrentDay"], none, 0.85, color="#ff9999")
        huntingBar = axes.bar(data["CurrentDay"], hunting, 0.85, bottom=none, color="#99ff99")
        buildingBar = axes.bar(data["CurrentDay"], building, 0.85, bottom=np.array(none)+np.array(hunting), color="#66b3ff")
        axes.set_ylabel("Number of Agents")
        axes.set_xlabel("Day")
        axes.set_title("Agent Activity Breakdown per Day")
        axes.legend((noneBar[0], huntingBar[0], buildingBar[0]), ("None", "Hunting", "Building"))

        fig = (plot, "activityBreakdown" + str(k) + ".png")
        fig[0].savefig(fig[1])
        zip.write(fig[1])
        plotNames.append(fig[1])

    for plot in plotNames:
        DeleteFile(plot)
