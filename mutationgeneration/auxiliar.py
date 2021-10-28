def remove_description(text):
        descriptionStartComment = "(*@KEY@:DESCRIPTION*)"
        descriptionEndComment = "(*@KEY@:END_DESCRIPTION*)"

        descriptionStart = text.find(descriptionStartComment)
        descriptionEnd = text.find(descriptionEndComment)
        
        initToDelete = descriptionStart + len(descriptionStartComment)
        endToDelete  = descriptionEnd
        
        subString1 = text[:initToDelete]
        subString2 = text[endToDelete:-1]
        
        text = subString1 + subString2
        return text

    
    
def remove_comments(text):
    import re
    res = re.sub(r"\(\*([\s\S]*?)\*\)", " ", text)
    return res   

def remove_whitelines(fileInput, fileOutput):
    with open(fileInput, 'r') as reader:
        inputLines = reader.readlines()
    reader.close()
    
    with open(fileOutput, 'w') as writer:
        for line in inputLines:
            if line.strip():
                writer.write(line)