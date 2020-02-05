import pandas as pd 
import os

NAME = "FBFullNames.csv"

df = pd.DataFrame(columns=['count', 'name'])

f = open("facebook-names-original.txt", "r")
count = 0
save_every = 2000

for line in f:
    count += 1
    df = df.append({'count':1, 'name':line}, ignore_index=True)
    
    if save_every % count == 0:
        df = df.groupby(['name']).sum()
        df.to_csv(NAME)

df = df.groupby(['name']).sum()
df.to_csv(NAME)
