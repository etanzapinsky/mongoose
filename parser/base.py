import ply.yacc as yacc
from lexer import lexer
from tree import Node, Function
import vtypes as v
import re
from backend import backend
# hack to get the tokens since they are a global variable in the lexer object
tokens = lexer.tokens

#class Node:    def __init__(self, vtype, inh_value=None, syn_value=None, children=[]):

precedence = (
    ('nonassoc', '='), #(right if we allow)
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'EQ', 'NEQ'),
    ('nonassoc', '<', '>', 'LEQ', 'GEQ'),
    ('left', '+', '-'),
    ('left', '*', '/', '%'),
    ('right', '^'),
    ('right', 'NOT', 'UMINUS'),           
)

start =  'program'


def p_program(p):
    ''' program : stat_list_wrapper agent_list_wrapper stat_list_wrapper environment stat_list_wrapper terminate_block stat_list_wrapper analysis stat_list_wrapper
    '''
    p[0] = Node(vtype=v.PROGRAM, children=[p[2],p[4],p[6],p[8],p[1],p[3],p[5],p[7],p[9]])#order: agent, environment, terminate, analysis then all other statements in order

#def p_program_error(p):
#    ''' program : stat_list_wrapper error stat_list_wrapper 
#    '''
#    print "Missing environment block!"

#######################
## AGENT DEFINITIONS ##
#######################

def p_agent_list_wrapper(p):
    ''' agent_list_wrapper : NEWLINE agent_list NEWLINE
                         | NEWLINE agent_list
                         | agent_list NEWLINE
                         | agent_list 
    '''
    if len(p) == 3:
        p[0] = p[2]
    elif len(p) == 2:
        if type(p[1]) is str:  
            p[0] = p[2]
        else:
            p[0] = p[1]
    else: #len(p) == 4
        p[0] = p[2]

#TODO: agentements require newline at end !!!!

def p_agent_opt(p):
    ''' agent_opt : agent                                                                                              
    '''
    p[0] = p[1]

def p_agent_opt_epsilon(p):
    ''' agent_opt : epsilon  
    '''
    p[0] = None

def p_agent_listn(p):
    ''' agent_list : agent_n agent_opt
    '''
    p[0] = Node(vtype=v.AGENT_LIST, children=[p[1], p[2]])

# TODO: dont require last newline                                                                               
def p_agentn(p):
    ''' agent_n : agent NEWLINE agent_n                                                                                      
              | epsilon                                                                                             
    '''
    if len(p) == 4:
        p[0] = Node(vtype=v.AGENT_WRAPPER, children=[p[1],p[3]])
    else:
        p[0] = None

def p_agent_1_cda(p):
    ''' agent : AGENT NAME '{' stat_list_wrapper create stat_list_wrapper destroy stat_list_wrapper action stat_list_wrapper '}'
    '''
    p[0] = Node(vtype=v.AGENT, symbol=p[2], children=[p[5],p[7],p[9],p[4],p[6],p[8],p[10]])#create, destroy, action, then all statements in order
    backend.scopes[-1][p[2]] = p[0]

def p_agent_2_cad(p):
    ''' agent : AGENT NAME '{' stat_list_wrapper create stat_list_wrapper action stat_list_wrapper destroy stat_list_wrapper '}'
    '''
    p[0] = Node(vtype=v.AGENT, symbol=p[2], children=[p[5],p[9],p[7],p[4],p[6],p[8],p[10]])
    backend.scopes[-1][p[2]] = p[0]

def p_agent_3_dca(p):
    ''' agent : AGENT NAME '{' stat_list_wrapper destroy stat_list_wrapper create stat_list_wrapper action stat_list_wrapper '}'
    '''
    p[0] = Node(vtype=v.AGENT, symbol=p[2], children=[p[7],p[5],p[9],p[4],p[6],p[8],p[10]])
    backend.scopes[-1][p[2]] = p[0]

def p_agent_4_dac(p):
    ''' agent : AGENT NAME '{' stat_list_wrapper destroy stat_list_wrapper action stat_list_wrapper create stat_list_wrapper '}'
    '''
    p[0] = Node(vtype=v.AGENT, symbol=p[2], children=[p[7],p[9],p[5],p[4],p[6],p[8],p[10]])
    backend.scopes[-1][p[2]] = p[0]

