import os
import magic
import codecs
import folderconfig as cfg
from auxiliar import *
sourcePath= cfg.preprocessFolder["sourcePath"]

targetPath = cfg.preprocessFolder["targetPath"]
listFiles=os.listdir(sourcePath)
os.chdir(sourcePath);
#file1=listFiles[1]
endFiles = []
clonedFiles = dict()
countFiles = 0
for f in os.listdir(targetPath):
    os.remove(os.path.join(targetPath, f))

for fileInput in listFiles:
    if fileInput.endswith(".st") or fileInput.endswith(".ST"):
        #print(fileInput)
        fileOutput = os.path.join(targetPath,"",fileInput)
        infile=open(fileInput)
        text=infile.read()    
        
        
        m = magic.Magic(mime_encoding=True)
        encoding = m.from_buffer(text)
        
        
        infile.close()
        text = remove_description(text)
        text = remove_comments(text)
        
        with codecs.open(fileOutput,'w','utf-8') as write_file:
            print(fileOutput)
            write_file.write(text)
            write_file.close()
        remove_whitelines(fileOutput,fileOutput)
        with codecs.open(fileOutput,'r','utf-8') as read_file:
            text=read_file.read()    
            
            
            read_file.close()
            countLines = text.count("\n")
            if countLines<15:
                 os.remove(fileOutput)
        
    if fileInput.endswith(".SCasdadsad"):
        fileOutput = os.path.join(targetPath,"",fileInput)
        infile=open(fileInput)
        text=infile.read()    
        infile.close()
        text = remove_comments(text)
        countLines = text.count("\n")
        with open(fileOutput,'w') as write_file:
            write_file.write(text)
        write_file.close()
        remove_whitelines(fileOutput,fileOutput)
        
  
        
#         with open(fileInput,'r') as read_file:
#         lines = read_file.readlines()
#         valid = False
#         for line in lines:
#             if valid:
#                 stripline = line.strip()
#                 defposition = stripline.strip().find(":")
#                 if defposition:
#                     identif =   stripline[0:defposition]
#                     identif = identif.strip()
#                     valid = False;
#                 if line.find("END_VAR")!=-1:
#                     valid = False            
#             if line.startswith("VAR"):
#                 valid = True;