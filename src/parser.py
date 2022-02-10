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
    dblSlashComment
)


def aw(tokentype):
    return partial(annotate, tokentype)


def annotate(tokentype, t):
    return (tokentype, t[0]) if t else []

param = Forward()
actpars = (
    Literal("(").setParseAction(aw("METHOD_MARKER"))
    + Optional(param + ZeroOrMore(Literal(",").setParseAction(aw("MARKER")) + param))
    + Literal(")").setParseAction(aw("METHOD_MARKER"))
)

semicolon = Literal(";").setParseAction(aw("MARKER"))
converter = oneOf("WORD_TO_BLOCK_DB BLOCK_DB_TO_WORD TEST_DB DWORD_TO_INT WORD_TO_INT DWORD_TO_REAL BYTE_TO_BOOL BYTE_TO_CHAR CHAR_TO_BYTE CHAR_TO_INT \
                DATE_TO_DINT DINT_TO_DATE DINT_TO_DWORD DINT_TO_INT DINT_TO_TIME DINT_TO_TOD DWORD_TO_BOOL DWORD_TO_BYTE DWORD_TO_DINT DWORD_TO_REAL DWORD_TO_WORD INT_TO_CHAR INT_TO_WORD \
                REAL_TO_DINT REAL_TO_DWORD REAL_TO_INT STRING_TO_CHAR TIME_TO_DINT TOD_TO_DINT WORD_TO_BOOL WORD_TO_DBYTE WORD_TO_INT")
#ident = converter + Literal("(").setParseAction(aw("MARKER")) + Word(alphas + "_", alphanums + "_").setParseAction(aw("IDENTIFIER")) + Literal(")").setParseAction(aw("MARKER")) \
ident = converter + actpars \
        | Optional(alphas + Literal("AT")) + Word(alphas + "_", alphanums + "_").setParseAction(aw("IDENTIFIER"))


dtype = Word(alphas + "_", alphanums + "_").setParseAction(aw("DATATYPE"))

assign_op = Literal(":=").setParseAction(aw("OPERATOR")) | Literal("=>").setParseAction(aw("OPERATOR"))

expression = Forward()
const_declaration = ident + assign_op + expression
pragma = Literal("{").setParseAction(aw("MARKER")) + OneOrMore(const_declaration + Optional(semicolon)) + Literal("}").setParseAction(aw("MARKER"))

primary_expression = Forward()

designator = ident + ZeroOrMore(
    (Literal(".").setParseAction(aw("MARKER")) + ident)
    | (
        Literal("[").setParseAction(aw("MARKER"))
        + OneOrMore(expression + (Optional(Literal(",")).suppress()))
        + Literal("]").setParseAction(aw("MARKER"))
    )
    | pragma
)
integer = Word(nums + "_").setParseAction(aw("LITERAL"))


mulop = (Literal("*") | Literal("/") | Literal("MOD")).setParseAction(aw("OPERATOR"))
addop = (Literal("+") | Literal("-")).setParseAction(aw("OPERATOR"))


subrange = Combine(Word(nums) + Literal("..") + Word(nums))

non_generic_type_name = dtype
array_specification = oneOf("ARRAY Array").setParseAction(aw("KEYWORD")) + Literal("[").setParseAction(aw("MARKER")) + subrange.setParseAction(aw("MARKER")) + ZeroOrMore(Literal(",").setParseAction(aw("MARKER")) + subrange) + Literal("]").setParseAction(aw("MARKER")) + Literal("OF").setParseAction(aw("KEYWORD")) + non_generic_type_name

struct_specification = Literal("STRUCT").setParseAction(aw("KEYWORD")) + ZeroOrMore(ident + Suppress(Literal(":")) + non_generic_type_name + semicolon) + Literal("END_STRUCT").setParseAction(aw("KEYWORD"))

var_init_decl = designator + ZeroOrMore(Literal(",").setParseAction(aw("MARKER")) + designator) + Optional(Keyword("AT").setParseAction(aw("KEYWORD")) + designator) + Suppress(Literal(":")) + (struct_specification | array_specification | (dtype + Optional(assign_op + expression)))

input_declaration = var_init_decl


var_decl = (
    oneOf("VAR_INPUT VAR_OUTPUT VAR_IN_OUT VAR VAR_TEMP VAR_EXTERNAL").setParseAction(aw("KEYWORD"))
    + Optional(
        Literal("CONSTANT").setParseAction(aw("KEYWORD"))
        | Literal("RETAIN").setParseAction(aw("KEYWORD"))
        | Literal("NON_RETAIN").setParseAction(aw("KEYWORD"))
    )
    + ZeroOrMore(
        input_declaration
        + semicolon
    )
    + Keyword("END_VAR").setParseAction(aw("KEYWORD"))
)

const_decl = (
    Keyword("CONST").setParseAction(aw("KEYWORD"))
    + Optional(
        Literal("CONSTANT").setParseAction(aw("KEYWORD"))
        | Literal("RETAIN").setParseAction(aw("KEYWORD"))
        | Literal("NON_RETAIN").setParseAction(aw("KEYWORD"))
    )
    + ZeroOrMore(
        const_declaration
        + semicolon
    )
    + Keyword("END_CONST").setParseAction(aw("KEYWORD"))
)