def p_agent_5_adc(p):
    ''' agent : AGENT NAME '{' stat_list_wrapper action stat_list_wrapper destroy stat_list_wrapper create stat_list_wrapper '}'
    '''
    p[0] = Node(vtype=v.AGENT, symbol=p[2], children=[p[9],p[7],p[5],p[4],p[6],p[8],p[10]])
    backend.scopes[-1][p[2]] = p[0]

def p_agent_6_acd(p):
    ''' agent : AGENT NAME '{' stat_list_wrapper action stat_list_wrapper create stat_list_wrapper destroy stat_list_wrapper '}'
    '''
    p[0] = Node(vtype=v.AGENT, symbol=p[2], children=[p[9],p[5],p[7],p[4],p[6],p[8],p[10]])
    backend.scopes[-1][p[2]] = p[0]

def p_create(p):
    ''' create : CREATE '(' formal_param_list ')' '{' stat_list_wrapper '}'
    '''
    symbol = p[1]
    if p[3] is not None:
        parameter_pairs = p[3].inh_value
        parameter_pairs = parameter_pairs[:-1]
        parameter_pairs = parameter_pairs.split(",")
        parameter_pairs = [tuple(s.split(" ")) for s in parameter_pairs]
    else:
        parameter_pairs = []
    p[0] = Function(symbol=symbol, statements=p[6],
                              return_type='agent', #use agent as placeholder for agent's name, which can't be known here
                              parameter_pairs=parameter_pairs)
    backend.scopes[-1][symbol] = p[0]

def p_destroy(p):
    ''' destroy : DESTROY '{' stat_list_wrapper '}'
    '''
    p[0] = Node(vtype=v.DESTROY, children=[p[3]])


#######################
## ENVIRONMENT BLOCK ##
#######################

def p_environment_1(p):
    ''' environment : ENVIRONMENT '{' stat_list_wrapper populate stat_list_wrapper action stat_list_wrapper  '}'
    '''
    p[0] = Node(vtype=v.ENVIRONMENT, children=[p[4],p[6],p[3],p[5],p[7]])#order: populate, action, then all surrounding statements

def p_environment_2(p):
    ''' environment : ENVIRONMENT '{' stat_list_wrapper action stat_list_wrapper populate stat_list_wrapper  '}'
    ''' 
    p[0] = Node(vtype=v.ENVIRONMENT, children=[p[6],p[4],p[3],p[5],p[7]])#order: populate, action, then all surrounding statements 

def p_populate(p):
    ''' populate : POPULATE '{' stat_list_wrapper '}'
    '''
    p[0] = Node(vtype=v.POPULATE, children=[p[3]])

def p_action(p):
    ''' action : ACTION '{' stat_list_wrapper '}'
    '''
    p[0] = Node(vtype=v.ACTION, children=[p[3]])

#####################
## TERMINATE BLOCK ##
#####################

def p_opt_frequency(p):
    ''' opt_frequency : VINTEGER ':'
                      | epsilon
    '''
    if len(p) == 3:
        p[0] = Node(vtype=v.INTEGER_VALUE, syn_value=p[1]) 
    else:
        p[0] = Node(vtype=v.INTEGER_VALUE, syn_value='1') #default frequency == 1

def p_terminate_block(p):
    ''' terminate_block : TERMINATE '{' invariant_list_wrapper '}'
    '''
    p[0] = p[3]

def p_invariant_list_wrapper(p):
    '''invariant_list_wrapper : NEWLINE invariant_list NEWLINE
                         | NEWLINE invariant_list
                         | invariant_list NEWLINE
                         | invariant_list 
    '''
    if len(p) == 3:
        p[0] = p[2]
    elif len(p) == 2:
        if type(p[1]) is str:  
            p[0] = p[2]
        else:
            p[0] = p[1]
    else: #len(p) == 4
        p[0] = p[2]

#TODO: invariantements require newline at end !!!!

def p_invariant_opt(p):
    ''' invariant_opt : invariant                                                                                              
    '''
    p[0] = p[1]

def p_invariant_opt_epsilon(p):
    ''' invariant_opt : epsilon  
    '''
    p[0] = None

