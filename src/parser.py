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
    alphas
)



letter = alphas
digit = nums
octal_digit = (Literal("0") | Literal("1") | Literal("2") | Literal("3") | Literal("4") | Literal("5") | Literal("6") | Literal("7"))

hex_digit = (digit | Literal("A")| Literal("B") | Literal("C") | Literal("D") | Literal("E") | Literal("F"))
identifier = (letter | (Literal("_") + (letter | digit))) + ZeroOrMore(Optional("_") + (letter | digit))

integer = digit + ZeroOrMore(Optional("_" + digit))
signed_integer = Optional(Literal("+") | Literal("-")) + integer

fixed_point = integer + Optional("." + integer)
milliseconds = fixed_point ("ms")
seconds = ((fixed_point +"s") | (integer + "s")) + Optional("_") + milliseconds
minutes = ((fixed_point +"m") | (integer + "m")) + Optional("_") + seconds
hours = ((fixed_point + "h") | (integer + "h")) + Optional("_") + minutes
days = ((fixed_point + "d") | (integer  + "d")) + Optional("_") +hours
interval = days | hours | minutes | seconds | milliseconds


day_hour = integer
day_minute = integer
day_second = fixed_point
year = integer
month = integer
day = integer
date_literal = year + "-" + month + "-" + day
date = (Literal("DATE") | Literal("D")) + "#" + date_literal
daytime = day_hour + ":" + day_minute + ":" + day_second
date_and_time = (Literal("DATE_AND_TIME") | Literal("DT")) + "#" + date_literal + "-" + daytime
time_of_day = (Literal("TIME_OF_DAY") | Literal("TOD")) + "#" + daytime

string_type_name = identifier
simple_type_name = identifier
subrange_type_name = identifier
enumerated_type_name = identifier
array_type_name = identifier
structure_type_name = identifier
single_element_type_name = simple_type_name | subrange_type_name | enumerated_type_name
derived_type_name = single_element_type_name | array_type_name | structure_type_name | string_type_name
generic_type_name = (Keyword("ANY") | Keyword("ANY_DERIVED") | Keyword("ANY_ELEMENTARY") | Keyword("ANY_MAGNITUDE") | Keyword("ANY_NUM") | Keyword("ANY_REAL") | Keyword("ANY_INT") | Keyword("ANY_BIT") | Keyword("ANY_STRING") | Keyword("ANY_DATE"))
bit_string_type_name = (Keyword("BOOL") | Keyword("BYTE") | Keyword("WORD") | Keyword("DWORD") | Keyword("LWORD"))
date_type_name = (Keyword("DATE") | Keyword("TIME_OF_DAY") | Keyword("TOD") | Keyword("DATE_AND_TIME") | Keyword("DT"))
real_type_name = (Keyword("REAL") | Keyword("LREAL"))
unsigned_integer_type_name = (Keyword("USINT") | Keyword("UINT") | Keyword("UDINT") | Keyword("ULINT"))
signed_integer_type_name = (Keyword("SINT") | Keyword("INT") | Keyword("DINT") | Keyword("LINT"))
integer_type_name = signed_integer_type_name | unsigned_integer_type_name
numeric_type_name = integer_type_name | real_type_name
elementary_type_name = (numeric_type_name | date_type_name | bit_string_type_name| Keyword("STRING") | Keyword("WSTRING") | Keyword("TIME"))
non_generic_type_name = elementary_type_name | derived_type_name
data_type_name = non_generic_type_name | generic_type_name

variable_name = identifier

field_selector = identifier

location_prefix = (Literal("I") | Literal("Q") | Literal("M"))
size_prefix = (Literal("X") | Literal("B") | Literal("W") | Literal("D") | Literal("L"))

bit = (Literal("1") | Literal("0"))
direct_variable = "%" + location_prefix + size_prefix + integer + ZeroOrMore("." + integer)
binary_integer = "2#" + bit + ZeroOrMore(Optional("_") + bit)
location_prefix = (Literal("I") | Literal("Q") | Literal("M"))
size_prefix =  Literal("X") | Literal("B") | Literal("W") | Literal("D") | Literal("L")
octal_integer = "8#" + octal_digit + ZeroOrMore(Optional("_") + octal_digit)
hex_integer = "16#" + hex_digit + ZeroOrMore(Optional("_") + hex_digit)

expression = Forward()

