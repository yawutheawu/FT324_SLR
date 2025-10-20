import pandas as pd
import os

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

os.chdir("Searches")
corpusSources = list(os.listdir())
corpus = []
totalSources = 0
if ".DS_Store" in corpusSources:
    corpusSources.remove(".DS_Store")
for i in corpusSources:
    with open(i,"r") as f:
        fileText = f.read()
        microCorpus = fileText.split("\n")
        for j in range(len(microCorpus)):
            microCorpus[j] = microCorpus[j].strip()
        corpus.extend(microCorpus)
        print(f"{f.name} has {len(microCorpus)} sources")
        totalSources += len(microCorpus)

corpus = list(set(corpus))

print(f"Total number of articles in Pruned Research Corpus: {len(corpus)}")
print(f"Total number of articles pre-pruning: {totalSources}\nSources pruned: {totalSources-len(corpus)}")
print(f"{round(((totalSources-len(corpus))/totalSources) * 100,2)}% Duplicates")

os.chdir("..")
corpus = pd.DataFrame({"Source Link":corpus})
corpus.to_csv("PrunedResearchPapers.csv")