def p_invariant_listn(p):
    '''invariant_list : invariant_n invariant_opt
    '''
    p[0] = Node(vtype=v.TERMINATE, children=[p[1], p[2]])

# TODO: dont require last newline                                                                               
def p_invariantn(p):
    '''invariant_n : invariant NEWLINE invariant_n                                                                                      
              | epsilon                                                                                             
    '''
    if len(p) == 4:
        p[0] = Node(vtype=v.INVARIANTS, children=[p[1],p[3]])
    else:
        p[0] = None

def p_invariant(p):
    ''' invariant : opt_frequency '(' expr ')' '{' stat_list_wrapper '}'
    '''
    p[0] = Node(vtype=v.INVARIANT_CLAUSE, syn_value=p[1].syn_value, children=[p[3],p[6]])   


####################
## ANALYSIS BLOCK ##
####################

def p_analysis_block(p):
    ''' analysis : ANALYSIS '{' stat_list_wrapper '}'
    '''
    p[0] = Node(vtype=v.ANALYSIS, children=[p[3]])

################
## STATEMENTS ##
################

def p_stat_list_wrapper(p):
    '''stat_list_wrapper : NEWLINE stat_list NEWLINE
                         | NEWLINE stat_list
                         | stat_list NEWLINE
                         | stat_list 
    '''
    if len(p) == 3:
        p[0] = p[2]
    elif len(p) == 2:
        if type(p[1]) is str:  
            p[0] = p[2]
        else:
            p[0] = p[1]
    else: #len(p) == 4
        p[0] = p[2]

#TODO: statements require newline at end !!!!

def p_stat_opt(p):
    ''' stat_opt : stat                                                                                              
    '''
    p[0] = p[1]

def p_stat_opt_epsilon(p):
    ''' stat_opt : epsilon  
    '''
    p[0] = None

def p_stat_listn(p):
    '''stat_list : stat_n stat_opt
    '''
    p[0] = Node(vtype=v.STATEMENT_LIST, children=[p[1], p[2]])

# TODO: dont require last newline                                                                               
def p_statn(p):
    '''stat_n : stat NEWLINE stat_n                                                                                      
              | epsilon                                                                                             
    '''
    if len(p) == 4:
        p[0] = Node(vtype=v.STATEMENT, children=[p[1],p[3]])
    else:
        p[0] = None

###############
## FUNCTIONS ##
###############

#TODO stat_list_wrapper causes problems , does not exlcude function def within function def or loops, etc.
#list_type changed from return_type
def p_function_def(p):
    ''' stat : list_type NAME '(' formal_param_list ')' '{' stat_list_wrapper '}'
    '''
    symbol = p[2]
    if p[4] is not None:
        parameter_pairs = p[4].inh_value
        parameter_pairs = parameter_pairs[:-1]
        parameter_pairs = parameter_pairs.split(",")
        parameter_pairs = [tuple(s.split(" ")) for s in parameter_pairs]
    else:
        parameter_pairs = []
    p[0] = Function(symbol=symbol, statements=p[7],
                              return_type=re.sub('\d+','',p[1].inh_value),
                              parameter_pairs=parameter_pairs)
    #if not backend.scopes[-1].has_key(symbol):
    backend.scopes[-1][symbol] = p[0]
    #else:
    #    print "Error: function "+symbol+" already defined"
    #    raise SyntaxError

def p_stat_function_call(p):
    ''' stat : function_call 
    '''
    p[0] = p[1]

#brack changed from empty_brack
def p_formal_param(p):
    ''' formal_param : type brack NAME
    '''
    p[0] = Node(vtype=v.FORMAL_PARAM, symbol=p[3], children=[p[1],p[2]], inh_value=p[1].syn_value+re.sub('\d+','',p[2].inh_value))

def p_formal_param_list(p):
    ''' formal_param_list : formal_param formal_param_comma
                          | epsilon
    '''  
    if len(p) == 3:
        p[0] = Node(vtype=v.FORMAL_PARAM_LIST, children=[p[1],p[2]], inh_value=p[1].inh_value+' '+p[1].symbol+','+(p[2].inh_value if p[2] != None else ''))
    else:
        p[0] = None

def p_formal_param_comma(p):
    ''' formal_param_comma : ',' formal_param_list
                           | epsilon
    '''     
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = None

