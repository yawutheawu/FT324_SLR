import os
import numpy as np
import math
import pandas as pd

def resetDir():
    fileName = __file__
    if type(fileName.split("\\")) == list and len(fileName.split("\\"))>1:
        fileName = fileName.split("\\")[-1]
        filePath = __file__.replace(fileName,"")
    else:
        fileName = fileName.split("/")[-1]
        filePath = __file__.replace(fileName,"")
    os.chdir(filePath)
    return os.path.abspath(filePath)

resetDir()

os.chdir("Research Corpus")
os.chdir("Data by Source")
files = list(os.listdir())
if ".DS_Store" in files:
    files.remove(".DS_Store")

files.sort(key= lambda x:int(x.split("_")[1].split("~")[0]))

sources = sorted([x.split("~")[0] for x in files],key= lambda x:int(x.split("_")[1]))
ConsensusMechs = ['Proof of Work', 'Proof of Stake', 'Delegated Proof of Stake', 'Proof of History', 'Proof of Stake with Byzantine Fault Tolerance', 'Proof of History with Proof of Stake', 'zk-proof', 'Sharding', 'DAGs']

intermediateData = {x : {'TPS' :[],  'Energy Use per Transaction':[],  'Nakamoto Coefficient':[],  '% of nodes required to take over network':[],  'Strengths':[], 'Weaknesses':[]} for x in ConsensusMechs}

for i in files:
    temp = pd.read_excel(i,na_values="N/A")
    for j in intermediateData.keys():
        for z in intermediateData[j]:
            workingItem = temp.loc[temp["Consensus"] == j][z].item()
            if not pd.isna(workingItem):
                intermediateData[j][z].append(workingItem)

averagedData = {"Consensus Mechanism" : [], 'TPS' :[],  'Energy Use per Transaction':[],  'Nakamoto Coefficient':[],  '% of nodes required to take over network':[],  'Strengths':[], 'Weaknesses':[]}

for i in intermediateData.keys():
    averagedData["Consensus Mechanism"].append(i)
    for j in intermediateData[i]:
        if len(intermediateData[i][j])>0:
            if type(intermediateData[i][j][0]) == float or type(intermediateData[i][j][0]) == int:
                averagedData[j].append(np.mean(intermediateData[i][j]))
            else:
                temporaryList = []
                for k in intermediateData[i][j]:
                    temporaryList.append(k)
                averagedData[j].append(temporaryList)
        else:
            averagedData[j].append(pd.NA)

averagedData = pd.DataFrame(averagedData)
resetDir()
averagedData.to_excel("Averaged Data.xlsx")
print(averagedData.head(10))
print("Average Data saved")