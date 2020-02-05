import pandas as pd 
import os

df = pd.DataFrame(columns=['count', 'name'])

f = open("facebook-names-original.txt", "r")
count = 0
save_every = 2000

for line in f:
    count += 1
    split = line.split()
    df = df.append({'count':1, 'name':split[1].capitalize()}, ignore_index=True)
    
    if save_every % count == 0:
        df = df.groupby(['name']).sum()
        df.to_csv("FBFullnames.csv")

df = df.groupby(['name']).sum()
df.to_csv("FBFullnamess.csv")