def p_function_call(p):
    ''' function_call : NAME '(' actual_param_list ')'
    '''
    p[0] = Node(vtype=v.FUNCTION_CALL, symbol=p[1], children=[p[3]])

def p_actual_param(p):
    ''' actual_param : expr
    '''
    p[0] = p[1]

def p_actual_param_list(p):
    ''' actual_param_list : actual_param actual_param_comma
                          | epsilon
    '''  
    if len(p) == 3:
        p[0] = Node(vtype=v.ACTUAL_PARAM_LIST, children=[p[1],p[2]])
    else:
        p[0] = None

def p_actual_param_comma(p):
    ''' actual_param_comma : ',' actual_param_list
                           | epsilon
    '''     
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = None 

##################
## CONTROL FLOW ##
##################

#TODO: (fix:) cant have newline before {
def p_while(p):
    ''' stat : WHILE '(' expr ')' '{' stat_list_wrapper '}'
    '''
    p[0] = Node(vtype=v.WHILE, children=[p[3], p[6]])

#TODO: no newline allowed before elif/else, maybe fix this
def p_if(p):
    ''' stat : IF '(' expr ')' '{' stat_list_wrapper '}' opt_elifs opt_else  
    '''
    p[0] = Node(vtype=v.IF, children=[p[3],p[6],p[8],p[9]])

def p_opt_elifs(p):
    ''' opt_elifs : epsilon
                  | opt_elifs ELIF '(' expr ')' '{' stat_list_wrapper '}' 
    ''' 
    if len(p) == 9:
        p[0] = Node(vtype=v.ELIF, children=[p[1],p[4],p[7]])
    else: #len(p)==2
        p[0] = None

def p_opt_else(p):
    ''' opt_else : epsilon
                 | ELSE '{' stat_list_wrapper '}'
    '''
    if len(p) == 5:
        p[0] = Node(vtype=v.ELSE, children=[p[3]]) 
    else:
        p[0] = None

#VFLOAT is non-negative
def p_pif(p):
    ''' stat : PIF '(' VFLOAT ')' '{' stat_list_wrapper '}' opt_pelifs opt_pelse                                               
    '''
    p[0] = Node(vtype=v.PIF, children=[Node(vtype=v.FLOAT_VALUE, syn_value=p[3]),p[6],p[8],p[9]])

def p_opt_pelifs(p):
    ''' opt_pelifs : epsilon                                                                                               
                  | opt_pelifs PELIF '(' VFLOAT ')' '{' stat_list_wrapper '}'                                                 
    '''
    if len(p) == 9:
        p[0] = Node(vtype=v.PELIF, children=[p[1],Node(vtype=v.FLOAT_VALUE, syn_value=p[4]),p[7]])
    else: #len(p)==2                                                                                                      
        p[0] = None

def p_opt_pelse(p):
    ''' opt_pelse : epsilon   
                 | PELSE '{' stat_list_wrapper '}'                                                                     
    '''
    if len(p) == 5:
        p[0] = Node(vtype=v.PELSE, children=[p[3]])
    else:
        p[0] = None

##############################
## DECLARATIONS/ASSIGNMENTS ##
##############################

def p_stat_assign(p):
    '''stat : NAME non_empty_brack '=' expr    
    '''
    p[0] = Node(vtype=v.ASSIGNMENT, children=[Node(vtype=v.IDENTIFIER, symbol=p[1], children=[p[2]]), p[4]]) 

def p_stat_decl_assign(p):
    '''stat : decl '=' expr                                                                                                  
    '''
    p[0] = Node(vtype=v.DECLARATION_ASSIGNMENT, children=[p[1], p[3]] )#, symbol=p[1].children[1].symbol)

def p_stat_decl(p):
    '''stat : decl
    '''
    p[0] = p[1] 

############################
## ARITHMETIC EXPRESSIONS ##
############################

def p_expr_b(p):
    '''expr : b_expr'''
    p[0] = p[1]

