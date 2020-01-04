module Config

// This is the config, its the place where you canhnge the values for stuff


let mutable maxSimulationTurn = -1 // Set in Parsing as a cmd arg; Negative value corresponds to infinity
let mutable numAgents = 0
// How many times the simulation should be run
let mutable numRuns = 1
let numberOfRules = 5

let costOfHunting = 30.0

let staggiEnergyValue = 200.0
let staggiProbability = 0.1 // likelihood is 1 in 10 intervals
let staggiMeanRegenRate = 0.1
let staggiMinIndividual = costOfHunting * 0.4
let staggiMinCollective = costOfHunting * 2.0
let rabbosEnergyValue = 50.0
let rabbosProbability = 0.3 // likelihood is 3 in 10 intervals
let rabbosMinRequirement = costOfHunting * 0.4
let rabbosMeanRegenRate = 0.1

let eb = 10.0 // energy cost per worker to build
let em = 2.5 // energy cost per worker to maintain
let rg = 0.05 // shelter quality decay rate
let es = 35.0 // energy cost per worker to build one shelter
let ep = 0.8 // maximum shelter energy preservation
let rb = 5.0 //base energy decay rate

let maxNumStag = 30
let maxNumHare = 30

let vetoThreshold = 2.0
let nominationThreshold = 0.5

// For Sanctions
let InfamyStep = 0.1

// Time between rule changes
let ruleTime = 6

// MinimumFoodForOligarchy as a fraction of F/N (maximum assignable value equivalent to communism) 
let MinimumFoodForOligarchy = 1.0
let CrimeDiscoveryRate = 0.5
let WorkExemptionThreshold = 0.3

// Constants for decision making
let Tau = 10.0
let Gamma = 5.0

let AgentMaxEnergy = 100.0