array_variable = Forward()
multi_element_variable = Forward()
subscript = expression
subscript_list = "[" + subscript + ZeroOrMore("," + subscript) + "]"
symbolic_variable = variable_name | multi_element_variable
record_variable = symbolic_variable
structured_variable = record_variable + "." + field_selector
multi_element_variable << (array_variable | structured_variable)
subscripted_variable = symbolic_variable
array_variable << (subscripted_variable + subscript_list)
integer_literal = Optional(integer_type_name + Literal("#")) + ( signed_integer | binary_integer | octal_integer | hex_integer)
exponent = (Literal("E") | Literal("e")) + Optional(Literal("+")| Literal("-")) + integer
real_literal = Optional(real_type_name + "#") + signed_integer + "." + integer + Optional(exponent)
numeric_literal = (integer_literal | real_literal)
single_byte_character_string = Literal(""" {single_byte_character_representation} """)
double_byte_character_string = Literal(""" {double_byte_character_representation} """)
character_string = single_byte_character_string | double_byte_character_string
duration = (Literal("T") | Literal("TIME")) + "#" + Optional("-") + interval
time_literal = duration | time_of_day
bit_string_literal = Optional( (Literal("BYTE") | Literal("WORD") | Literal("DWORD") | Literal("LWORD")) + Literal("#") ) + ( signed_integer | binary_integer | octal_integer | hex_integer)
boolean_literal = ( Optional("BOOL#") + (Keyword("1") | Keyword("0") ) ) | Keyword("TRUE") | Keyword("FALSE")
constant = (numeric_literal | character_string | time_literal | bit_string_literal | boolean_literal)

array_initialization = Forward()
structure_initialization = Forward()

subrange = signed_integer + ".." + signed_integer
structure_element_name = identifier
simple_specification = elementary_type_name | simple_type_name
simple_spec_init = simple_specification + Optional(":=" + constant)
subrange_specification = (integer_type_name + "(" + subrange +")") | subrange_type_name
subrange_spec_init = subrange_specification + Optional(":=" + signed_integer)
enumerated_value = Optional(enumerated_type_name + "#") + identifier
enumerated_specification = ("(" + enumerated_value + ZeroOrMore("," + enumerated_value) + ")") | enumerated_type_name
enumerated_spec_init = enumerated_specification + Optional(":=" + enumerated_value)
array_specification = array_type_name | ("ARRAY" + "[" + subrange + ZeroOrMore("," + subrange) + "]" + "OF" + non_generic_type_name)
array_spec_init = array_specification + Optional(":=" + array_initialization)
structure_element_initialization = structure_element_name + ":=" + (constant | enumerated_value | array_initialization | structure_initialization)
structure_initialization << ("(" + structure_element_initialization + ZeroOrMore("," + structure_element_initialization) + ")")
initialized_structure =structure_type_name + Optional(":=" + structure_initialization)
structure_element_declaration = structure_element_name + ":" + (simple_spec_init |subrange_spec_init | enumerated_spec_init | array_spec_init | initialized_structure)
structure_declaration ="STRUCT" + structure_element_declaration + ";" + ZeroOrMore(structure_element_declaration + ";") + "END_STRUCT"
array_initial_element = constant | enumerated_value | structure_initialization | array_initialization
array_initial_elements = array_initial_element | (integer + "(" + Optional(array_initial_element) + ")")
array_initialization << ("[" + array_initial_elements + ZeroOrMore("," + array_initial_elements) + "]")
subrange_type_declaration = subrange_type_name + ":" + subrange_spec_init
simple_type_declaration = simple_type_name + ":" + simple_spec_init
enumerated_type_declaration = enumerated_type_name + ":" + enumerated_spec_init
single_element_type_declaration = simple_type_declaration | subrange_type_declaration | enumerated_type_declaration
array_type_declaration = array_type_name + ":" + array_spec_init
structure_specification = structure_declaration | initialized_structure
string_type_declaration = string_type_name + ":" + (Keyword("STRING")|Keyword("WSTRING")) + Optional("[" + integer + "]") + Optional(":=" + character_string)
structure_type_declaration = structure_type_name + ":" + structure_specification
type_declaration = single_element_type_declaration | array_type_declaration | structure_type_declaration | string_type_declaration
data_type_declaration = Keyword("TYPE") + type_declaration + ";" + ZeroOrMore(type_declaration + ";") + Keyword("END_TYPE")

variable = direct_variable | symbolic_variable

statement = Forward()


