import os
import glob
import folderconfig as cfg
from random import seed
from random import randint
from mutations import mutate
from pathlib import Path
import shutil

OSCATPath = cfg.OSCATsrc["sourcePath"]
TargetPath = cfg.OSCATsrc["targetPath"]
    
matches = []

print(OSCATPath)
# root_dir needs a trailing slash (i.e. /root/dir/)
#for filename in glob.iglob(OSCATPath + '**/**', recursive=True):
#     print(filename)
        
for path in Path(OSCATPath).rglob('*.ST'):
    #matches.Append(path.name)
    #print(path.name)
    #print(path.parent)
    InitPath = os.path.join(path.parent,"",path.name)
    EndPath = os.path.join(TargetPath,"",path.name)
    shutil.copyfile(InitPath, EndPath)
    
    
for path in Path(OSCATPath).rglob('*.st'):
    InitPath = os.path.join(path.parent,"",path.name)
    EndPath = os.path.join(TargetPath,"",path.name)
    shutil.copyfile(InitPath, EndPath)
    
    
for path in Path(OSCATPath).rglob('*.SCL'):
    InitPath = os.path.join(path.parent,"",path.name)
    EndPath = os.path.join(TargetPath,"",path.name)
    shutil.copyfile(InitPath, EndPath)