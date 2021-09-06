import os
import folderconfig as cfg
from src.ast_builder import ASTBuilder
creator = ASTBuilder()
sourcePath= cfg.sourceFolder["path"]
listFiles=os.listdir(sourcePath)
os.chdir(sourcePath);
#file1=listFiles[1]

for fileInput in listFiles:
    if fileInput.endswith(".st") or fileInput.endswith(".ST"):
        print(fileInput)
        print("===============")
        infile=open(fileInput)
        a=infile.read()    
        creator.parse(a)
print("done")
infile.close()