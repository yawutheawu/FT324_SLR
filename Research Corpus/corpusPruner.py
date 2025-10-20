import pandas as pd
import os
import traceback

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

headless = True

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

os.chdir("..")
print("Getting Titles...")
Titles = []
options = Options()
if headless:
    options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)
for i in corpus:
    driver.get(i)
    microTitle = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"/html/body/primo-explore/div/prm-full-view-page/prm-full-view-cont/md-content/div[2]/prm-full-view/div/div/div/div[1]/div/div[2]/prm-full-view-service-container/div[2]/prm-brief-result-container/div[1]/div[3]/prm-brief-result/h3/a/span/prm-highlight/span"))).text
    Titles.append(microTitle)
driver.close()

corpus = pd.DataFrame({"Source Link":corpus,"Title":Titles})
corpus.sort_values(by="Title")
corpus.drop_duplicates(subset=['Title'],inplace=True)
print(f"Total number of articles in Pruned Research Corpus: {len(corpus)}")
print(f"Total number of articles pre-pruning: {totalSources}\nSources pruned: {totalSources-len(corpus)}")
print(f"{round(((totalSources-len(corpus))/totalSources) * 100,2)}% Duplicates")
corpus.reset_index(inplace=True,drop=True)
corpus.to_csv("PrunedResearchPapers.csv")