module CSVDump

open System.IO
open Config
open Types

//// csv file headings
let headings = "CurrentDay,Buildings,CurrentChair,TimeToNewChair,CurrentShelterRule,CurrentVotingRule,CurrentFoodRule,CurrentWorkRule,CurrentMaxPunishment,CurrentSanctionStepSize,NumHare,NumStag,NumberOfCrimes,BuildingRewardPerDay,HuntingRewardPerDay,BuildingAverageTotalReward,HuntingAverageTotalReward,"

// agent headings duplicated for each agent
let agentHeadings = "[ID]Susceptibility,[ID]Idealism,[ID]Egotism,[ID]Fairness,[ID]Gain,[ID]EnergyDepreciation,[ID]EnergyConsumed,[ID]Infamy,[ID]Energy,[ID]HuntedFood,[ID]Today'sActivity,[ID]AccessToShelter,[ID]SelfConfidence,[ID]Today'sHuntOption,[ID]FoodSharing,[ID]LastCrimeDate,[ID]AccessToFood,[ID]Alive,"

let csvdump (world : WorldState) (unsortedAgents : Agent list) (csvwriter : StreamWriter) : WorldState = 

    let agents = List.sortBy (fun elem -> elem.ID) unsortedAgents
    let totalFairness = List.sumBy (fun elem -> elem.Gain) agents + rb * (float numAgents) - 2.0 * List.sumBy (fun elem -> elem.EnergyDeprecation) agents - List.sumBy (fun elem -> elem.EnergyConsumed) agents

    // world state dump
    csvwriter.Write("\n")
    csvwriter.Write(world.CurrentDay)
    csvwriter.Write(",")
    csvwriter.Write(world.Buildings)
    csvwriter.Write(",")
    let currentChair = match world.CurrentChair with
                       | Some x -> string x.ID
                       | _ -> ""
    csvwriter.Write(currentChair)
    csvwriter.Write(",")
    csvwriter.Write(world.TimeToNewChair)
    csvwriter.Write(",")
    csvwriter.Write(world.CurrentShelterRule)
    csvwriter.Write(",")
    csvwriter.Write(world.CurrentVotingRule)
    csvwriter.Write(",")
    csvwriter.Write(world.CurrentFoodRule)
    csvwriter.Write(",")
    csvwriter.Write(world.CurrentWorkRule)
    csvwriter.Write(",")
    csvwriter.Write(world.CurrentMaxPunishment)
    csvwriter.Write(",")
    csvwriter.Write(world.CurrentSanctionStepSize)
    csvwriter.Write(",")
    csvwriter.Write(world.NumHare)
    csvwriter.Write(",")
    csvwriter.Write(world.NumStag)
    csvwriter.Write(",")
    //let currentRuleSet = List.map (fun (x,y,z) -> [x;y;z]) world.CurrentRuleSet
    //csvwriter.Write(currentRuleSet)
    //csvwriter.Write(",")
    //csvwriter.Write(world.AllRules)
    //csvwriter.Write(",")
    csvwriter.Write(world.NumberOfCrimes)
    csvwriter.Write(",")
    csvwriter.Write(world.BuildingRewardPerDay)
    csvwriter.Write(",")
    csvwriter.Write(world.HuntingRewardPerDay)
    csvwriter.Write(",")
    csvwriter.Write(world.BuildingAverageTotalReward)
    csvwriter.Write(",")
    csvwriter.Write(world.HuntingAverageTotalReward)
    csvwriter.Write(",")
    //csvwriter.Write(world.S)
    //csvwriter.Write(",")
    //csvwriter.Write(world.ShuntingEnergySplit)
    //csvwriter.Write(",")

    // dump for a single agent
    let agentDump _ (agent : Agent) : WorldState =

        if (agent.Alive) then

            let indivFairness = agent.Gain + rb - 2.0 * agent.EnergyDeprecation - agent.EnergyConsumed

            csvwriter.Write(agent.Susceptibility)
            csvwriter.Write(",")
            csvwriter.Write(agent.Idealism)
            csvwriter.Write(",")
            csvwriter.Write(agent.Egotism)
            csvwriter.Write(",")
            csvwriter.Write(indivFairness / totalFairness)
            csvwriter.Write(",")
            csvwriter.Write(agent.Gain)
            csvwriter.Write(",")
            csvwriter.Write(agent.EnergyDeprecation)
            csvwriter.Write(",")
            csvwriter.Write(agent.EnergyConsumed)
            csvwriter.Write(",")
            csvwriter.Write(agent.Infamy)
            csvwriter.Write(",")
            csvwriter.Write(agent.Energy)
            csvwriter.Write(",")
            csvwriter.Write(agent.HuntedFood)
            csvwriter.Write(",")
            csvwriter.Write(fst agent.TodaysActivity)
            csvwriter.Write(",")
            csvwriter.Write(agent.AccessToShelter)
            csvwriter.Write(",")
            csvwriter.Write(agent.SelfConfidence)
            csvwriter.Write(",")
            csvwriter.Write(agent.TodaysHuntOption)
            csvwriter.Write(",")
            //csvwriter.Write(agent.R)
            //csvwriter.Write(",")
            //csvwriter.Write(agent.RhuntingEnergySplit)
            //csvwriter.Write(",")
            //csvwriter.Write(agent.Rsharing)
            //csvwriter.Write(",")
            csvwriter.Write(agent.FoodShared)
            csvwriter.Write(",")
            csvwriter.Write(agent.LastCrimeDate)
            csvwriter.Write(",")
            csvwriter.Write(agent.AccessToFood)
            csvwriter.Write(",")
            csvwriter.Write(agent.Alive)
            csvwriter.Write(",")
        else 
            csvwriter.Write(",,,,,,,,,,,,,,,,,,")
        
        world

    // single agent dump iterated across list of agents
    List.fold agentDump world agents