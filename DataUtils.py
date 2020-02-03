import pandas as pd 
import glob
import string 
import os

ALLOWED_CHARS = string.ascii_letters + "-,. \"()'"

def concat_all_data(path : str = 'Data/*.csv', save_path : str = 'Data/final.csv'):
    csvs = glob.glob(path)

    li = []

    for csv in csvs:
        df = pd.read_csv(csv)
        li.append(df)

    final_df = pd.concat(li)

    final_df.to_csv(save_path)

def clean_csv(path : str, save_pth : str):
    df = pd.read_csv(path)
    df = remove_dups_df(df)
    df = remove_invalid_rows_df(df)

    df.to_csv(save_pth)

def remove_dups_df(df : pd.DataFrame):
    df.sort_values("name", inplace = True)
    df.drop_duplicates(subset="name", keep=False, inplace=True)

    return df

def remove_invalid_rows_df(df : pd.DataFrame):
    return df[df['name'].apply(lambda x: set(x).issubset(ALLOWED_CHARS))]

df = pd.DataFrame(columns=['count', 'name'])

f = open("fbnames.txt", "r")
count = 0
save_every = 2000

for line in f:
    count += 1
    split = line.split()
    df = df.append({'count':split[0], 'name':split[1].capitalize()}, ignore_index=True)
    
    if count % save_every == 0:
        df.to_csv("fbnames.csv")

df.to_csv("fbnames.csv")


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