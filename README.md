# multi-agent-systems
This is the repo for the Self Organising Multi-Agent Systems Assessed Project

# Pre-requitisits

## dontnet for Ubuntu 18.04
wget -q https://packages.microsoft.com/config/ubuntu/18.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb #.Net Stuff part 1
sudo dpkg -i packages-microsoft-prod.deb #.Net Stuff part 2
sudo apt-get install dotnet-sdk-3.1 -y #.Net Stuff part 3
sudo apt install fsharp -y # F# Stuff

## Stuff needed for visualisations

pip3 install pandas
pip3 install numpy
pip3 install matplotlib

### Needed for GUI to work
pip3 install PyQt5

# Method 1 (non-GUI)

## 0. Build and compile:

Developed with __dotnetcore 3.0__ (might be compatible w other versions)

* To build (from the GitHub cloned directory do) :

      dotnet build .\multi-agent-systems.sln
* To run (from the GitHub cloned directory do) :

      cd  .\multi-agent-systems\bin\Debug\netcoreapp3.0\
      .\multi-agent-systems.exe  --number-days -1 --number-profiles 7 --number-agents 24
      
## 1. Run the program w the default configuration:

   In order to run from the command line Baseline Configuration (12 balanced agents, 2 from each other category) use the following command line arguments:

     --number-days -1 --number-profiles 7 --number-agents 24 [--number-runs 1]

  where:
  * --number-days x -> x is the number of days the simulation runs for, if -1 runs until all agents are dead 
  * --number-profiles x -> x is the number of agent profiles there are (number of profie_ files in the dir multi-agent-systems\Agent-Config\agent_dir)
  * --number-agents x -> x is the number of agents that take part in the simulation initially - this has to be consistent w the number given in the python script
  * --number-runs x -> optional argument - n is number of times the simulation is repeated (produces x csv files in multi-agent-systems/csv)
  
## 2. Run the program w your own configuration:

* Modify in multi-agent-systems\Agent-Config\agent_init.py TotalProfiles:

      TotalProfiles = [(Balanced, 12), (Egotist, 2), (Idealist, 2), (Susceptible, 2),
                       (NotIdealist, 2), (NotEgotist, 2), (NotSusceptible, 2)]                 
   in order to choose how many agents of which types you'd like to have    

* Run multi-agent-systems\Agent-Config\agent_init.py in order to generate the profiles

* Run the f sharp executable with the command line args specified previously (don't forget to change the number-days, number-profiles, number-agents accordingly)

## 3. Modify other program variables:

In Config.fs there are other config variables that can be changed for testing & experimenting in dev stages. They are not meant to be modified during the runtime when a user runs the simulation.

## 4. See the output:

There are 3 ways at the moment:

* With printf see the output in terminal

* The agent and world states are printed every day in output files in multi-agent-systems/output. They are numbered 0..n-1 depending on how many times the simulation is run (--number-runs). Also, n csv files are produced as well in a similar fashion in the multi-agent-systems/csv folder.

* Run `cd visualisation\` in top level directory folder, then `python3 visualistion.py {number of runs}` to create zips of each run in `multi-agent-systems\csv\`. Each zip contains various visualisations for each run to show what occured.

# Method 2 (GUI - only on Linux (and Mac?)) <-- currently on visualisation branch

## 1. Build `dotnet build ./multi-agent-systems.sln`
## 2. Run `python3 run.py` in the top level directory folder
