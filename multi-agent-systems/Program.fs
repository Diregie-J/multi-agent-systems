module Program
open Types
open Decision
open Sanctions
open Hunt
open Build
open Config
open Duma
open Opinion
open System.IO
open Agent
open CSVDump
open System.Threading

[<EntryPoint>]
let main argv =
    Thread.CurrentThread.CurrentCulture <- System.Globalization.CultureInfo.InvariantCulture;
    // Agent parsing - test with command line args "--number-days -1 --number-profiles 7 --number-agents 24 [--number-runs 3]"
    let agents = Parsing.parse argv

    let printAgent (agent : Agent) =
        ("ID: ", agent.ID), ("Energy: ", agent.Energy), ("Susceptibility: ", agent.Susceptibility),
        ("Idealism: ", agent.Idealism), ("Egotism: ", agent.Egotism),
        ("Gain: ", agent.Gain), ("EnergyConsumed: ", agent.EnergyConsumed), ("EnergyDeprecation: ", agent.EnergyDeprecation),
        ("HuntedFood: ", agent.HuntedFood), ("Activity: ", agent.TodaysActivity), 
        ("ShelterAccess: ", agent.AccessToShelter), ("FoodShared: ", agent.FoodShared), ("HuntOption: ", agent.TodaysHuntOption),
        ("SelfConfidence: ", agent.SelfConfidence), ("LastCrimeDate: ", agent.LastCrimeDate), ("FoodAccess: ", agent.AccessToFood),
        ("Alive: ", agent.Alive), ("OverallRuleOpinion: ", agent.DecisionOpinions.Value.OverallRuleOpinion),
        ("OtherAgentsOpinion: ", List.map (fun (ag, opin) -> ag.ID, opin) agent.DecisionOpinions.Value.AllOtherAgentsOpinion)

    let printWorld (world : WorldState) =
        (("Buildings: ", world.Buildings), ("Time to new chair: ", world.TimeToNewChair), ("CurrentRules: ", world.CurrentRuleSet),
         ("CurrentDay: ", world.CurrentDay), ("CurrentChair: ", world.CurrentChair.Value.ID), ("NumHare: ", world.NumHare), ("NumStag: ", world.NumStag),
         ("AllRules: ", world.AllRules), ("TotalSanctions:", world.NumberOfCrimes))
        
    let currentWorld =
        {
            Buildings = List.Empty;
            TimeToNewChair = 5;
            CurrentShelterRule = Random;
            CurrentFoodRule = Communism;
            CurrentVotingRule = Borda;
            CurrentWorkRule = Everyone;
            CurrentMaxPunishment = Exile;
            ShelterTime = ruleTime;
            VoteTime = ruleTime;
            FoodTime = ruleTime;
            WorkTime = ruleTime;
            PunishmentTime = ruleTime;
            CurrentSanctionStepSize = 0.1;
            CurrentDay = 0;
            CurrentChair = None;
            NumHare = 15;
            NumStag = 15;
            NumberOfCrimes = 0;
            CurrentRuleSet = initialiseRuleSet;
            AllRules = initialiseAllRules;
            BuildingRewardPerDay = 0.0;
            HuntingRewardPerDay = 0.0;
            BuildingAverageTotalReward = 0.0;
            HuntingAverageTotalReward = 0.0;
            S = [0.5; 0.5; 0.5];
            ShuntingEnergySplit = List.init 11 (fun _ -> 0.5);
        }

    let updateEndOfDayState (agents: Agent list) (state: WorldState) : WorldState = 
        let updateNoneAgentStates (currentWorld: WorldState) : WorldState =
            {currentWorld with CurrentDay = currentWorld.CurrentDay + 1;
                                NumHare = currentWorld.NumHare + regenRate rabbosMeanRegenRate currentWorld.NumHare maxNumHare;
                                NumStag = currentWorld.NumStag + regenRate staggiMeanRegenRate currentWorld.NumStag maxNumStag}  // Regeneration
        
        let updateSocialGoodForWork (state: WorldState) : WorldState =
            let socialGood (prevVal: float) (activity: Activity) : float = 
                let targets = 
                    agents
                    |> List.filter (fun el -> fst el.TodaysActivity = activity)
                if targets = [] then prevVal    // If no agent carries out action, social good not changed
                else
                    targets
                    |> List.map (fun el -> el.Gain - 2.0 * el.EnergyConsumed - 2.0 * el.EnergyDeprecation)
                    |> List.sum
                    |> fun x -> x / (agents.Length |> float)

            let updatedS =
                List.zip [NONE; HUNTING; BUILDING] state.S
                |> List.map (fun (work, s) ->
                    work
                    |> socialGood s
                    |> getCumulativeAverage state.CurrentDay s
                )
                |> standardize

            {state with S = updatedS}
            
        let updateSocialGoodForHunters (state: WorldState) : WorldState =
            let socialGood (prevVal: float) (option: int) : float = 
                let targets = 
                    agents
                    |> List.filter (fun el -> el.TodaysHuntOption = option)
                
                if targets = [] then prevVal
                else
                    targets
                    |> List.map (fun el -> el.Gain - 2.0 * el.EnergyConsumed - 2.0 * el.EnergyDeprecation)
                    |> List.sum
                    |> fun x -> x / (agents.Length |> float)

            let updatedS =
                List.zip [for i in 0..10 -> i] state.ShuntingEnergySplit
                |> List.map (fun (option, s) ->
                    option
                    |> socialGood s
                    |> getCumulativeAverage state.CurrentDay s
                )
                |> standardize

            {state with ShuntingEnergySplit = updatedS}
        
        state
        |> updateAverageTotalRewards agents
        |> updateSocialGoodForWork
        |> updateSocialGoodForHunters
        |> updateNoneAgentStates

    let rec loop (currentWorld : WorldState) (agents : Agent list) (writer : StreamWriter) (csvwriter : StreamWriter) : WorldState =

        let livingAgents = agents |> List.filter (fun el -> el.Alive = true)
        let deadAgents = agents |> List.filter (fun el -> el.Alive = false)

        // Duma session
        let currentWorld = fullDuma livingAgents currentWorld

        // Work allocation
        let agentsWithJobs =
            livingAgents
            |> List.map (fun el ->
                let decision = workAllocation el currentWorld // To verify
                match decision with
                | 0 -> {el with TodaysActivity = NONE, 0.0}
                | 1 -> 
                    let huntingStrategy = huntStrategyDecision el currentWorld
                    {el with TodaysActivity = HUNTING, 1.0;
                                TodaysHuntOption = huntingStrategy}
                | 2 -> {el with TodaysActivity = BUILDING, 1.0}
                | _ -> failwith("Invalid decision")
            )
            |> List.map (fun el ->
               {el with Gain = 0.0; FoodShared = false; HuntedFood = 0.0}     // Reset variables that might interfere with printing or decision making
            )
            
        let builders =
            agentsWithJobs
            |> List.filter (fun el -> fst el.TodaysActivity = BUILDING)

        // Update shelter
        let currentWorld = newWorldShelters currentWorld builders

        let slackers =
            agentsWithJobs
            |> List.filter (fun el -> fst el.TodaysActivity = NONE)

        let hunters, currentWorld = 
            agentsWithJobs
            |> List.filter (fun el -> fst el.TodaysActivity = HUNTING)
            |> hunt currentWorld


        // Food energy for allocation
        let energyForAllocation = 
            hunters
            // Discounts agents who do not share food without sanctioning them
            |> List.map (fun el -> el.HuntedFood - el.Gain)
            |> List.sum
            
        // Re-concatenate the individually processed groups
        let agentsAfterWorking = hunters @ builders @ slackers

        let idealEnergyAssignment, idealWorkStatus = idealAllocation currentWorld agentsAfterWorking energyForAllocation

        // Resource Allocation
        let agentsAfterResorceAllocation =
            agentsAfterWorking
            |> assignShelters currentWorld
        // Sanction
        let (agentsAfterSanction, currentWorld) = detectCrime currentWorld idealEnergyAssignment idealWorkStatus agentsAfterResorceAllocation
        let agentsAfterResorceAllocation = 
            agentsAfterSanction
            |> sanction currentWorld
        // Allocate food
            |> allocateFood currentWorld idealEnergyAssignment
        // Energy decay due to working
            |> reduceEnergyForWorking
        // End-of-turn energy decay
            |> List.map (fun el -> newAgentEnergy el)
        // End-of-turn infamy decay
            |> infamyDecay currentWorld
        // Update reward matrices for works
            |> updateWorkRewardMatrices

        // Opinion, Payoff, Social Good updates
        let opinionChangesAgents = agentsAfterResorceAllocation
                                     |> updateRuleOpinion
                                     |> updateRewardsForEveryRuleForAgent currentWorld
        let currentWorld = normaliseTheSocialGood (updateSocialGoodForEveryCurrentRule  opinionChangesAgents currentWorld)

        let normalisedAgentArrays = normaliseTheAgentArrays opinionChangesAgents
                                     |> updateAggregationArrayForAgent currentWorld
                                     |> workOpinions currentWorld
                                     |> selfConfidenceUpdate
        // After sanction, agent may die
        let deadAgentsAfterToday = 
            deadAgents @ (normalisedAgentArrays |> List.filter (fun el -> el.Alive = false || el.Energy <= 0.0))
            |> List.map (fun agent -> {agent with Alive = false})
        let livingAgentsAfterToday = 
            normalisedAgentArrays 
            |> List.filter (fun el -> el.Alive = true && el.Energy > 0.0)

        let currentWorld = updateEndOfDayState agents currentWorld

        printf "times: %A, %A, %A, %A, %A" currentWorld.FoodTime currentWorld.WorkTime currentWorld.PunishmentTime currentWorld.VoteTime currentWorld.ShelterTime
        printf "rules: %A, %A, %A, %A, %A" currentWorld.CurrentFoodRule currentWorld.CurrentWorkRule currentWorld.CurrentMaxPunishment currentWorld.CurrentVotingRule currentWorld.CurrentShelterRule
        
        writer.Write ("Living Agents in day ")
        writer.Write (currentWorld.CurrentDay)
        List.map (fun agent -> writer.Write (printAgent agent)) livingAgentsAfterToday |> ignore
        writer.WriteLine ()
        writer.WriteLine ()
        writer.Write("World Status in day ")
        writer.Write (currentWorld.CurrentDay)
        writer.Write (printWorld currentWorld)
        writer.WriteLine ()
        writer.WriteLine ()
        writer.Write("END OF DAY ")
        writer.Write (currentWorld.CurrentDay)

        if livingAgentsAfterToday.Length = 0 || currentWorld.CurrentDay = maxSimulationTurn then
            csvdump currentWorld (livingAgentsAfterToday @ deadAgentsAfterToday) csvwriter
        else
            //printfn "Living Agents: %A" (List.map printAgent livingAgentsAfterToday)
            //printfn "Dead Agents: %A" (List.map printAgent livingAgentsAfterToday)
            //printfn "Current world status: %A" (printWorld currentWorld)
            printfn "End of DAY: %A" currentWorld.CurrentDay
            writer.WriteLine ()
            writer.WriteLine ()
            loop (csvdump currentWorld (livingAgentsAfterToday @ deadAgentsAfterToday) csvwriter)
                 (livingAgentsAfterToday @ deadAgentsAfterToday)
                  writer 
                  csvwriter

    let runSimulation (outputTXT : string) (outputCSV :string) =
        let writer = new StreamWriter(outputTXT)
        let csvwriter = new System.IO.StreamWriter(outputCSV)
        csvwriter.Write(headings)
        csvwriter.Write(List.fold (fun acc elem -> acc + agentHeadings.Replace("[ID]",string elem.ID)) "" agents)
        let finalWorld = loop currentWorld agents writer csvwriter
        printfn "Final world status: %A" (printWorld finalWorld);
        printfn "Last day %A" finalWorld.CurrentDay
        writer.Write("Final world: ")
        writer.WriteLine(finalWorld)
        writer.Close()
        csvwriter.Close()
    
    let outputName = "output"
    let testName = "test"
    List.map (fun simNumber -> runSimulation (Path.Combine [|".."; ".."; ".."; "..";  "output"; (outputName + (simNumber |> string) + ".txt")|])
                                  (Path.Combine [|".."; ".."; ".."; "..";  "csv"; (testName + (simNumber |> string) + ".csv")|])) [0..(numRuns - 1)] |> ignore

    0
