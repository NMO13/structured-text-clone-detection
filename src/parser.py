from functools import partial
from pyparsing import (
    Word,
    Literal,
    Keyword,
    alphas,
    ZeroOrMore,
    OneOrMore,
    Optional,
    nums,
    Forward,
    oneOf,
    Suppress
)


def aw(tokentype):
    return partial(annotate, tokentype)

def annotate(tokentype, t):
    return (tokentype, t[0]) if t else []


semicolon = Literal(";").setParseAction(aw("MARKER"))
ident = Word(alphas + "_", alphas + "_" + "#").setParseAction(aw("TYPE_IDENTIFIER"))
dtype = Word(alphas + "_", alphas + "_" + "#").setParseAction(aw("DATATYPE"))
expression = Forward()
designator = ident + Optional(
    (Literal(".").setParseAction(aw("MARKER")) + ident) | (Literal("[").setParseAction(aw("MARKER")) + expression + Literal("]").setParseAction(aw("MARKER")))
)
assign_op = Literal(":=").setParseAction(aw("OPERATOR"))
mulop = (Literal("*") | Literal("/")).setParseAction(aw("OPERATOR"))
addop = (Literal("+") | Literal("-")).setParseAction(aw("OPERATOR"))
var_decl = (
    oneOf("VAR_INPUT VAR_OUTPUT VAR_IN_OUT VAR").setParseAction(aw("KEYWORD"))
    + ZeroOrMore(
        designator + Suppress(Literal(":")) + dtype + Optional(assign_op + expression) + semicolon
    )
    + Keyword("END_VAR").setParseAction(aw("KEYWORD"))
)
relop = (
    Literal(">=")
    | Literal(">")
    | Literal("<>")
    | Literal("<=")
    | Literal("<")
    | Literal("=")
).setParseAction(aw("OPERATOR"))
booleanop = (Literal("AND") | Literal("OR")).setParseAction(aw("KEYWORD"))
condfact = (
    Optional("NOT").setParseAction(aw("KEYWORD"))
    + Optional("(").setParseAction(aw("MARKER"))
    + expression
    + Optional(relop + expression)
    + Optional(")").setParseAction(aw("MARKER"))
)
condterm = Optional("(").setParseAction(aw("MARKER")) + condfact + ZeroOrMore(Keyword("AND").setParseAction(aw("KEYWORD")) + condfact) + Optional(")").setParseAction(aw("MARKER"))
condition = condterm + ZeroOrMore(Literal("OR").setParseAction(aw("KEYWORD")) + condterm)

arithmeticop = (Literal("+") | Literal("-") | Literal("*") | Literal("/")).setParseAction(aw("OPERATOR"))

param = Forward()
actpars = Literal("(").setParseAction(aw("MARKER")) + Optional(param + ZeroOrMore(Literal(",").setParseAction(aw("MARKER")) + param)) + Literal(")").setParseAction(aw("MARKER"))
factor = (
    (designator + Optional(actpars).setParseAction(aw("METHOD_IDENTIFIER")))
    | Word(nums).setParseAction(aw("LITERAL"))
    | Literal("(").setParseAction(aw("MARKER")) + expression + Literal(")").setParseAction(aw("MARKER"))
)
term = factor + ZeroOrMore(mulop + factor)
param << (
    expression
    + Optional(
        Optional(assign_op + expression)
        + ZeroOrMore((relop | arithmeticop | booleanop + Optional("NOT").setParseAction(aw("KEYWORD"))) + expression)
    )
)
expression << (Optional("-").setParseAction(aw("OPERATOR")) + term + ZeroOrMore(addop + Optional("-").setParseAction(aw("OPERATOR")) + term))
statement = Forward()
block = ZeroOrMore(statement)
count_condition = (
    Literal("(").setParseAction(aw("MARKER"))
    + designator
    + assign_op
    + expression
    + Keyword("TO").setParseAction(aw("KEYWORD"))
    + expression
    + Literal(")").setParseAction(aw("MARKER"))
)
caseblock = Word(nums).setParseAction(aw("MARKER")) + Suppress(Literal(":")) + block
statement << (
    (
        Keyword("REPEAT").setParseAction(aw("KEYWORD"))
        + block
        + Keyword("UNTIL").setParseAction(aw("KEYWORD"))
        + condition
        + semicolon
        + Keyword("END_REPEAT").setParseAction(aw("KEYWORD"))
        + semicolon
    )
    | (designator + ((assign_op + expression) | actpars.setParseAction(aw("METHOD_IDENTIFIER"))) + semicolon)
    | (
        Keyword("FOR").setParseAction(aw("KEYWORD"))
        + count_condition
        + Keyword("DO").setParseAction(aw("KEYWORD"))
        + block
        + Keyword("END_FOR").setParseAction(aw("KEYWORD"))
        + semicolon
    )
    | (
        Keyword("WHILE").setParseAction(aw("KEYWORD"))
        + condition
        + Keyword("DO").setParseAction(aw("KEYWORD"))
        + block
        + Keyword("END_WHILE").setParseAction(aw("KEYWORD"))
        + semicolon
    )
    | (
        Keyword("IF").setParseAction(aw("KEYWORD"))
        + condition
        + Keyword("THEN").setParseAction(aw("KEYWORD"))
        + block
        + ZeroOrMore(
            Keyword("ELSIF").setParseAction(aw("KEYWORD"))
            + Optional(Literal("(")).setParseAction(aw("MARKER"))
            + condition
            + Optional(Literal(")")).setParseAction(aw("MARKER"))
            + Keyword("THEN").setParseAction(aw("KEYWORD"))
            + block
        )
        + Optional(Keyword("ELSE").setParseAction(aw("KEYWORD")) + block)
        + Keyword("END_IF").setParseAction(aw("KEYWORD"))
        + semicolon
    )
    | (
        Keyword("CASE").setParseAction(aw("KEYWORD"))
        + designator
        + Optional(actpars).setParseAction(aw("METHOD_IDENTIFIER"))
        + Keyword("OF").setParseAction(aw("KEYWORD"))
        + OneOrMore(caseblock)
        + Optional(Keyword("ELSE").setParseAction(aw("KEYWORD")) + block)
        + Keyword("END_CASE").setParseAction(aw("KEYWORD"))
        + semicolon
    )
    | (Keyword("RETURN").setParseAction(aw("KEYWORD")) + semicolon)
)



parser = (
    (Keyword("PROGRAM")
    | Keyword("FUNCTION_BLOCK")
    | Keyword("FUNCTION")).setParseAction(aw("KEYWORD"))
    + ident
    + Optional(Suppress(":") + ident)
    + ZeroOrMore(var_decl)
    + ZeroOrMore(statement)
    + oneOf("END_PROGRAM END_FUNCTION_BLOCK END_FUNCTION").setParseAction(aw("KEYWORD"))
)

