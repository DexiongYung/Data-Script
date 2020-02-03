import pandas as pd 
import os

files = os.listdir("namesbystate/")

df = pd.DataFrame(columns=['count', 'name'])

count = 0
save_every = 2000

for file in files:
    f = open(f"namesbystate\{file}", "r")
    count = 0
    for line in f:
        count += 1
        split = line.split(",")
        df = df.append({"count":int(split[4]),"name":split[3]}, ignore_index=True)
        if save_every % count == 0:
            df = df.groupby(['name']).sum()
            df.to_csv("namesbystates.csv")

df.groupby(['name']).sum()
df.to_csv("namesbystates.csv")
