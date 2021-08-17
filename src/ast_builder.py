class ASTBuilder():
    def __init__(self):
        from src import parser
        self.parser = parser

    def parse(self, text):
        text = self.remove_comments(text)
        self.parser.parseString(text)

    def remove_comments(self, text):
        import re
        res = re.sub(r"(\(\*[^\(]*)\*\)", " ", text)
        return res
