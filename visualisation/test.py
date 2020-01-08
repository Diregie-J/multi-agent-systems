import os

balanced = 1
idealist = 1
egotist = 1
susceptible = 1
idealistN = 1
egotistN = 1
suscpetibleN = 0

runs = 10

days = -1


agent_init = f"from agent import *\n\nTotalProfiles = list(filter(lambda x: x[1] != 0, [(Balanced, {balanced}), (Egotist, {egotist}), (Idealist, {idealist}), (Susceptible, {susceptible}), (NotIdealist, {idealistN}), (NotEgotist, {egotistN}), (NotSusceptible, {suscpetibleN})]))"
total_agents = balanced + idealist + egotist + susceptible + idealistN + egotistN + suscpetibleN
num_profiles = len(list(filter(lambda x: x != 0, [balanced, idealist, egotist, susceptible, idealistN, egotistN, suscpetibleN])))
cmd = f"cd ../multi-agent-systems/Agent-Config ; printf \"{agent_init}\" > total_profiles.py ; python3 agent_init.py ; cd ../bin/Debug/netcoreapp3.0/ ; ./multi-agent-systems  --number-days {days} --number-profiles {num_profiles} --number-agents {total_agents} --number-runs {runs}"

os.system(cmd)