label_decl = (
    Keyword("LABEL").setParseAction(aw("KEYWORD"))
    + ZeroOrMore(
        ident + semicolon
    )
    + Keyword("END_LABEL").setParseAction(aw("KEYWORD"))
)


relop = (Literal(">=") | Literal(">") | Literal("<=") | Literal("<")).setParseAction(
    aw("OPERATOR")
)
booleanop = (Literal("AND") | Literal("OR")).setParseAction(aw("KEYWORD"))


arithmeticop = (
    Literal("+") | Literal("-") | Literal("*") | Literal("/")
).setParseAction(aw("OPERATOR"))



signed_real_number = Optional("-") + Word(nums) + Optional(
        Literal(".")
        + Word(nums)
        + Optional(oneOf("E e") + Optional(oneOf("- +")) + Word(nums))
    )
signed_integer = Optional(oneOf("+ -")) + Word(nums)
binary_integer = "2#" + Word("10_")
octal_integer = "8#" + Word("01234567")
hex_integer = "16#" + Word(nums+"ABCDEF")
integer_type_name = oneOf("SINT INT DINT LINT USINT UINT UDINT ULINT sint int dint lint usint uint udint ulint")
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

blockattr_decl = (
    Literal("VERSION").setParseAction(aw("KEYWORD")) + Literal(":").setParseAction(aw("KEYWORD")) + constant
    | oneOf("AUTHOR FAMILY NAME").setParseAction(aw("KEYWORD")) + Literal(":").setParseAction(aw("KEYWORD")) + ( ident | constant)
    | Literal("TITLE").setParseAction(aw("KEYWORD")) + Literal("=").setParseAction(aw("KEYWORD")) + constant
    | Literal("KNOW_HOW_PROTECT").setParseAction(aw("KEYWORD"))
)


primary_expression << (
    constant.setParseAction(aw("LITERAL"))
    | Combine(
        oneOf("DATE TOD DATE_AND_TIME DT t")
        + Literal("#")
        + Word(alphanums + "_" + "-" + "#" + "." + ":")
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
                | booleanop + oneOf("NOT not").setParseAction(aw("KEYWORD"))
            )
            + expression
        )
    )
)

unary_operator = Literal("-").setParseAction(aw("OPERATOR")) | oneOf(
    "NOT not"
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
        | oneOf("AND and").setParseAction(aw("OPERATOR"))
    )
    + comparison
)
xor_expression = and_expression + ZeroOrMore(
    oneOf("XOR xor").setParseAction(aw("OPERATOR")) + and_expression
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
case_list_element = subrange | Word(nums) | enumerated_value
case_list = case_list_element + ZeroOrMore("," + case_list_element)
case_element = case_list.setParseAction(aw("MARKER")) + Suppress(Literal(":")) + block
for_list = expression + Keyword("TO").setParseAction(aw("KEYWORD")) + expression + Optional(Keyword("BY").setParseAction(aw("KEYWORD")) + expression)
exit_statement = oneOf("EXIT Exit exit").setParseAction(aw("KEYWORD"))

statement << (
    (designator + ((assign_op + expression) | actpars) + semicolon)
    | (
        Keyword("REPEAT").setParseAction(aw("KEYWORD"))
        + block
        + Keyword("UNTIL").setParseAction(aw("KEYWORD"))
        + expression
        + Keyword("END_REPEAT").setParseAction(aw("KEYWORD"))
    )
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
        (oneOf("CASE Case case")).setParseAction(aw("KEYWORD"))
        + expression
        + Keyword("OF").setParseAction(aw("KEYWORD"))
        + OneOrMore(case_element)
        + Optional(Keyword("ELSE").setParseAction(aw("KEYWORD")) + block)
        + Keyword("END_CASE").setParseAction(aw("KEYWORD"))
        + semicolon
    )
    | (Keyword("RETURN").setParseAction(aw("KEYWORD")) + semicolon)
    | exit_statement + semicolon
    | ident + Literal(":").suppress() + semicolon
    | (Keyword("GOTO").setParseAction(aw("KEYWORD")) + ident + semicolon)
    | semicolon
)



function_block = (Keyword("PROGRAM") | Keyword("FUNCTION_BLOCK") | Keyword("FUNCTION")).setParseAction(aw("KEYWORD"))\
    + ident \
    + Optional(Suppress(":") + ident) \
    + ZeroOrMore(blockattr_decl) \
    + ZeroOrMore(pragma) \
    + ZeroOrMore(var_decl) \
    + ZeroOrMore(const_decl) \
    + ZeroOrMore(label_decl) \
    + Optional(Keyword("BEGIN")).setParseAction(aw("KEYWORD")) \
    + ZeroOrMore(statement) \
    + oneOf("END_PROGRAM END_FUNCTION_BLOCK END_FUNCTION").setParseAction(aw("KEYWORD"))


parser = (ZeroOrMore(pragma) + OneOrMore(function_block)).ignore(dblSlashComment)