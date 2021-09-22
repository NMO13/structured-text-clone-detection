class ASTBuilder:

    def __init__(self):
        from src.parser import parser

        self.parser = parser

    def parse(self, text):
        text = self.remove_comments(text)
        result = self.parser.parseString(text)
        self.post_process(result)

    def remove_comments(self, text):
        import re

        res = re.sub(r"\(\*([\s\S]*?)\*\)", " ", text)

        return res

    def post_process(self, parsed_text):
        """
        Redeclare method types
        :return:
        """
