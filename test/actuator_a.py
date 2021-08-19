text = """
FUNCTION_BLOCK ACTUATOR_A

(*Group:Default*)


VAR_INPUT
	I1 :	BYTE;
	IS :	BOOL;
	I2 :	BYTE;
	RV :	BOOL;
	DX :	BOOL;
	RUNTIME :	TIME;
	SELF_ACT_TIME :	TIME;
	OUT_MIN :	DWORD;
	OUT_MAX :	DWORD;
END_VAR


VAR_OUTPUT
	Y :	DWORD;
END_VAR


VAR
	timer :	CYCLE_4;
	dx_edge :	BOOL;
END_VAR


timer(T0 := RUNTIME, T1 := RUNTIME, T3 := SELF_ACT_TIME, sl := DX AND NOT dx_edge, sx := 0, S0 := SELF_ACT_TIME > t#0s);
dx_edge := dx;





END_FUNCTION_BLOCK
"""

from src.ast_builder import ASTBuilder
creator = ASTBuilder()
creator.parse(text)