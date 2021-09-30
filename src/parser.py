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
    Suppress,
    Combine,
    alphanums,
    QuotedString,
)


def aw(tokentype):
    return partial(annotate, tokentype)


def annotate(tokentype, t):
    return (tokentype, t[0]) if t else []


semicolon = Literal(";").setParseAction(aw("MARKER"))
ident = Word(alphas + "_", alphanums + "_").setParseAction(aw("IDENTIFIER"))
dtype = Word(alphas + "_", alphanums + "_").setParseAction(aw("DATATYPE"))
expression = Forward()
designator = ident + ZeroOrMore(
    (Literal(".").setParseAction(aw("MARKER")) + ident)
    | (
        Literal("[").setParseAction(aw("MARKER"))
        + expression
        + Literal("]").setParseAction(aw("MARKER"))
    )
)


assign_op = Literal(":=").setParseAction(aw("OPERATOR"))
mulop = (Literal("*") | Literal("/") | Literal("MOD")).setParseAction(aw("OPERATOR"))
addop = (Literal("+") | Literal("-")).setParseAction(aw("OPERATOR"))
var_decl = (
    oneOf("VAR_INPUT VAR_OUTPUT VAR_IN_OUT VAR").setParseAction(aw("KEYWORD"))
    + Optional(
        Literal("CONSTANT").setParseAction(aw("KEYWORD"))
        | Literal("RETAIN").setParseAction(aw("KEYWORD"))
        | Literal("NON_RETAIN").setParseAction(aw("KEYWORD"))
    )
    + ZeroOrMore(
        designator
        + Suppress(Literal(":"))
        + dtype
        + Optional(assign_op + expression)
        + semicolon
    )
    + Keyword("END_VAR").setParseAction(aw("KEYWORD"))
)
relop = (Literal(">=") | Literal(">") | Literal("<=") | Literal("<")).setParseAction(
    aw("OPERATOR")
)
booleanop = (Literal("AND") | Literal("OR")).setParseAction(aw("KEYWORD"))


arithmeticop = (
    Literal("+") | Literal("-") | Literal("*") | Literal("/")
).setParseAction(aw("OPERATOR"))

param = Forward()
actpars = (
    Literal("(").setParseAction(aw("METHOD_MARKER"))
    + Optional(param + ZeroOrMore(Literal(",").setParseAction(aw("MARKER")) + param))
    + Literal(")").setParseAction(aw("METHOD_MARKER"))
)

single_byte_character = Literal("\\") + Literal("'")
double_byte_character = Literal('"')

number_literal = Combine(
    Optional(oneOf("REAL LREAL SINT INT DINT LINT USINT UINT UDINT ULINT") + "#")
    + Optional("-")
    + Word(nums)
    + Optional(
        Literal(".")
        + Word(nums)
        + Optional(Literal("E") + Optional(Literal("-")) + Word(nums))
    )
).setParseAction(aw("LITERAL"))

numeric_literal = number_literal
character_string = (QuotedString('"') | QuotedString("'")).setParseAction(aw("LITERAL"))
duration = Combine(oneOf("T Time") + "#" + Optional("-") + Word(alphanums))
time_of_day = Combine(oneOf("TIME_OF_DAY TOD") + "#" + Word(alphanums))
time_literal = duration | time_of_day
bit_string_literal = Combine(oneOf("BYTE WORD DWORD LWORD") + "#" + Word(nums + "_" + "-" + "#"))
boolean_literal = Combine(Optional("BOOL#") + oneOf("1 0 TRUE FALSE"))
constant = (
    numeric_literal
    | character_string
    | time_literal
    | bit_string_literal
    | boolean_literal
)

primary_expression = (
    constant.setParseAction(aw("LITERAL"))
    | Combine(
        oneOf("DATE TOD DATE_AND_TIME DT t")
        + Literal("#")
        + Word(alphanums + "_" + "-" + "#")
    ).setParseAction(aw("LITERAL"))
    | (designator + Optional(actpars))
    | (
        Literal("(").setParseAction(aw("MARKER"))
        + expression
        + Literal(")").setParseAction(aw("MARKER"))
    )
)

param << (
    expression
    + Optional(
        Optional(assign_op + expression)
        + ZeroOrMore(
            (
                relop
                | arithmeticop
                | booleanop + Optional("NOT").setParseAction(aw("KEYWORD"))
            )
            + expression
        )
    )
)

