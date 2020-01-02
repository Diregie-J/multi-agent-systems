import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

path = os.path.join('c:\\', 'users', 'alex', 'desktop', 'test.csv')
csvfile = pd.read_csv(path)
print(csvfile)

filtered_col = []

energy = csvfile.filter(regex="Energy$", axis=1)
for x in range(len(energy.T.columns)):
    col = energy.T[x]
    filtered_col.append(col.dropna())

print(filtered_col)

fig, axes = plt.subplots(nrows=1, ncols=1)

axes.boxplot(filtered_col, vert=True, patch_artist=True)

axes.set_title('Rectangular box plot')

# adding horizontal grid lines
axes.yaxis.grid(True)
axes.set_xlabel('Three separate samples')
axes.set_ylabel('Observed values')
axes.set_ylim(0, 100)

plt.show()