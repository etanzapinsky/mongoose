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
	print syntax_error_in_input+"program order must be: [agents] environment terminate analysis" 

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

