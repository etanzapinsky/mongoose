syntax_error_in_input = "Syntax error in input: " 

"""
def p_no_environment_error(p):
	''' program : stat_list_wrapper agent_list_wrapper stat_list_wrapper error stat_list_wrapper terminate_block stat_list_wrapper analysis stat_list_wrapper
	'''
	print "Syntax error in input: missing environment block!"

def p_no_terminate_error(p):
    ''' program : stat_list_wrapper agent_list_wrapper stat_list_wrapper environment stat_list_wrapper error stat_list_wrapper analysis stat_list_wrapper
    '''
    print "Syntax error in input: missing terminate block!"

def p_no_analysis_error(p):
	''' program : stat_list_wrapper agent_list_wrapper stat_list_wrapper environment stat_list_wrapper terminate_block stat_list_wrapper error stat_list_wrapper
	'''
	print "Syntax error in input: missing analysis block!"
"""

def p_program_error(p):
	''' program : error 
	'''
	print syntax_error_in_input+"Program contains an error. Block order must be: [agents] environment terminate analysis" 

def p_environment_error(p):
    ''' environment : ENVIRONMENT error 
    '''
    print syntax_error_in_input+"ENVIRONMENT block contains an error at line "+str(p.lineno(2))+". Proper format: ENVIRONMENT '{' statement_list populate/action statement_list action/populate statement_list  '}'"

def p_populate_error(p):
    ''' populate : POPULATE error
    '''
    print syntax_error_in_input+"POPULATE block contains an error at line "+str(p.lineno(2))+". Proper format: POPULATE '{' statement_list '}'"

def p_action_error(p):
    ''' action : ACTION error
    '''
    print syntax_error_in_input+"ACTION block contains an error at line "+str(p.lineno(2))+". Proper format: ACTION '{' statement_list '}'"

def p_terminate_error(p):
    ''' terminate_block : TERMINATE error
    '''
    print syntax_error_in_input+"TERMINATE block contains an error at line "+str(p.lineno(2))+". Proper format: TERMINATE '{' invariant_list '}'"

def p_analysis_error(p):
    ''' analysis : ANALYSIS error
    '''
    print syntax_error_in_input+"ANALYSIS block contains an error at line "+str(p.lineno(2))+". Proper format: ANALYSIS '{' statement_list '}'"

def p_agent_error(p):
	''' agent : AGENT NAME '{' error '}'
	'''
	print syntax_error_in_input+"agent requires create method, destroy block and action terminate_block"

def p_agent_cda_left_brace_error(p):
    ''' agent : AGENT NAME error stat_list_wrapper create stat_list_wrapper destroy stat_list_wrapper action stat_list_wrapper '}'
    '''
    print syntax_error_in_input+"missing left brace in agent definition at line "+str(p.lineno(3))

def p_agent_cad_left_brace_error(p):
    ''' agent : AGENT NAME error stat_list_wrapper create stat_list_wrapper action stat_list_wrapper destroy stat_list_wrapper '}'
    '''
    print syntax_error_in_input+"missing left brace in agent definition at line "+str(p.lineno(3))

def p_agent_dca_left_brace_error(p):
    ''' agent : AGENT NAME error stat_list_wrapper destroy stat_list_wrapper create stat_list_wrapper action stat_list_wrapper '}'
    '''
    print syntax_error_in_input+"missing left brace in agent definition at line "+str(p.lineno(3))

def p_agent_dac_left_brace_error(p):
    ''' agent : AGENT NAME error stat_list_wrapper destroy stat_list_wrapper action stat_list_wrapper create stat_list_wrapper '}'
    '''
    print syntax_error_in_input+"missing left brace in agent definition at line "+str(p.lineno(3))

def p_agent_adc_left_brace_error(p):
    ''' agent : AGENT NAME error stat_list_wrapper action stat_list_wrapper destroy stat_list_wrapper create stat_list_wrapper '}'
    '''
    print syntax_error_in_input+"missing left brace in agent definition at line "+str(p.lineno(3))

def p_agent_acd_left_brace_error(p):
    ''' agent : AGENT NAME error stat_list_wrapper action stat_list_wrapper create stat_list_wrapper destroy stat_list_wrapper '}'
    '''
    print syntax_error_in_input+"missing left brace in agent definition at line "+str(p.lineno(3))

