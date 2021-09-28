class ASTBuilder:
    def __init__(self):
        from src.parser import parser

        self.parser = parser

    def parse(self, text):
        text = self.remove_description(text)
        text = self.remove_comments(text)
        result = self.parser.parseString(text)
        self.resolve_method_marker(result)
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

    def resolve_method_marker(self, parsed_text):
        """
        Redeclare method types
        :return:
        """
        def merge_qualifier(prev_ident, next_ident):
            prev_ident()

        for i, token in enumerate(parsed_text):
            if token[0] == "MARKER" and token[1] == ".":
                merge_qualifier(parsed_text[i-1], parsed_text[i+1])

