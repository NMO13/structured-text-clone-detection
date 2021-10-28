import string
import shutil
from random import seed
from random import randint

def changeIdentificator(fileInput, fileOutput):
    identif = "empty"
    with open(fileInput,'r') as read_file:
        lines = read_file.readlines()
        valid = False
        for line in lines:
            if valid:
                stripline = line.strip()
                defposition = stripline.strip().find(":")
                if defposition:
                    identif =   stripline[0:defposition]
                    identif = identif.strip()
                    valid = False;
                if line.find("END_VAR")!=-1:
                    valid = False            
            if line.startswith("VAR"):
                valid = True;
    if identif!="empty":
            with open(fileInput, 'r') as reader:
                text = reader.read()    
                alphabet_string = string. ascii_lowercase
                newIdentificator = alphabet_string[randint(0, len(alphabet_string))-1]
                text = text.replace(identif, newIdentificator)
                reader.close()
            with open(fileOutput, 'w') as writer:
                writer.write(text)
                writer.close()
                
def generateLine():
    alphabet_string = string. ascii_lowercase
    identificator = alphabet_string[randint(0, len(alphabet_string))-1]
    lineToAdd = identificator + " := 1;\n"
    return lineToAdd
    
def processAddDelete(fileInput, fileOutput, addLine):
    with open(fileInput,'r') as read_file:
        lines = read_file.readlines()
        numLines = len(lines)

        foundVar = False
        valid = False
        currentLine = 0 
        check = False
        
        with open(fileOutput,'w') as write_file:
            for line in lines:
                currentLine+=1
                if line.startswith("VAR") and len(line)<5:
                    foundVar = True
                    valid = False
                if (line.find("END_VAR")!=-1) and foundVar:
                    if currentLine <= numLines:
                        valid = True
                        if addLine:
                            lineInterest = randint(currentLine, numLines-1)    
                        else:
                            if currentLine < numLines-1:
                                lineInterest = randint(currentLine+1, numLines-1)    
                            else:
                                lineInterest = 0
                delete = True
                if line.startswith("IF") or line.startswith("ELSE") or line.startswith("CASE") or line.startswith("END") or line.startswith("FOR"):
                    delete = False
                if valid and currentLine == lineInterest and (addLine or delete):
                    #print(currentLine)
                    valid = False
                    if addLine:
                        lineToAdd = generateLine()
                        write_file.write(line)    
                        write_file.write(lineToAdd)       
                else:
                     write_file.write(line)
        

def mutate(fileInput,targetPath,idclone): 
    suffix = ""
    for i in range(3):
        #Identificator
        valueIdent = randint(0, 1)    
        valueDelete = randint(0, 5) 
        valueAdd = randint(0, 5) 
        suffix += "chg"+str(valueIdent)
        suffix += "del"+str(valueDelete)
        suffix += "add"+str(valueAdd)
        
        newName = fileInput.replace(".st", "_"+suffix+"_"+idclone+".st")
        newName = newName.replace(".ST", "_"+suffix+"_"+idclone+".ST")
        fileOutput = targetPath+"/"+newName 

        
        shutil.copyfile(fileInput, fileOutput)
        
        #processuntilbody(fileInput,fileOutput)
        if valueIdent:
            changeIdentificator(fileOutput, fileOutput)
        for y in range(valueAdd):
            processAddDelete(fileOutput, fileOutput, True)
        
        for x in range(valueDelete):
            processAddDelete(fileOutput, fileOutput, False)
        
        return newName