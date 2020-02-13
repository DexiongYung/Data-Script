import pandas as pd 
import os

df = pd.DataFrame(columns=['count', 'name'])

f = open("fbnames.txt", "r")
count = 0
save_every = 2000

for line in f:
    count += 1
    split = line.split()
    df = df.append({'count':split[0], 'name':split[1].capitalize()}, ignore_index=True)
    
    if count % save_every == 0:
        df.to_csv("fb_lastnames.csv")

df.to_csv("fb_lastnames.csv")
