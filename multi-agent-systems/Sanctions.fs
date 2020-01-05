module Sanctions

open Types
open Config

// Breakable Rules
// 1) Agents not sharing food
// 2) Agents not doing as told

// Calculate the ideal allocation according to rule
// This means returning expected energy gain and a job allocation
// Since sanction does not check for job type as long as there is a job
// Actual job allocation does not matter
let idealAllocation (world: WorldState) (agents: Agent list) (totalFoodShared: float): float list * Activity list = 

    let totalEnergy = 
        agents
        |> List.map (fun el -> el.Energy)
        |> List.sum

    let totalEffort =
        agents
        |> List.map (fun el -> snd el.TodaysActivity)
        |> List.sum

    let targetEnergyList =
        if totalFoodShared <= 0.0 then
            List.map (fun _ -> 0.0) [0..(List.length agents-1)]
        else    
            let numAgents = List.length agents |> float
            agents
            |> List.map (fun el ->
                match world.CurrentFoodRule with
                | Communism -> totalFoodShared / numAgents
                | FoodRule.Socialism -> totalFoodShared * (1.0 - el.Energy / totalEnergy) / (numAgents - 1.0)
                | FoodRule.Meritocracy -> totalFoodShared * (snd el.TodaysActivity) / totalEffort
                | FoodRule.Oligarchy -> 
                    let maxAssignmentPerAgent = totalFoodShared / numAgents * MinimumFoodForOligarchy
                    el.Energy / totalEnergy * totalFoodShared * (1.0 - MinimumFoodForOligarchy) + maxAssignmentPerAgent
            )

    let targetWorkStatus = 
        agents
        |> List.map (fun el ->
            match world.CurrentWorkRule with
            | Everyone -> 
                BUILDING // Indicate that agent will have activity
            | Strongest -> 
                if el.Energy >= WorkExemptionThreshold then BUILDING else NONE
            | _ -> NONE // No expectation on working
        )

    (targetEnergyList, targetWorkStatus)

// Allocate food according to precomputed assignment
let allocateFood (targetEnergyList: float list) (agents: Agent list): Agent list = 
    List.zip agents targetEnergyList
    |> List.map (fun (agent, energy) ->
        if agent.AccessToFood = true
        then 
            let newGain = min (agent.Gain + energy) (AgentMaxEnergy - agent.Energy) // Limit gain to the current energy headroom
            {agent with Energy = agent.Energy + newGain;
                            Gain = newGain}
        else {agent with Gain = 0.0}
    )


// Update at end-of-day
let infamyDecay (world: WorldState) (agents: Agent list) : Agent list =
    agents
    // Halve infamy every 8 days
    |> List.map (fun el ->
        if world.CurrentDay <> el.LastCrimeDate then
            match (world.CurrentDay - el.LastCrimeDate) % 8 with
            | 0 -> {el with Infamy = el.Infamy / 2.0 |> floor}
            | _ -> el
        else el
    )

// Sanction (change accessibility state) based on rules
let sanction (world: WorldState) (agents: Agent list) : Agent list = 
    agents
    |> List.map (fun el ->
        if el.LastCrimeDate = world.CurrentDay then
            if el.Infamy <= 0.2 then {el with AccessToShelter = el.AccessToShelter;
                                                AccessToFood = true}
            elif el.Infamy <= 0.5 then {el with AccessToShelter = None;
                                                AccessToFood = true}
            elif el.Infamy <= 0.9 then {el with AccessToFood = false;
                                                AccessToShelter = None}
            else 
                match world.CurrentMaxPunishment with 
                | NoFoodAndShelter -> {el with AccessToFood = false;
                                                AccessToShelter = None}
                | Exile -> {el with Alive = false}
                | _ -> failwith "Invalid maximum punishment setting"
        else {el with AccessToShelter = el.AccessToShelter;
                        AccessToFood = true;
                        Energy = max 0.0 el.Energy - BasePenalty}
    )


// Detect crime actions based on probability of discovery
let detectCrime (world: WorldState) (expectedEnergyGain: float list) (expectedWorkType: Activity list) (agents: Agent list) : Agent list * WorldState =
   
    let mutable numCrimes = world.NumberOfCrimes
    let rand = new System.Random()
    let checkFoodAllocation (agents: Agent list) = 
        List.zip agents expectedEnergyGain
        |> List.map (fun (agent, gain) ->
            if agent.Gain > gain && rand.NextDouble() < CrimeDiscoveryRate 
                then numCrimes <- numCrimes + 1
                     {agent with Infamy = min 1.0 agent.Infamy + InfamyStep; LastCrimeDate = world.CurrentDay}
            else agent
        )

    let checkTaskExecution (agents: Agent list) = 
        List.zip agents expectedWorkType
        |> List.map (fun (agent, job) ->
            if fst agent.TodaysActivity = NONE && job <> NONE && rand.NextDouble() < CrimeDiscoveryRate 
                then numCrimes <- numCrimes + 1
                     {agent with Infamy = min 1.0 agent.Infamy + InfamyStep; LastCrimeDate = world.CurrentDay}
            else agent
        )

    (agents |> checkFoodAllocation |> checkTaskExecution, {world with NumberOfCrimes = numCrimes})

