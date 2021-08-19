text = """
(*@KEY@:END_DESCRIPTION*)
FUNCTION_BLOCK ACTUATOR_3P

(*Group:Default*)


VAR_INPUT
	IN :	BYTE;
	TEST :	BOOL;
	ARE :	BOOL := TRUE;
	END_POS :	BOOL;
	T_RUN :	TIME := T#60s;
	T_EXT :	TIME := T#10s;
	T_CAL :	TIME := T#600s;
	T_DIAG :	TIME := T#10d;
	SWITCH_AVAIL :	BOOL;
END_VAR


VAR_OUTPUT
	OUT1 :	BOOL;
	OUT2 :	BOOL;
	POS :	BYTE;
	ERROR :	BOOL;
	STATUS :	BYTE;
END_VAR


VAR_IN_OUT
	ARX :	BOOL;
END_VAR


VAR
	tx :	TIME;
	ramp :	_RMP_NEXT;
	next_cal :	TIME;
	next_diag :	TIME;
	last :	TIME;
	start :	TIME;
	T_PLC_MS :	T_PLC_MS;
END_VAR


(*@KEY@: WORKSHEET
NAME: ACTUATOR_3P
IEC_LANGUAGE: ST
*)
(* setup *)
T_PLC_MS();
tx := UDINT_TO_TIME(T_PLC_MS.T_PLC_MS);

(* check test input *)
IF TEST THEN
	status := BYTE#103;
	start := tx;
	ARX := TRUE;
END_IF;

CASE _BYTE_TO_INT(status) OF
	0:	(* power on setup *)
		IF ARE AND NOT ARX THEN
			status := BYTE#103;
			start := tx;
			ARX := TRUE;
		END_IF;

	100:	(* normal operation *)
		(* check for auto diagnostics *)
		IF T_DIAG > T#0s AND tx > next_diag AND ARE AND NOT ARX THEN
				status := BYTE#103;
				start := tx;
				ARX := TRUE;

		(* check for auto calibration *)
		ELSIF T_CAL > T#0s AND tx > next_cal AND ARE AND NOT ARX THEN
			IF pos > BYTE#127 THEN
				OUT1 := TRUE;
				OUT2 := FALSE;
				ramp.IN := BYTE#255;
				ARX := TRUE;
			ELSE
				OUT1 := FALSE;
				OUT2 := TRUE;
				ramp.IN := BYTE#0;
				ARX := TRUE;
			END_IF;
			status := BYTE#101;
			start := tx;
		ELSE
			(* increment next_cal if not active *)
			IF NOT(OUT1 OR OUT2) THEN next_cal := next_cal + (tx-last); END_IF;
			(* set ramp generator to IN *)
			ramp.IN := IN;
		END_IF;

	101:	(* calibrate *)
		IF tx - start < T_EXT THEN
			next_cal := tx + T_CAL;
		ELSIF SWITCH_AVAIL AND END_POS THEN
			STATUS := BYTE#100;
			ARX := FALSE;
		ELSIF tx - start > T_EXT + T_RUN THEN
			ERROR := SWITCH_AVAIL;
			ARX := FALSE;
		END_IF;

	103:	(* diagnostics up*)
		(* run up for T_ext *)
		IF tx - start < T_EXT THEN
			ERROR := FALSE;
			ramp.TR := T_RUN;
			ramp.TF := T_RUN;
			OUT1 := TRUE;
			OUT2 := FALSE;
			ramp.IN := BYTE#255;
		ELSIF SWITCH_AVAIL AND END_POS THEN
			ramp.TR := tx - start;
			STATUS := BYTE#104;
		ELSIF tx - start > T_EXT + T_RUN THEN
			ERROR := SWITCH_AVAIL;
			STATUS := BYTE#104;
			start := tx;
		END_IF;

	104:	(* diagnostics dn*)
		IF tx - start < T_ext THEN
			OUT1 := FALSE;
			OUT2 := TRUE;
			ramp.IN := BYTE#0;
			next_diag := tx + T_DIAG;
		ELSIF SWITCH_AVAIL AND END_POS THEN
			ramp.TR := tx - start;
			(* check if runtimes differ by more than 10% *)
			IF DINT_TO_TIME(ABS(TIME_TO_DINT(ramp.TR) - TIME_TO_DINT(ramp.TF)) * DINT#10) > T_RUN THEN error := TRUE; END_IF;
			STATUS := BYTE#100;
			ARX := FALSE;
			next_cal := tx + T_CAL;
		ELSIF tx - start > T_EXT + T_RUN THEN
			IF SWITCH_AVAIL THEN ERROR := TRUE; END_IF;
			STATUS := BYTE#100;
			ARX := FALSE;
			next_CAL := tx + T_CAL;
		END_IF;
END_CASE;

(* internal flap simulation and output activation *)
ramp(OUT := POS);
POS := ramp.OUT;
IF STATUS = BYTE#100 THEN
	OUT1 := ramp.UP;
	OUT2 := ramp.DN;
END_IF;

(* adjust position if end switch is active *)
IF SWITCH_AVAIL AND END_POS THEN
	POS := SEL_BYTE(POS > BYTE#127, BYTE#0, BYTE#255);
	next_cal := tx + T_CAL;
END_IF;

(* set last to tx for next cycle *)
last := tx;



(* revision history

hm	19. oct 2006	rev 1.1
	added security checks for end_switch to avoid overrun of the end_switch, hans

hm	23. jan 2007	rev 1.2
	deleted unused variables force_on and force_off

hm	15. sep 2007	 rev 1.3
	replaced Time() with T_PLC_MS for compatibility and performance reasons

hm	28. jan 2010	rev 2.0
	new code and new features

*)
(*@KEY@: END_WORKSHEET *)
END_FUNCTION_BLOCK
"""

from src.ast_builder import ASTBuilder
creator = ASTBuilder()
creator.parse(text)