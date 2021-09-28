def create_occurrence_list(tokens):
    token_occurence_dict = {"KEYWORD": 0, "OPERATOR": 0, "MARKER": 0, "LITERAL": 0, "METHOD_IDENTIFIER": 0, "DATATYPE": 0, "QUALIFIED_NAME": 0, "VARIABLE_IDENTIFIER": 0}
    for t in tokens:
        token_occurence_dict[t[0]] += 1


def similarity_score(tokensA, tokensB):
    def classify(tuple):
        print(tuple)
    [classify(t) for t in tokensA]
    print(tokensA)