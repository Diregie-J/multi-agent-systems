import pandas as pd 
import os 

path = os.path.join('c:\\', 'users', 'alex', 'desktop', 'test.csv')
csvfile = pd.read_csv(path)
print(csvfile)