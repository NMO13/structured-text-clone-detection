text = """
FUNCTION_BLOCK ACTUATOR_COIL

(*Group:Default*)


VAR_INPUT
	IN :	BOOL;
	SELF_ACT_CYCLE :	TIME := T#10d;
	SELF_ACT_TIME :	TIME := T#1s;
END_VAR


VAR_OUTPUT
	OUT :	BOOL;
	STATUS :	BYTE;
END_VAR


VAR
	last :	UDINT;
	init :	BOOL;
	tx :	UDINT;
	now :	UDINT;
	T_PLC_MS :	T_PLC_MS;
END_VAR


(*@KEY@: WORKSHEET
NAME: ACTUATOR_COIL
IEC_LANGUAGE: ST
*)
(* read system time *)
T_PLC_MS();
now := T_PLC_MS.T_PLC_MS;

(* initialize for first cycle *)
IF NOT init THEN
	last := now;
	init := TRUE;
ELSIF IN THEN
	OUT := TRUE;
	STATUS := BYTE#101; (* activated by input *)
	LAST := now;
ELSE
	OUT := FALSE;
	STATUS := BYTE#100; (* disabled *)
	(* now we need to check for self activation *)
	tx := now - last;
	IF (self_act_cycle > T#0s) AND (tx >= TIME_TO_UDINT(self_act_cycle)) THEN
		OUT := TRUE;
		STATUS := BYTE#102; (* auto activation *)
		IF tx >= TIME_TO_UDINT(self_act_cycle + self_act_time) THEN
			last := now;
			OUT := FALSE;
			STATUS := BYTE#100; (* idle *)
		END_IF;
	END_IF;
END_IF;

(*
revision history:

hm		1. jun. 2008 	rev 1.0
	original version

*)
(*@KEY@: END_WORKSHEET *)
END_FUNCTION_BLOCK
"""

from src.ast_builder import ASTBuilder
creator = ASTBuilder()
creator.parse(text)