#uminus and NOT may be incorrect precedence
def p_arith_expr(p):
    '''arith_expr : arith_expr '+' term
                  | arith_expr '-' term
                  | term
    '''
    if len(p) == 4:
        if p[2] == '+':
            p[0] = Node(vtype=v.ADD, children=[p[1], p[3]])
        else: 
            p[0] = Node(vtype=v.SUBTRACT, children=[p[1], p[3]])
    else: # len(p) == 2:
        p[0] = p[1]

def p_term(p):
    '''term : term '*' factor
            | term '/' factor
            | term '%' factor
            | factor
    '''
    if len(p) == 4:
        if p[2] == '*':
            p[0] = Node(vtype=v.MULTIPLY, children=[p[1], p[3]])
        elif p[2] == '/':
            p[0] = Node(vtype=v.DIVIDE, children=[p[1], p[3]])
        else: #p[2] == '%'
            p[0] = Node(vtype=v.MODULUS, children=[p[1], p[3]])
    else: #len(p) == 2
        p[0] = p[1]

def p_factor(p):
    '''factor : factor '^' pow
              | pow             
    '''
    if len(p) == 4:
       p[0] = Node(vtype=v.POWER, children=[p[1], p[3]])
    else:#len(p) == 2
       p[0] = p[1]

def p_power(p):
    ''' pow : '-' arith_expr %prec UMINUS
    '''                                                                             
    p[0] = Node(vtype=v.UMINUS, children=[p[2]])

#####################
## WEIGHTED VALUES ##
#####################

def p_weighted_values(p):
    ''' pow : '(' weighted_val_stat ')'
    '''
    p[0] = p[2]

def p_weighted_val_stat(p):
    ''' weighted_val_stat : weighted_val_clause weighted_val_clause_pipe
    '''
    p[0] = Node(vtype=v.WEIGHTED_VALUE_STAT, children=[p[1],p[2]])

def p_clause_pipe(p):
    ''' weighted_val_clause_pipe : '|' weighted_val_stat 
                                 | epsilon
    '''
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = None

#VINTEGER is non-negative
def p_weighted_val_clause(p):
    ''' weighted_val_clause : VINTEGER ':' pow
    '''
    p[0] = Node(vtype=v.WEIGHTED_VALUE_CLAUSE, children=[Node(vtype=v.INTEGER_VALUE, syn_value=p[1]),p[3]])

################################
## PRIMITIVES AND IDENTIFIERS ##
################################

def p_pow_function_call(p):
    ''' pow : function_call
    '''
    p[0] = p[1]

def p_integer(p):
    ''' pow : VINTEGER '''
    p[0] = Node(vtype=v.INTEGER_VALUE, syn_value=p[1])#p[1], Depends on responsibility to decide value (backend) 

def p_float(p):
    ''' pow : VFLOAT '''
    p[0] = Node(vtype=v.FLOAT_VALUE, syn_value=p[1])#p[1], see p_integer

def p_bool(p):
    ''' pow : VBOOLEAN '''
    p[0] = Node(vtype=v.BOOLEAN_VALUE, syn_value=p[1])#p[1], see p_integer    

def p_string(p):
    ''' pow : VSTRING '''
    p[0] = Node(vtype=v.STRING_VALUE, syn_value=p[1])#p[1], see p_integer    

def p_id(p):
    ''' pow : NAME non_empty_brack '''
    p[0] = Node(vtype=v.IDENTIFIER, symbol=p[1], children=[p[2]])

def p_expr_paren(p):
    ''' pow : '(' expr ')'
    '''
    p[0] = p[2]

#########################
## BOOLEAN EXPRESSIONS ##
#########################

def p_exprb(p):
    ''' b_expr : b_expr OR b_term 
               | b_term 
    '''         
    if len(p) == 4:
        p[0] = Node(vtype=v.OR, children=[p[1], p[3]])
    else:
        p[0] = p[1]

def p_termb(p):
    ''' b_term : b_term AND b_factor
               | b_factor
    '''
    if len(p) == 4:
        p[0] = Node(vtype=v.AND, children=[p[1], p[3]])
    else:
        p[0] = p[1]

def p_factorb(p):
    ''' b_factor : NOT b_primary
                 | b_primary
    '''
    if len(p) == 3:
        p[0] = Node(vtype=v.NOT, children=[p[2]])
    else:
        p[0] = p[1]        
          
def p_primaryb(p):
    ''' b_primary : b_condition   
    ''' 
    p[0] = p[1] 

