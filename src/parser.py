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
    oneOf("VAR_INPUT VAR_OUTPUT VAR_IN_OUT VAR VAR_EXTERNAL").setParseAction(aw("KEYWORD"))
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

signed_real_number = Optional("-") + Word(nums) + Optional(
        Literal(".")
        + Word(nums)
        + Optional(Literal("E") + Optional(Literal("-")) + Word(nums))
    )
signed_integer = Optional(oneOf("+ -")) + Word(nums)
binary_integer = "2#" + Word("10_")
octal_integer = "8#" + Word("01234567")
hex_integer = "16#" + Word(nums+"ABCDEF")
integer_type_name = oneOf("SINT INT DINT LINT USINT UINT UDINT ULINT")
real_type_name = oneOf("REAL LREAL")
integer_literal = Combine(Optional(integer_type_name + "#") + (binary_integer | octal_integer | hex_integer | signed_real_number))
real_literal = Combine(Optional(real_type_name + "#") + signed_real_number)
numeric_literal = integer_literal | real_literal
character_string = Combine(Optional(oneOf("STRING WSTRING") + "#") + (QuotedString('"') | QuotedString("'")))
duration = Combine(oneOf("T TIME").setParseAction(aw("KEYWORD")) + "#" + Optional("-") + Word(alphanums))
time_of_day = Combine(oneOf("TIME_OF_DAY TOD").setParseAction(aw("KEYWORD")) + "#" + Word(alphanums))
time_literal = duration | time_of_day
bit_string_literal = Combine(oneOf("BYTE WORD DWORD LWORD").setParseAction(aw("KEYWORD")) + "#" + Word(alphanums + "_" + "-" + "#"))
boolean_literal = Combine(Optional("BOOL#").setParseAction(aw("KEYWORD")) + oneOf("1 0 TRUE FALSE").setParseAction(aw("KEYWORD")))

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
        + Word(alphanums + "_" + "-" + "#" + ".")
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
exit_statement = Keyword("EXIT").setParseAction(aw("KEYWORD"))

statement << (
    (
        Keyword("REPEAT").setParseAction(aw("KEYWORD"))
        + block
        + Keyword("UNTIL").setParseAction(aw("KEYWORD"))
        + expression
        + Keyword("END_REPEAT").setParseAction(aw("KEYWORD"))
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
    | exit_statement + semicolon
    | semicolon
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
