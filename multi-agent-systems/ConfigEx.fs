module ConfigEx

// This is the config, its the place where you canhnge the values for stuff


let mutable maxSimulationTurn = -1 // Set in Parsing as a cmd arg; Negative value corresponds to infinity
let mutable numAgents = [10;20;30;40;50]
let numberOfRules = 5

let costOfHunting = [1.0;2.0;3.0;4.0;5.0;6.0;7.0;8.0;9.0]

let staggiEnergyValue = [50.0;100.0;150.0;200.0;250.0;300.0;350.0;400.0]
let staggiProbability = [0.1;0.2;0.3;0.4;0.5;0.6;0.7;0.8;0.9] // likelihood is 1 in 10 intervals
let staggiMeanRegenRate = [0.1;0.2;0.3;0.4;0.5;0.6;0.7;0.8;0.9]
let staggiMinIndividual = costOfHunting * [0.1;0.2;0.3;0.4;0.5;0.6;0.7;0.8;0.9]
let staggiMinCollective = costOfHunting * [1.0;2.0;3.0;4.0;5.0;6.0;7.0;8.0;9.0]
let rabbosEnergyValue = 50.0
let rabbosProbability = [0.1;0.2;0.3;0.4;0.5;0.6;0.7;0.8;0.9]// likelihood is 3 in 10 intervals
let rabbosMinRequirement = costOfHunting * [0.1;0.2;0.3;0.4;0.5;0.6;0.7;0.8;0.9]
let rabbosMeanRegenRate = [0.1;0.2;0.3;0.4;0.5;0.6;0.7;0.8;0.9]

let eb = [1.0;2.0;3.0;4.0;5.0;6.0;7.0;8.0;9.0] // energy cost per worker to build
let em = 2.5 // energy cost per worker to maintain
let rg = 0.05 // shelter quality decay rate
let es = [10.0;20.0;30.0;40.0;50.0;60.0;70.0;80.0;90.0;100.0] // energy cost per worker to build one shelter
let ep = 0.8 // maximum shelter energy preservation
let rb = 5.0 //base energy decay rate

let maxNumStag = [10;20;30;40;50;60;70;80;90;100]
let maxNumHare = [10;20;30;40;50;60;70;80;90;100]

let vetoThreshold = 2.0
let nominationThreshold = 0.5

// For Sanctions
let InfamyStep = 0.1

// MinimumFoodForOligarchy as a fraction of F/N (maximum assignable value equivalent to communism) 
let MinimumFoodForOligarchy = 1.0
let CrimeDiscoveryRate = 0.5
let WorkExemptionThreshold = 0.3

// Constants for decision making
let Tau = 10.0
let Gamma = 5.0