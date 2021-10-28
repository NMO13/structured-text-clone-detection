import os
import folderconfig as cfg
from random import seed
from random import randint
from mutations import mutate
seed(2)
sourcePath= cfg.sourceFolder["path"]

targetPath = sourcePath+cfg.cloneGeneration["subfolder"]
numSources = cfg.cloneGeneration["numSources"]
minClones = cfg.cloneGeneration["numClonesMin"]
maxClones = cfg.cloneGeneration["numClonesMax"]
listFiles=os.listdir(sourcePath)
os.chdir(sourcePath);
#file1=listFiles[1]
endFiles = []
numClones = dict()
cloneFromAFile = []
countFiles = 0
finalFiles = []
for fileInput in listFiles:
    if fileInput.endswith(".st") or fileInput.endswith(".ST"):
        endFiles.append(fileInput)
        numClones[fileInput] = 0
        cloneFromAFile.append(-1)
        countFiles+=1    
        finalFiles.append(fileInput)
        
for f in os.listdir(targetPath):
    os.remove(os.path.join(targetPath, f))
valueTotal = 0
for x in range(numSources):
    value = randint(0, countFiles-1)
    fileInput = endFiles[value]
    fileClone = mutate(fileInput,targetPath,str(numClones[fileInput]))
    numClones[fileInput] += 1
    
    finalFiles.append(fileClone)
    valueTotal = len(finalFiles)-1
    
    cloneFromAFile.append(value)
    cloneFromAFile[value] = valueTotal

fileRegistry = sourcePath+cfg.cloneGeneration["registry"]+"/registry.csv"
with open(fileRegistry, 'w') as writer:
    writer.write("#ID,Filename,#CloneID\n")
    for y in range(valueTotal):
        writer.write(str(y)+", "+finalFiles[y]+", "+str(cloneFromAFile[y])+"\n")
    writer.close()
    
clones    = dict()
nonclones = dict()
for z in range(valueTotal):
    currentFile = finalFiles[z]
    currentClones = ""
    currentNonClones = ""
    #clones[currentFile] = ""
    #nonclones[currentFile] = ""
    w = countFiles
    for w in range(valueTotal):
        if (w!=z):
            if cloneFromAFile[w]==z:
                #clones[currentFile] += str(w)+","
                currentClones += str(w)+","
            else:
                currentNonClones += str(w)+","
                #nonclones[currentFile] += str(w)+","
    fileTrained = sourcePath+cfg.cloneGeneration["registry"]+"/TRAINED_"+currentFile+".txt"
    with open(fileTrained, 'w') as writer:
        writer.write("Trained List for: #"+str(z)+" "+currentFile+"\n")
        #writer.write("Clones: "+clones[currentFile]+"\n")
        writer.write("Clones: "+currentClones+"\n")
        writer.write("Non Clones: "+currentNonClones+"\n")
        #writer.write("Non Clones: "+nonclones[currentFile]+"\n")
        writer.close()