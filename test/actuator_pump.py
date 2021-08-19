text = """
FUNCTION_BLOCK ACTUATOR_PUMP

(*Group:Default*)


VAR_INPUT
	IN :	BOOL;
	MANUAL :	BOOL;
	RST :	BOOL := FALSE;
	MIN_ONTIME :	TIME := T#10s;
	MIN_OFFTIME :	TIME := T#10s;
	RUN_EVERY :	TIME := T#10000m;
END_VAR


VAR_OUTPUT
	PUMP :	BOOL;
	RUNTIME :	UDINT;
	CYCLES :	UDINT;
END_VAR


VAR
	tx :	TIME;
	last_change :	TIME;
	meter :	ontime;
	old_man :	BOOL;
	init :	BOOL;
	T_PLC_MS :	T_PLC_MS;
END_VAR


(*@KEY@: WORKSHEET
NAME: ACTUATOR_PUMP
IEC_LANGUAGE: ST
*)
T_PLC_MS();
tx:= UDINT_TO_TIME(T_PLC_MS.T_PLC_MS);

IF NOT init THEN
	init := TRUE;
	last_change := tx;
ELSIF rst THEN
	rst := FALSE;
	runtime := UDINT#0;
	cycles := UDINT#0;
ELSIF manual AND NOT pump AND NOT old_man THEN
	last_change := tx;
	pump := TRUE;
ELSIF NOT manual AND old_man AND pump AND NOT in THEN
	last_change := tx;
	pump := FALSE;
ELSIF in AND NOT pump AND tx - last_change >= min_offtime THEN
	last_change := tx;
	pump := TRUE;
ELSIF pump AND NOT in AND NOT manual AND tx - last_change >= min_ontime THEN
	last_change := tx;
	pump := FALSE;
ELSIF NOT pump AND (tx - last_change >= run_every) AND (run_every > T#0s) THEN
	last_change := tx;
	pump := TRUE;
END_IF;

meter(in := pump, SECONDS := runtime, CYCLES := cycles);
cycles := meter.CYCLES;
runtime := meter.SECONDS;

old_man := manual;

(*
hm	27.12.2006		rev 1.1
	fixed a failure while the pump would run for tmin after startup.

hm	15.9.2007		rev 1.2
	replaced Time() with T_PLC_MS for compatibility and performance reasons

hm	13. oct. 2008	rev 1.3
	auto activation can now be disabled when run_every = t#0s

hm	21. oct. 2008	rev 1.4
	changed to use ontime rev 2.0

*)
(*@KEY@: END_WORKSHEET *)
END_FUNCTION_BLOCK
"""

from src.ast_builder import ASTBuilder
creator = ASTBuilder()
creator.parse(text)