unary_operator = Literal("-").setParseAction(aw("OPERATOR")) | Literal(
    "NOT"
).setParseAction(aw("OPERATOR"))
unary_expression = Optional(unary_operator) + primary_expression
power_expression = unary_expression + ZeroOrMore(
    Literal("**").setParseAction(aw("OPERATOR")) + unary_expression
)
term = power_expression + ZeroOrMore(mulop + power_expression)
add_expression = term + ZeroOrMore(addop + term)
equ_expression = add_expression + ZeroOrMore(relop + add_expression)
comparison = equ_expression + ZeroOrMore(
    (
        Literal("=").setParseAction(aw("OPERATOR"))
        | Literal("<>").setParseAction(aw("OPERATOR"))
    )
    + equ_expression
)
and_expression = comparison + ZeroOrMore(
    (
        Literal("&").setParseAction(aw("OPERATOR"))
        | Literal("AND").setParseAction(aw("OPERATOR"))
    )
    + comparison
)
xor_expression = and_expression + ZeroOrMore(
    Literal("XOR").setParseAction(aw("OPERATOR")) + and_expression
)
expression << (
    xor_expression
    + ZeroOrMore(Literal("OR").setParseAction(aw("OPERATOR")) + xor_expression)
)


statement = Forward()
block = ZeroOrMore(statement)
count_condition = (
    designator
    + assign_op
    + expression
    + Keyword("TO").setParseAction(aw("KEYWORD"))
    + expression
)

enumerated_value = Combine(Optional(ident + "#") + ident)
subrange = Combine(Word(nums) + Literal("..") + Word(nums))
case_list_element = subrange | Word(nums) | enumerated_value
case_list = case_list_element + ZeroOrMore("," + case_list_element)
case_element = case_list.setParseAction(aw("MARKER")) + Suppress(Literal(":")) + block
for_list = expression + Keyword("TO").setParseAction(aw("KEYWORD")) + expression + Optional(Keyword("BY").setParseAction(aw("KEYWORD")) + expression)

statement << (
    (
        Keyword("REPEAT").setParseAction(aw("KEYWORD"))
        + block
        + Keyword("UNTIL").setParseAction(aw("KEYWORD"))
        + expression
        + semicolon
        + Keyword("END_REPEAT").setParseAction(aw("KEYWORD"))
        + semicolon
    )
    | (designator + ((assign_op + expression) | actpars) + semicolon)
    | (
        Keyword("FOR").setParseAction(aw("KEYWORD"))
        + ident
        + assign_op
        + for_list
        + Keyword("DO").setParseAction(aw("KEYWORD"))
        + block
        + Keyword("END_FOR").setParseAction(aw("KEYWORD"))
        + semicolon
    )
    | (
        Keyword("WHILE").setParseAction(aw("KEYWORD"))
        + expression
        + Keyword("DO").setParseAction(aw("KEYWORD"))
        + block
        + Keyword("END_WHILE").setParseAction(aw("KEYWORD"))
        + semicolon
    )
    | (
        Keyword("IF").setParseAction(aw("KEYWORD"))
        + expression
        + Keyword("THEN").setParseAction(aw("KEYWORD"))
        + block
        + ZeroOrMore(
            Keyword("ELSIF").setParseAction(aw("KEYWORD"))
            + expression
            + Keyword("THEN").setParseAction(aw("KEYWORD"))
            + block
        )
        + Optional(Keyword("ELSE").setParseAction(aw("KEYWORD")) + block)
        + Keyword("END_IF").setParseAction(aw("KEYWORD"))
        + semicolon
    )
    | (
        Keyword("CASE").setParseAction(aw("KEYWORD"))
        + expression
        + Keyword("OF").setParseAction(aw("KEYWORD"))
        + OneOrMore(case_element)
        + Optional(Keyword("ELSE").setParseAction(aw("KEYWORD")) + block)
        + Keyword("END_CASE").setParseAction(aw("KEYWORD"))
        + semicolon
    )
    | (Keyword("RETURN").setParseAction(aw("KEYWORD")) + semicolon)
)

parser = (
    (
        Keyword("PROGRAM") | Keyword("FUNCTION_BLOCK") | Keyword("FUNCTION")
    ).setParseAction(aw("KEYWORD"))
    + ident
    + Optional(Suppress(":") + ident)
    + ZeroOrMore(var_decl)
    + ZeroOrMore(statement)
    + oneOf("END_PROGRAM END_FUNCTION_BLOCK END_FUNCTION").setParseAction(aw("KEYWORD"))
)
