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
    oneOf,
)

semicolon = Literal(";")
ident = Word(alphanums + "_", alphanums + "_" + "#")
expression = Forward()
designator = ident + Optional(
    (Literal(".") + ident) | (Literal("[") + expression + Literal("]"))
)
assign_op = Literal(":=")
mulop = Literal("*") | Literal("/")
addop = Literal("+") | Literal("-")
var_decl = (
    oneOf("VAR_INPUT VAR_OUTPUT VAR_IN_OUT VAR")
    + ZeroOrMore(
        designator + Literal(":") + ident + Optional(assign_op + expression) + semicolon
    )
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
booleanop = Literal("AND") | Literal("OR")
condfact = (
    Optional("NOT")
    + Optional("(")
    + expression
    + Optional(relop + expression)
    + Optional(")")
)
condterm = Optional("(") + condfact + ZeroOrMore("AND" + condfact) + Optional(")")
condition = condterm + ZeroOrMore(Literal("OR") + condterm)

arithmeticop = Literal("+") | Literal("-") | Literal("*") | Literal("/")

param = Forward()
actpars = Literal("(") + Optional(param + ZeroOrMore("," + param)) + Literal(")")
factor = (
    (designator + Optional(actpars))
    | Word(nums)
    | Literal("(") + expression + Literal(")")
)
term = factor + ZeroOrMore(mulop + factor)
param << (
    expression
    + Optional(
        Optional(assign_op + expression)
        + ZeroOrMore((relop | arithmeticop | booleanop + Optional("NOT")) + expression)
    )
)
expression << (Optional("-") + term + ZeroOrMore(addop + Optional("-") + term))
statement = Forward()
block = ZeroOrMore(statement)
count_condition = (
    Literal("(")
    + designator
    + assign_op
    + Word(nums)
    + Keyword("TO")
    + Word(nums)
    + Literal(")")
)
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
        + count_condition
        + Keyword("DO")
        + block
        + Keyword("END_FOR")
        + semicolon
    )
    | (
        Keyword("WHILE")
        + condition
        + Keyword("DO")
        + block
        + Keyword("END_WHILE")
        + semicolon
    )
    | (
        Keyword("IF")
        + condition
        + Keyword("THEN")
        + block
        + ZeroOrMore(
            Keyword("ELSIF")
            + Optional(Literal("("))
            + condition
            + Optional(Literal(")"))
            + Keyword("THEN")
            + block
        )
        + Optional(Keyword("ELSE") + block)
        + Keyword("END_IF")
        + semicolon
    )
    | (
        Keyword("CASE")
        + designator
        + Optional(actpars)
        + Keyword("OF")
        + OneOrMore(caseblock)
        + Optional(Keyword("ELSE") + block)
        + Keyword("END_CASE")
        + semicolon
    )
    | (Keyword("RETURN") + semicolon)
)


parser = (
    Keyword("PROGRAM") |  Keyword("FUNCTION_BLOCK") | Keyword("FUNCTION")
    + ident + Optional(":" + ident)
    + ZeroOrMore(var_decl)
    + ZeroOrMore(statement)
    + oneOf("END_PROGRAM END_FUNCTION_BLOCK END_FUNCTION")
)