def p_primaryb_aexpr(p):
    ''' b_primary : arith_expr
    '''
    p[0] = p[1]  

def p_conditionb(p):
    ''' b_condition : arith_expr '<' arith_expr
               | arith_expr '>' arith_expr
               | arith_expr GEQ arith_expr
               | arith_expr LEQ arith_expr
               | arith_expr EQ arith_expr
               | arith_expr NEQ arith_expr
    '''
    if p[2] == '<':
            p[0] = Node(vtype=v.LESS_THAN, children=[p[1], p[3]]) 
    elif p[2] == '>':
            p[0] = Node(vtype=v.GREATER_THAN, children=[p[1], p[3]])
    elif p[2] == '>=':
            p[0] = Node(vtype=v.GREATER_THAN_EQUAL, children=[p[1], p[3]])
    elif p[2] == '<=':
            p[0] = Node(vtype=v.LESS_THAN_EQUAL, children=[p[1], p[3]])
    elif p[2] == '==':
            p[0] = Node(vtype=v.EQUAL, children=[p[1], p[3]])
    elif p[2] == '!=':
            p[0] = Node(vtype=v.NOT_EQUAL, children=[p[1], p[3]])

################
## LIST TYPES ##
################

def p_decl(p):
    '''decl : list_type NAME
    '''
    p[0] = Node(vtype=v.DECLARATION, children=[p[1], Node(vtype=v.IDENTIFIER, symbol=p[2])]) #name is syn_value or symbol?
    symbol = p[2]
    backend.scopes[-1][symbol] = None

def p_list_type(p):
    ''' list_type : type brack
    '''
    p[0] = Node(vtype=v.LIST_TYPE, children=[p[1],p[2]], inh_value=p[1].syn_value+p[2].inh_value) #TODO: change these (and below) to syn_value

#VINTEGER is non-negative
def p_bracket(p):
    ''' brack : '[' VINTEGER ']' brack
              | '[' ']' brack
              | epsilon
    '''
    if len(p) == 5:
        p[0] = Node(vtype=v.BRACKET_DECL, children=[p[4]], inh_value=p[1]+p[2]+p[3]+p[4].inh_value)
    elif len(p) == 4:
        p[0] = Node(vtype=v.BRACKET_DECL, children=[p[3]], inh_value=p[1]+p[2]+p[3].inh_value)
    else:  
        p[0] = Node(vtype=v.BRACKET_DECL, inh_value='')

#VINTEGER is non-negative
def p_non_empty_bracket(p):
    ''' non_empty_brack :  '[' VINTEGER ']' non_empty_brack
                        | epsilon
    '''
    if len(p) == 5:
        p[0] = Node(vtype=v.BRACKET_ACCESS, children=[p[4]], inh_value=p[1]+p[2]+p[3]+p[4].inh_value)
    else:  
        p[0] = Node(vtype=v.BRACKET_ACCESS, inh_value='')

########################
## PRIMITIVE KEYWORDS ##
########################

def p_type_int(p):
    '''type : INTEGER 
    '''        
    p[0] = Node(vtype=v.INT_KEYWORD, syn_value=p[1]) ####using syn_value #<BASIC_TYPE>_KEYWORD

def p_type_float(p):
    '''type : FLOAT                                                                                                    
    '''  
    p[0] = Node(vtype=v.FLOAT_KEYWORD, syn_value=p[1])

def p_type_string(p):
    '''type : STRING 
    '''
    p[0] = Node(vtype=v.STRING_KEYWORD, syn_value=p[1])

def p_type_boolean(p):
    '''type : BOOLEAN
    '''
    p[0] = Node(vtype=v.BOOLEAN_KEYWORD, syn_value=p[1])

#def p_function(p):
    #'expr : NAME LPAREN expr RPAREN'
    #func = lexer.symbol_table.get(p[1])
    #p[0] = Node(vtype='FUNCTION', syn_value=func, children=[p[3]])

def p_epsilon(p):
    '''epsilon :'''
    pass

# Error rule for syntax errors
def p_error(p):
    print p
    print(u'Syntax error in input:\n\tInput: {}'.format(p))

# Build the parser
parser = yacc.yacc()

if __name__ == '__main__':
    pass    
