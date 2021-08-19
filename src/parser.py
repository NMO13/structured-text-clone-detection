from pyparsing import (
    Word,
    Literal,
    Keyword,
    alphanums,
    ZeroOrMore,
    OneOrMore,
    Optional,
    nums,
    Forward,
    oneOf
)

semicolon = Literal(";")
ident = Word(alphanums+"_", alphanums+'_'+"#")
expression = Forward()
designator = ident + Optional((Literal(".") + ident) | (Literal("[") + expression + Literal("]")))
assign_op = Literal(":=")
mulop = Literal("*") | Literal("/")
addop = Literal("+") | Literal("-")
var_decl = (
    oneOf("VAR_INPUT VAR_OUTPUT VAR_IN_OUT VAR")
    + ZeroOrMore(designator + Literal(":") + oneOf("INT BOOL BYTE TIME _RMP_NEXT T_PLC_MS") + Optional(assign_op + expression) + semicolon)
    + Keyword("END_VAR")
)
relop = (
    Literal(">=")
    | Literal(">")
    | Literal("<>")
    | Literal("<=")
    | Literal("<")
    | Literal("=")
)
condfact = Optional("NOT") + Optional("(") + expression + Optional(")") + Optional(relop + expression)
condterm = condfact + ZeroOrMore("AND" + condfact)
condition = condterm + ZeroOrMore(Literal("OR") + condterm)

arithmeticop = Literal("+") | Literal("-") | Literal("*") | Literal("/")

param = Forward()
actpars = Literal("(") + Optional(param + ZeroOrMore(",", param)) + Literal(")")
factor = (designator + Optional(actpars)) | Word(nums) | Literal("(") + expression + Literal(")")
term = factor + ZeroOrMore(mulop + factor)
param << (designator + Optional(Optional(assign_op + expression) + (relop | arithmeticop) + expression))
expression << (Optional("-") + term + ZeroOrMore(addop + term))
statement = Forward()
block = ZeroOrMore(statement)
count_condition = designator + assign_op + Word(nums) + Keyword("TO") + Word(nums)
caseblock = ident + Literal(":") + block
statement << (
    (
        Keyword("REPEAT")
        + block
        + Keyword("UNTIL")
        + condition
        + semicolon
        + Keyword("END_REPEAT")
        + semicolon
    )
    | (designator + ((assign_op + expression) | actpars) + semicolon)
    | (
        Keyword("FOR")
        + Literal("(")
        + count_condition
        + Literal(")")
        + Keyword("DO")
        + block
        + Keyword("END_FOR")
        + semicolon
    )
    | (
        Keyword("WHILE")
        + Literal("(")
        + condition
        + Literal(")")
        + Keyword("DO")
        + block
        + Keyword("END_WHILE")
        + semicolon
    )
    | (
        Keyword("IF")
        + Optional(Literal("("))
        + condition
        + Optional(Literal(")"))
        + Keyword("THEN")
        + block
        + ZeroOrMore(Keyword("ELSIF") + Optional(Literal("(")) + condition + Optional(Literal(")")) + Keyword("THEN") + block)
        + Optional(Keyword("ELSE") + block)
        + Keyword("END_IF")
        + semicolon
    )
    | (
        Keyword("CASE")
        + designator + Optional(actpars)
        + Keyword("OF")
        + OneOrMore(caseblock)
        + Optional(Keyword("ELSE") + block)
        + Keyword("END_CASE")
        + semicolon
    )
)


parser = (
    oneOf("PROGRAM FUNCTION_BLOCK")
    + ident
    + ZeroOrMore(var_decl)
    + ZeroOrMore(statement)
    + oneOf("END_PROGRAM END_FUNCTION_BLOCK")
)