case_list_element = subrange | signed_integer | enumerated_value
case_list = case_list_element + ZeroOrMore("," + case_list_element)
assignment_statement = variable + ":=" + expression
fb_name = identifier
param_assignment = (Optional(variable_name + ":=") + expression) | (Optional("NOT") + variable_name + "=>" + variable)
fb_invocation = fb_name + "(" + Optional(param_assignment + ZeroOrMore("," + param_assignment)) + ")"
subprogram_control_statement = fb_invocation | "RETURN"
statement_list = statement + ";" + ZeroOrMore(statement + ";")
if_statement = "IF" + expression + "THEN" + statement_list + ZeroOrMore("ELSIF" + expression + "THEN" + statement_list) + Optional("ELSE" + statement_list) + "END_IF"
case_element = case_list + ":" + statement_list
case_statement = "CASE" + expression + "OF" + case_element + ZeroOrMore(case_element) + Optional("ELSE" + statement_list) + "END_CASE"
selection_statement = if_statement | case_statement

exit_statement = "EXIT"
repeat_statement = "REPEAT" + statement_list + "UNTIL"  + expression + "END_REPEAT"
while_statement = "WHILE" + expression + "DO" + statement_list + "END_WHILE"
for_list = expression + "TO" + expression + Optional("BY" + expression)
control_variable = identifier
for_statement = "FOR" + control_variable + ":=" + for_list + "DO" + statement_list + "END_FOR"
iteration_statement = for_statement | while_statement | repeat_statement | exit_statement

statement << (assignment_statement | subprogram_control_statement| selection_statement | iteration_statement)




var1_list = variable_name + ZeroOrMore("," + variable_name)
array_var_init_decl = var1_list + ":" + array_spec_init
structured_var_init_decl = var1_list + ":" + initialized_structure
fb_name_list = fb_name  + ZeroOrMore("," + fb_name)
fb_name_decl = fb_name_list + ":" + identifier + Optional(":=" + structure_initialization)



add_operator = Literal("+") | Literal("-")


primary_expression = constant | enumerated_value | variable | "(" + expression + ")" | + identifier + "(" + param_assignment + ZeroOrMore("," + param_assignment) + ")"
unary_operator = Literal("-") | Literal("NOT")
unary_expression = Optional(unary_operator) + primary_expression
power_expression = unary_expression + ZeroOrMore("**" + unary_expression)
multiply_operator = Literal("*") | Literal("/") | Literal("MOD")
term = power_expression + ZeroOrMore(multiply_operator + power_expression)


comparison_operator = Literal("<") | Literal(">") | Literal("<=") | Literal(">=")
add_expression = term + ZeroOrMore(add_operator + term)
equ_expression = add_expression + ZeroOrMore(comparison_operator + add_expression)
comparison = equ_expression + ZeroOrMore((Literal("=") | Literal("<>")) + equ_expression)
and_expression = comparison + ZeroOrMore((Literal("&") | Literal("AND"))+ comparison)
xor_expression = and_expression + ZeroOrMore(Literal("XOR") + and_expression)
expression << (xor_expression + ZeroOrMore(Literal("OR") + xor_expression))



subscript = expression

common_character_representation = Literal("$$") | Literal("$L") | Literal("$N") | Literal("$P") | Literal("$R") | Literal("$T") | Literal("$l") | Literal("$n") | Literal("$p") | Literal("$r") | Literal("$t")
single_byte_character_representation = (common_character_representation | "$"" | """ |"$") + hex_digit + hex_digit
double_byte_character_representation = (common_character_representation | "$"" | """|"$") + hex_digit + hex_digit + hex_digit + hex_digit






symbolic_variable = variable_name | multi_element_variable
variable_name = identifier



multi_element_variable = array_variable | structured_variable
array_variable = subscripted_variable + subscript_list
subscripted_variable = symbolic_variable

global_var_name = identifier
single_byte_string_spec = "STRING" + Optional("[" + integer + "]") + Optional(":=" + single_byte_character_string)
double_byte_string_spec = "WSTRING" + Optional("[" + integer + "]") + Optional(":=" + double_byte_character_string)
location = "AT" + direct_variable
global_var_list = global_var_name + ZeroOrMore("," + global_var_name)
global_var_spec = global_var_list | (Optional(global_var_name) + location)
located_var_spec_init = simple_spec_init | subrange_spec_init | enumerated_spec_init | array_spec_init | initialized_structure | single_byte_string_spec | double_byte_string_spec
single_byte_string_var_declaration = var1_list + ":" + single_byte_string_spec
double_byte_string_var_declaration = var1_list + ":" + double_byte_string_spec
string_var_declaration = single_byte_string_var_declaration | double_byte_string_var_declaration

