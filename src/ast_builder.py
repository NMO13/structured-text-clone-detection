class ASTBuilder:
    def __init__(self):
        from src.parser import parser

        self.parser = parser

    def parse(self, text):
        text = self.remove_description(text)
        text = self.remove_comments(text)
        result = self.parser.parseString(text)
        print(result)
        return result

    def remove_description(self, text):
        descriptionStartComment = "(*@KEY@:DESCRIPTION*)"
        descriptionEndComment = "(*@KEY@:END_DESCRIPTION*)"

        descriptionStart = text.find(descriptionStartComment)
        descriptionEnd = text.find(descriptionEndComment)
        if descriptionStart == -1 or descriptionEnd == -1:
            return text

        initToDelete = descriptionStart + len(descriptionStartComment)
        endToDelete = descriptionEnd

        subString1 = text[:initToDelete]
        subString2 = text[endToDelete:-1]

        text = subString1 + subString2
        return text

    def remove_comments(self, text):
        import re

        res = re.sub(r"\(\*([\s\S]*?)\*\)", " ", text)

        return res

    def post_process(self, parsed_text):
        """
        Redeclare method types
        :return:
        """
