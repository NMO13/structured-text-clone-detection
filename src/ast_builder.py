class ASTBuilder:
    def __init__(self):
        from src.parser import parser

        self.parser = parser

    def parse(self, text):
        text = self.remove_description(text)
        text = self.remove_comments(text)
        result = self.parser.parseString(text)
        result = self.resolve_method_marker(result)
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

        def get_qualified_name(token, new_tokens):
            import re
            subtokens = re.findall('\(.*?\)', token[1])
            token_list = []
            for token in subtokens:
                token = eval(token)
                if token[0] == "IDENTIFIER":
                    token_list.append(token)
            x = ""
            for token in token_list[:-1]:
                x += token[1]
                x += "."

            if x:
                qualifier = ("QUALIFIED_NAME", x[:-1])
                new_tokens.append(qualifier)
            return token_list[-1]

        new_tokens = []
        for i, token in enumerate(parsed_text):
            if token[0] == "DESIGNATOR":
                ident = get_qualified_name(token, new_tokens)
                if parsed_text[i+1][0] == "METHOD_MARKER":
                    new_tokens.append(("METHOD_IDENTIFIER", ident[1]))
                else:
                    new_tokens.append(("VARIABLE_IDENTIFIER", ident[1]))
            else:
                new_tokens.append(token)
        return new_tokens
