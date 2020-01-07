import os

balanced = 10
idealist = 10
egotist = 10
susceptible = 10
idealistN = 10
egotistN = 10
suscpetibleN = 10

runs = 1

days = -1


agent_init = f"from agent import *\n\nTotalProfiles = [(Balanced, {balanced}), (Egotist, {egotist}), (Idealist, {idealist}), (Susceptible, {susceptible}), (NotIdealist, {idealistN}), (NotEgotist, {egotistN}), (NotSusceptible, {suscpetibleN})]"
total_agents = balanced + idealist + egotist + susceptible + idealistN + egotistN + suscpetibleN
cmd = f"cd ../multi-agent-systems/Agent-Config ; printf \"{agent_init}\" > total_profiles.py ; python3 agent_init.py ; cd ../bin/Debug/netcoreapp3.0/ ; ./multi-agent-systems  --number-days {days} --number-profiles 7 --number-agents {total_agents} --number-runs {runs}"

os.system(cmd)