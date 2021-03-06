from src.ast_builder import ASTBuilder
from src.vector_generation import create_similarity_vector, create_occurrence_list

def test_process(text):
    ast_builder = ASTBuilder()
    tokens = ast_builder.parse(text)
    print("Similarity Vector: {}".format(create_similarity_vector(create_occurrence_list(tokens), create_occurrence_list(tokens))))

text = """
PROGRAM main
VAR_INPUT
i : INT;
MIN_TIME_MS :	TIME := t#1s; 
END_VAR
foo(x.y.z);
foo(x.y.z());
i.j.k:=x.y.z[v+1];
Swap_Byte2 := DWORD#16#FF00FF00;
END_PROGRAM"""

test_process(text)

text = """
PROGRAM main
VAR_INPUT
i : INT;
END_VAR
i.j.k:=x.y[4];
END_PROGRAM"""

test_process(text)


##############

text = """
PROGRAM main
VAR_INPUT
i : INT;
END_VAR
x.y := 0;
u.v := 3;
END_PROGRAM"""

test_process(text)

##############

text = """
PROGRAM main
VAR_INPUT
i : INT;
S1 :	BYTE := 2#1111_1111;
END_VAR
i := 4;
REPEAT
i := i + 1;
UNTIL i < j+4
END_REPEAT;
END_PROGRAM"""

test_process(text)

##############

text = """
PROGRAM main
FOR i := 0 TO 10 DO
avg := avg[3].x + 4;
END_FOR;

FOR i := func(3) TO 10 DO
avg := avg[3].x + 4;
EXIT;
END_FOR;

END_PROGRAM
"""
test_process(text)

##############

text = """
PROGRAM main
VAR_INPUT
i : INT;
END_VAR
avg := 0;
i := 0;
WHILE (i < 5) DO
avg := avg + f[i];
i := i + 1;
END_WHILE;
avg := avg / 5;
END_PROGRAM"""

test_process(text)

##############

text = """
PROGRAM main
VAR_INPUT
i : INT;
END_VAR
i := 3 + f[5];
END_PROGRAM"""

test_process(text)

##############

text = """
PROGRAM main
VAR_INPUT
i : INT;
END_VAR
IF (a = 1) THEN
i := 3;
END_IF;
END_PROGRAM"""

test_process(text)

##############

text = """
PROGRAM main
VAR_INPUT
i : INT;
a : INT;
b : BOOL;
END_VAR
IF NOT init THEN
	init := TRUE;
	last_check := tx - t#100ms;
END_IF;
x := _BYTE_TO_INT(scene AND BYTE#2#0000_1111);
END_PROGRAM"""

test_process(text)

##############

text = """
PROGRAM main
VAR_INPUT
i : INT;
a : INT;
b : BOOL;
END_VAR
IF (a) THEN
i := 3;
END_IF;
END_PROGRAM"""

test_process(text)

##############

text = """
PROGRAM main
VAR_INPUT
i : INT;
END_VAR
IF (a = 1 AND b = 3 OR c = 5) THEN
i := 3;
END_IF;
END_PROGRAM"""

test_process(text)

##############

text = """
PROGRAM main
VAR_INPUT
i : INT;
END_VAR
IF (a = 1) THEN
   i := 3;
ELSE
   x := 0;
END_IF;
END_PROGRAM"""

test_process(text)

##############

text = """
PROGRAM main
VAR_INPUT
i : INT;
END_VAR
IF (a = 1) THEN
    x := 1;
ELSIF (b = 1) THEN
    y := 1;
ELSE
    x := 0;
    y := 0;
    z := 0;
END_IF;
END_PROGRAM"""

test_process(text)

##############

text = """
PROGRAM main
VAR_INPUT
i : INT;
END_VAR
IF (a = 1) THEN
    x := 1;
ELSIF (b = 1 AND t = 1) THEN
    y := 1;
    IF (000/02 = 0) THEN
        z := 1;
    END_IF;
ELSE
    x := 0;
    y := 0;
    z := 0;
END_IF;
END_PROGRAM"""

##############
text = """
PROGRAM main
VAR_INPUT
i : INT;
END_VAR

CASE state OF
0: IF (green_EW)THEN
     state :=1;
   END_IF;
1: IF (yellow_EW) THEN
     state :=2;
   END_IF;
2: IF (green_NS) THEN
     state :=3;
   END_IF;
END_CASE;
END_PROGRAM"""

test_process(text)

##############
text = """
PROGRAM main
VAR_INPUT
i : INT;
END_VAR

CASE state OF
1..7:	x := 3;
END_CASE;
END_PROGRAM"""

test_process(text)

##############
text = """
PROGRAM main
VAR_INPUT
i : INT;
END_VAR

CASE state OF
0: IF (green_EW)THEN
     state :=1;
   END_IF;
1: IF (yellow_EW) THEN
     state :=2;
   END_IF;
2: IF (green_NS) THEN
     state :=3;
   END_IF;
END_CASE;
END_PROGRAM"""

test_process(text)

##############