edge_declaration = var1_list + ":" + "BOOL" + (Literal("R_EDGE") | Literal("F_EDGE"))
var1_init_decl = var1_list + ":" + (simple_spec_init | subrange_spec_init | enumerated_spec_init)
var_init_decl = var1_init_decl | array_var_init_decl | structured_var_init_decl | fb_name_decl | string_var_declaration
input_declaration = var_init_decl | edge_declaration
input_declarations = "VAR_INPUT" + Optional(Literal("RETAIN") | Literal("NON_RETAIN")) + input_declaration + ";" + ZeroOrMore(input_declaration + ";") + "END_VAR"



var1_declaration = var1_list + ":" + (simple_specification | subrange_specification | enumerated_specification)
array_var_declaration = var1_list + ":" + array_specification
structured_var_declaration = var1_list + ":" + structure_type_name
temp_var_decl = var1_declaration | array_var_declaration | structured_var_declaration |string_var_declaration
var_declaration = temp_var_decl | fb_name_decl
var_declarations = "VAR" + Optional("CONSTANT") + var_init_decl + ";" + ZeroOrMore(var_init_decl + ";") +  "END_VAR"
output_declarations = Keyword("VAR_OUTPUT") + Optional(Keyword("RETAIN") | Keyword("NON_RETAIN")) + var_init_decl + ";" + ZeroOrMore(var_init_decl + ";") + "END_VAR"
input_output_declarations = Keyword("VAR_IN_OUT") + var_declaration + ";" + ZeroOrMore(var_declaration + ";") + "END_VAR"


retentive_var_declarations = "VAR" + "RETAIN" + var_init_decl + ";" + ZeroOrMore(var_init_decl + ";") +  "END_VAR"

located_var_decl = Optional(variable_name) + location + ":" + located_var_spec_init
located_var_declarations = "VAR"+ Optional(Keyword("CONSTANT") | Keyword("RETAIN") | Keyword("NON_RETAIN")) + located_var_decl + ";" + ZeroOrMore(located_var_decl + ";") + "END_VAR"

external_declaration = global_var_name + ":" + (simple_specification | subrange_specification | enumerated_specification | array_specification | structure_type_name | identifier)
external_var_declarations = "VAR_EXTERNAL" + Optional("CONSTANT") + external_declaration + ";" + ZeroOrMore(external_declaration + ";") + "END_VAR"


global_var_decl = global_var_spec + ":" + Optional(located_var_spec_init | identifier)
global_var_declarations = "VAR_GLOBAL" + Optional("CONSTANT" | "RETAIN") + global_var_decl + ";" + ZeroOrMore(global_var_decl + ";") + "END_VAR"





var_spec = simple_specification | subrange_specification | enumerated_specification | array_specification | structure_type_name | ("STRING" + Optional("[" + integer + "]") ) | ("WSTRING" + Optional("[" + integer + "]"))
incompl_location = "AT" + "%" + (Literal("I") | Literal("Q") | Literal("M")) + "*"
incompl_located_var_decl = variable_name + incompl_location + ":" + var_spec
incompl_located_var_declarations = "VAR" + Optional("RETAIN"|"NON_RETAIN") + incompl_located_var_decl + ";" + ZeroOrMore(incompl_located_var_decl + ";") + "END_VAR"



program_name = identifier
task_name = identifier
data_source = constant | direct_variable
task_initialization = "(" + Optional("SINGLE" ":=" + data_source + ",") + Optional("INTERVAL" + ":=" + data_source + ",")
direction = Keyword("READ_WRITE") | Keyword("READ_ONLY")
task_configuration = "TASK" + task_name + task_initialization

program_type_name = identifier
resource_name = identifier
function_block_type_name = identifier
global_var_reference = Optional(resource_name + ".") + global_var_name + Optional("." + structure_element_name)
function_name = identifier

instance_specific_init = resource_name + "." + program_name + "." + ZeroOrMore(fb_name + ".") + ((variable_name + Optional(location) + "." + located_var_spec_init) | (fb_name + ":" + identifier + ":=" + structure_initialization))

fb_task = fb_name + "WITH" + task_name
data_sink = global_var_reference | direct_variable
prog_data_source = constant | enumerated_value | global_var_reference | direct_variable
prog_cnxn = symbolic_variable + ":=" + prog_data_source | symbolic_variable + "=>" + data_sink
prog_conf_element = fb_task | prog_cnxn
prog_conf_elements = prog_conf_element + ZeroOrMore("," + prog_conf_element)