def p_agent_cda_right_brace_error(p):
    ''' agent : AGENT NAME '{' stat_list_wrapper create stat_list_wrapper destroy stat_list_wrapper action stat_list_wrapper error
    '''
    print syntax_error_in_input+"missing right brace in agent definition at line "+str(p.lineno(11))

def p_agent_cad_right_brace_error(p):
    ''' agent : AGENT NAME '{' stat_list_wrapper create stat_list_wrapper action stat_list_wrapper destroy stat_list_wrapper error
    '''
    print syntax_error_in_input+"missing right brace in agent definition at line "+str(p.lineno(11))

def p_agent_dca_right_brace_error(p):
    ''' agent : AGENT NAME '{' stat_list_wrapper destroy stat_list_wrapper create stat_list_wrapper action stat_list_wrapper error
    '''
    print syntax_error_in_input+"missing right brace in agent definition at line "+str(p.lineno(11))

def p_agent_dac_right_brace_error(p):
    ''' agent : AGENT NAME '{' stat_list_wrapper destroy stat_list_wrapper action stat_list_wrapper create stat_list_wrapper error
    '''
    print syntax_error_in_input+"missing right brace in agent definition at line "+str(p.lineno(11))

def p_agent_adc_right_brace_error(p):
    ''' agent : AGENT NAME '{' stat_list_wrapper action stat_list_wrapper destroy stat_list_wrapper create stat_list_wrapper error
    '''
    print syntax_error_in_input+"missing right brace in agent definition at line "+str(p.lineno(11))

def p_agent_acd_right_brace_error(p):
    ''' agent : AGENT NAME '{' stat_list_wrapper action stat_list_wrapper create stat_list_wrapper destroy stat_list_wrapper error
    '''
    print syntax_error_in_input+"missing right brace in agent definition at line "+str(p.lineno(11))

def p_create_error(p):
    ''' create : CREATE error
    '''
    print syntax_error_in_input+"CREATE function error at lineno "+str(p.lineno(2))+". create format: CREATE '(' formal_param_list ')' '{' statement_list '}'"

def p_destroy_error(p):
    ''' destroy : DESTROY error
    '''
    print syntax_error_in_input+"DESTROY block contains an error at line "+str(p.lineno(2))+". Proper format: DESTROY '{' statement_list '}'"

def p_while_error(p):
    ''' stat : WHILE error
    '''
    print syntax_error_in_input+"while loop error at line "+str(p.lineno(2))+". while format: WHILE '(' expr ')' '{' statement_list '}'"

def p_if_error(p):
    ''' stat : IF error   
    '''
    print syntax_error_in_input+"if statement error at line "+str(p.lineno(2))+". if format: IF '(' expr ')' '{' statement_list '}' [elifs] [else]"

def p_pif_error(p):
    ''' stat : PIF error
    '''
    print syntax_error_in_input+"pif statement error at line "+str(p.lineno(2))+". pif format: PIF '(' float ')' '{' statement_list '}' [pelifs] [pelse]"

def p_repeat_error(p):
    ''' stat : REPEAT error 
    '''
    print syntax_error_in_input+"repeat statement error at line "+str(p.lineno(2))+". repeat format: REPEAT '(' int ')' '{' statement_list '}'"

def p_possible_function_def_error(p):
    ''' stat : list_type NAME error 
    '''
    print syntax_error_in_input+"error at line "+str(p.lineno(3))+". See "+p[2] 

def p_possible_none_function_def_error(p):
    ''' stat : NONE NAME error 
    '''
    print syntax_error_in_input+"error at line "+str(p.lineno(3))+". See "+p[2] 

def p_function_call_error(p):
    ''' function_call : NAME '(' error ')'
    '''
    print syntax_error_in_input+"function call error at line "+str(p.lineno(3))+". function call format: NAME '{' actual_param_list '}'. See "+p[1] 

def p_weighted_val_stat_error(p):
    ''' weighted_val_stat : error
    '''
    print syntax_error_in_input+"weighted value error at line "+str(p.lineno(1))+". weighted value format: '(' (integer:value '|')* integer:value ')'" 















