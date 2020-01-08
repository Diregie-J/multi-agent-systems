from agent import *

TotalProfiles = list(filter(lambda x: x[1] != 0, [(Balanced, 1), (Egotist, 1), (Idealist, 1), (Susceptible, 1), (NotIdealist, 1), (NotEgotist, 1), (NotSusceptible, 0)]))