import openpyxl as xsl
import os
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
analyzedLinksFilename = "ResearchEvaluation.xlsx"
os.chdir("..")
analyzedLinks = xsl.load_workbook(analyzedLinksFilename, read_only=True, data_only=True)

processedSheet = analyzedLinks["Abstract Analysis"]

PaperTitles = []
print("Getting Processed Titles")
rowNum = 2
while str(processedSheet[f"A{rowNum}"].value).strip() != "" and processedSheet[f"A{rowNum}"].value != None:
    if str(processedSheet[f"B{rowNum}"].value).strip() == "Y":
        PaperTitles.append(str(processedSheet[f"A{rowNum}"].value).strip())
    elif str(processedSheet[f"A{rowNum}"].value).strip() == "" or processedSheet[f"A{rowNum}"].value == None:
        print(f"{str(processedSheet[f"A{rowNum}"].value).strip()} has not been processed in the excel file!")
    rowNum+=1
print("Got Processed Titles")
print("Getting Processed Links")
linksheet = analyzedLinks["Datasource"]

links = []
usedRowNums = []

for k,i in enumerate(PaperTitles):
    print(f"Fetching {k} of {len(PaperTitles)}")
    flag = True
    rowNum = 2
    spaceCounter = 0
    while flag:
        if rowNum in usedRowNums:
            pass
        else:
            if str(linksheet[f"C{rowNum}"].value).strip() == i.strip():
                links.append(str(linksheet[f"B{rowNum}"].value).strip())
                usedRowNums.append(rowNum)
                flag = False
            elif str(linksheet[f"C{rowNum}"].value).strip() == "" or linksheet[f"C{rowNum}"].value == None:
                links.append(None)
                flag = False
            else:
                pass
        rowNum += 1

titleAndLinkFinal = pd.DataFrame({"Title":PaperTitles,"Link":links})
print("Got Processed Links")
print(f"Final research corpus len: {len(titleAndLinkFinal)}")
titleAndLinkFinal.to_csv("finalResearchCorpus.csv")