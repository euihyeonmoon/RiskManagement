import pandas as pd
from pandas import json_normalize
import json
import os
from pathlib import Path

path = "./json_files"
file_list = os.listdir(path)
print ("file_list: {}".format(file_list))

path_fixed = "./json_files/csv_files"

for file in file_list:
    if file.endswith(".json"):
        print ("file: {}".format(file))
        file_name = file.split(".")[0]
        print ("file_name: {}".format(file_name))
        with open(path + "/" + file) as json_file:
            json_data = json.load(json_file)
            df = json_normalize(json_data["articles"])
            print ("df: {}".format(df))
            df.to_csv(path_fixed + "/" + file_name + ".csv")

DATASET = sorted([x for x in Path(path_fixed).glob("*.csv")])

def dataframe_from_csv(target):
    return pd.read_csv(target).rename(columns=lambda x: x.strip())

def dataframe_from_csvs(targets):
    return pd.concat([dataframe_from_csv(x) for x in targets])

DATA = dataframe_from_csvs(DATASET)
print(DATA)

DATA.to_csv("DATA.csv")