fb_task = fb_name + "WITH" + task_name
prog_data_source = constant | enumerated_value | global_var_reference | direct_variable
prog_cnxn = symbolic_variable + ":=" + (prog_data_source | symbolic_variable) + "=>" + data_sink
instance_specific_initializations = "VAR_CONFIG" + instance_specific_init + ";" + instance_specific_init + ";" + "END_VAR"
instance_specific_init = resource_name + "." + program_name + "." + ZeroOrMore(fb_name + ".") + ((variable_name + Optional(location) + ":" + located_var_spec_init) | (fb_name + ":" + function_block_type_name + ":=" + structure_initialization))

il_assign_operator = variable_name + ":="
il_assign_out_operator = Optional("NOT") + variable_name + "=>"
il_call_operator = "CAL" | "CALC" | "CALCN"
il_return_operator = "RET" | "RETC" | "RETCN"
il_jump_operator = "JMP" | "JMPC" | "JMPCN"
EOL = "\n"

il_simple_instruction = Forward()
il_expr_operator = Keyword("AND") | Keyword("&") | Keyword("OR") | Keyword("XOR") | Keyword("ANDN") | Keyword("\&N") | Keyword("ORN") | Keyword("XORN") | Keyword("ADD") | Keyword("SUB") | Keyword("MUL") | Keyword("DIV") | Keyword("MOD") | Keyword("GT") | Keyword("GE") | Keyword("EQ")| Keyword("LT") | Keyword("LE") | Keyword("NE")
il_simple_operator = Keyword("LD") | Keyword("LDN") | Keyword("ST") | Keyword("STN") | Keyword("NOT") | Keyword("S") | Keyword("R") | Keyword("S1") | Keyword("R1") | Keyword("CLK") | Keyword("CU") | Keyword("CD") | Keyword("PV") | Keyword("IN") | Keyword("PT") | il_expr_operator
il_operand = constant | variable | enumerated_value
il_operand_list = il_operand + ZeroOrMore("," + il_operand)
il_simple_operation = ( il_simple_operator + Optional(il_operand) ) | ( function_name + Optional(il_operand_list) )
label = identifier
simple_instr_list = il_simple_instruction + ZeroOrMore(il_simple_instruction)
il_expression = il_expr_operator + "(" + Optional(il_operand) +  EOL + ZeroOrMore(EOL) + Optional(simple_instr_list) + ")"
il_param_assignment = il_assign_operator + ( il_operand | ("(" + EOL + ZeroOrMore(EOL) + simple_instr_list + ")" ) )
il_param_out_assignment = il_assign_out_operator + variable
il_param_instruction = (il_param_assignment | il_param_out_assignment) + "," + EOL + ZeroOrMore(EOL)
il_param_last_instruction = ( il_param_assignment | il_param_out_assignment ) + EOL + ZeroOrMore(EOL)
il_param_list = ZeroOrMore(il_param_instruction) + il_param_last_instruction
il_formal_funct_call = function_name + "(" + EOL + ZeroOrMore(EOL) + Optional(il_param_list) + ")"
il_simple_instruction << ((il_simple_operation | il_expression | il_formal_funct_call) + EOL + ZeroOrMore(EOL))
il_jump_operation = il_jump_operator + label
il_fb_call = il_call_operator + fb_name + Optional("(" + (EOL + ZeroOrMore(EOL) + Optional( il_param_list )) | Optional(il_operand_list) + ")")
il_instruction = Optional(label +":") + Optional(il_simple_operation | il_expression | il_jump_operation | il_fb_call | il_formal_funct_call | il_return_operator) + EOL + ZeroOrMore(EOL)
instruction_list = il_instruction + ZeroOrMore(il_instruction)

var2_init_decl = var1_init_decl | array_var_init_decl | structured_var_init_decl | string_var_declaration
function_body = instruction_list | statement_list
function_var_decls = "VAR" + Optional("CONSTANT") + var2_init_decl + ";" + ZeroOrMore(var2_init_decl + ";") + "END_VAR"
derived_function_name = identifier
io_var_declarations = input_declarations | output_declarations | input_output_declarations
function_declaration = "FUNCTION" + derived_function_name + ":" + (elementary_type_name | derived_type_name) + ZeroOrMore(io_var_declarations | function_var_decls ) + function_body + "END_FUNCTION"
program_configuration = "PROGRAM" + Optional(Keyword("RETAIN") | Keyword("NON_RETAIN")) + program_name + Optional("WITH" + task_name) + ":" + program_type_name + Optional("(" + prog_conf_elements + ")")

parser = function_declaration | program_configuration