text = """
PROGRAM main
VAR_INPUT
i : INT;
END_VAR
x := foo();
END_PROGRAM"""

test_process(text)

##############

text = """
PROGRAM main
VAR_INPUT
i : INT;
END_VAR
x := foo(3);
x := foo(3, i);
END_PROGRAM"""

test_process(text)

##############

text = """
PROGRAM main
VAR_INPUT
i : INT;
END_VAR
ramp(OUT := 3);
ramp(OUT := 4, RUN := 1);
END_PROGRAM"""

test_process(text)

##############

text = """
PROGRAM main
VAR_INPUT
i : INT;
END_VAR
(* adjust position if end switch is active *)
IF SWITCH_AVAIL AND END_POS THEN
	POS := SEL_BYTE(POS > BYTE#127, BYTE#0, BYTE#255);
	next_cal := tx + T_CAL;
END_IF;

END_PROGRAM"""

test_process(text)

##############

text = """
PROGRAM main
VAR_INPUT
i : INT;
END_VAR
(* adjust position if end switch is active *)
IF SWITCH_AVAIL AND END_POS THEN
	POS := SEL_BYTE(X := POS > BYTE#127, BYTE#0, BYTE#255);
	next_cal := tx + T_CAL;
END_IF;

END_PROGRAM"""

test_process(text)

##############

text = """
PROGRAM main
VAR_INPUT
i : INT;
END_VAR
(* adjust position if end switch is active *)
IF SWITCH_AVAIL AND END_POS THEN
	POS := SEL_BYTE(X := POS + BYTE#127 * 4, BYTE#0, BYTE#255+7);
	next_cal := tx + T_CAL;
END_IF;

END_PROGRAM"""

test_process(text)

##############

text = """
PROGRAM main
VAR_INPUT
i : INT;
END_VAR
(* adjust position if end switch is active *)
IF DINT_TO_TIME(ABS(TIME_TO_DINT(ramp.TR) - TIME_TO_DINT(ramp.TF)) * DINT#10) > T_RUN THEN error := TRUE; END_IF;

END_PROGRAM"""

test_process(text)

##############

text = """
PROGRAM main
VAR_INPUT
i : INT;
END_VAR
(* adjust position if end switch is active *)
	IF (self_act_cycle > T#0s) AND (tx >= 5) THEN
	END_IF;
END_PROGRAM"""

test_process(text)

##############

text = """
PROGRAM main
VAR_INPUT
i : INT;
END_VAR
(* adjust position if end switch is active *)
IF (status > BYTE#0 AND status < BYTE#100) THEN 
  RETURN;
END_IF;
END_PROGRAM"""

test_process(text)

##############

text = """
PROGRAM main
VAR_INPUT
i : INT;
END_VAR
(* adjust position if end switch is active *)
timer1(in := flame AND in AND motor AND coil1 AND NOT coil2, SECONDS := runtime1, CYCLES := cycles);
timer2(in := flame AND in AND motor AND coil1 AND coil2, SECONDS := runtime2, CYCLES := cycles2);
END_PROGRAM"""

test_process(text)

##############

text = """
PROGRAM main
VAR_INPUT
i : INT;
END_VAR
(* adjust position if end switch is active *)
timer2(in := flame AND in AND motor AND coil1 AND coil2, SECONDS := runtime2, CYCLES := cycles2);
END_PROGRAM"""

test_process(text)

##############

text = """
FUNCTION WATER_DENSITY:REAL
WATER_DENSITY := (999.83952 + 16.952577*T + -7.9905127E-3*T2 + -4.6241757E-5*T2*T + 1.0584601E-7*T4 + -2.8103006E-10*T4*T) / (1.0 + 0.0168872*T);
END_FUNCTION"""

test_process(text)

##############

text = """
PROGRAM main
IF (tx - last) >= T2 THEN
	(* timeout for long pulse if second click did not occur or in stays high *)
	Q := FALSE;
END_IF;
END_PROGRAM"""

test_process(text)

##############

text = """
PROGRAM main
cmp:="ab";
cmp:='ab';
END_PROGRAM"""

test_process(text)

##############

text = """
PROGRAM main
SWIL := LW.Y; // [mm]
NOL := (SWP_1.FulRolLen - SWIL) * 0.5;
END_PROGRAM"""

test_process(text)

##############

text = """
PROGRAM main
VAR_INPUT
    X : ARRAY[0..3] OF BYTE; (* scan line inputs *)
    L : ARRAY[0..3] OF BYTE; (* scan line status *)
    _temp AT temp : ARRAY[0..7] OF BOOL;
    y2, y3, y4 : BOOL;
END_VAR
avg := 0;
i := 0;
END_PROGRAM"""

test_process(text)

##############

text = """
PROGRAM main
STRING_TO_URL.STR:="http://ipinfodb.com/ip_query.php?timezone=true&IP=";
END_PROGRAM"""

test_process(text)

##############

text = """
FUNCTION_BLOCK FILE_PATH_SPLIT
FOR b := 1 TO c DO

END_FOR;
END_FUNCTION_BLOCK
"""

test_process(text)
