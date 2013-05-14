import ply.yacc as yacc
from lexer import lexer
from tree import Node, Function, Conditional, List, Agent
import vtypes as v
import re
import traceback
from backend import backend
from error import *
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
    ('left', '.'),           
)

start =  'program'


def p_program(p):
    ''' program : stat_list_wrapper agent_list_wrapper stat_list_wrapper environment stat_list_wrapper terminate_block stat_list_wrapper analysis stat_list_wrapper
    '''
    p[0] = Node(vtype=v.PROGRAM, children=[p[2],p[4],p[6],p[8],p[1],p[3],p[5],p[7],p[9]])#order: agent, environment, terminate, analysis then all other statements in order

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
    children = p[1]
    if p[2]:
        children.extend(p[2])
    p[0] = Node(vtype=v.AGENT_LIST, children=children)

# TODO: dont require last newline                                                                               
def p_agentn(p):
    ''' agent_n : agent NEWLINE agent_n                                                                                    
              | epsilon                                                                                             
    '''
    if len(p) == 4:
        agents = [p[1]]
        if p[3]:
            agents.extend(p[3])
        p[0] = agents
    else:
        p[0] = None

def p_agent_1_cda(p):
    ''' agent : AGENT NAME '{' stat_list_wrapper create stat_list_wrapper destroy stat_list_wrapper action stat_list_wrapper '}'
    '''
    p[0] = Agent(symbol=p[2], statements=[p[4],p[6],p[8],p[10]], create=p[5],
                 action=p[9], destroy=p[7])

def p_agent_2_cad(p):
    ''' agent : AGENT NAME '{' stat_list_wrapper create stat_list_wrapper action stat_list_wrapper destroy stat_list_wrapper '}'
    '''
    p[0] = Agent(symbol=p[2], statements=[p[4],p[6],p[8],p[10]], create=p[5],
                 action=p[7], destroy=p[9])

def p_agent_3_dca(p):
    ''' agent : AGENT NAME '{' stat_list_wrapper destroy stat_list_wrapper create stat_list_wrapper action stat_list_wrapper '}'
    '''
    p[0] = Agent(symbol=p[2], statements=[p[4],p[6],p[8],p[10]], create=p[7],
                 action=p[9], destroy=p[5])

def p_agent_4_dac(p):
    ''' agent : AGENT NAME '{' stat_list_wrapper destroy stat_list_wrapper action stat_list_wrapper create stat_list_wrapper '}'
    '''
    p[0] = Agent(symbol=p[2], statements=[p[4],p[6],p[8],p[10]], create=p[9],
                 action=p[7], destroy=p[5])

def p_agent_5_adc(p):
    ''' agent : AGENT NAME '{' stat_list_wrapper action stat_list_wrapper destroy stat_list_wrapper create stat_list_wrapper '}'
    '''
    p[0] = Agent(symbol=p[2], statements=[p[4],p[6],p[8],p[10]], create=p[9],
                 action=p[5], destroy=p[7])

def p_agent_6_acd(p):
    ''' agent : AGENT NAME '{' stat_list_wrapper action stat_list_wrapper create stat_list_wrapper destroy stat_list_wrapper '}'
    '''
    p[0] = Agent(symbol=p[2], statements=[p[4],p[6],p[8],p[10]], create=p[7],
                 action=p[5], destroy=p[9])

def p_create(p):
    ''' create : CREATE '(' formal_param_list ')' '{' stat_list_wrapper '}'
    '''
    parameter_pairs = []
    if p[3] is not None:
        for decl in p[3].syn_value:
            parameter_pairs.append((decl.syn_vtype, decl.symbol))
    p[0] = Function(symbol=p[1], statements=p[6],
                    return_type=v.AGENT_VALUE, #use agent as placeholder for agent's name, which can't be known here
                    parameter_pairs=parameter_pairs,
                    return_value=Node(vtype=v.RETURN_STATEMENT, children=[]))

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
        p[0] = Node(vtype=v.INTEGER_VALUE, syn_value=int(p[1])) 
    else:
        p[0] = Node(vtype=v.INTEGER_VALUE, syn_value=1) #default frequency == 1

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
    children = p[1]
    if p[2]:
        children.extend(p[2])
    p[0] = Node(vtype=v.TERMINATE, children=children)

# TODO: dont require last newline                                                                               
def p_invariantn(p):
    '''invariant_n : invariant NEWLINE invariant_n                                                                                      
              | epsilon                                                                                             
    '''
    if len(p) == 4:
        kids = [p[1]]
        if p[3]:
            kids.extend(p[3])
        p[0] = kids
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
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
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
    children = []
    if p[1]:
        children = p[1].children
    if p[2]:
        children.extend(p[2])
    p[0] = Node(vtype=v.STATEMENT_LIST, children=children)

# TODO: dont require last newline                                                                               
def p_statn(p):
    '''stat_n : stat NEWLINE stat_n                                                                                      
              | epsilon                                                                                             
    '''
    if len(p) == 4:
        children = [p[1],]
        if p[3]:
            children.extend(p[3].children)
        p[0] = Node(vtype=v.STATEMENT, children=children)
    else:
        p[0] = None

###############
## FUNCTIONS ##
###############

#TODO stat_list_wrapper causes problems , does not exlcude function def within function def or loops, etc.
#list_type changed from return_type
def p_function_def(p):
    ''' stat : list_type NAME '(' formal_param_list ')' '{' stat_list_wrapper RETURN expr NEWLINE '}'
    '''
    parameter_pairs = []
    if p[4] is not None:
        for decl in p[4].syn_value:
            parameter_pairs.append((decl.syn_vtype, decl.symbol))
    p[0] = Function(symbol=p[2], statements=p[7],
                              return_type=p[1].vtype,
                              parameter_pairs=parameter_pairs,
                              return_value=Node(vtype=v.RETURN_STATEMENT, children=[p[9]]))

def p_void_function_def(p):
    ''' stat : NONE NAME '(' formal_param_list ')' '{' stat_list_wrapper RETURN NEWLINE '}'
    '''
    parameter_pairs = []
    if p[4] is not None:
        for decl in p[4].syn_value:
            parameter_pairs.append((decl.syn_vtype, decl.symbol))
    p[0] = Function(symbol=p[2], statements=p[7],
                              return_type=v.NONE_VALUE,
                              parameter_pairs=parameter_pairs,
                              return_value=Node(vtype=v.RETURN_STATEMENT))

#def p_return_stat(p):
#    ''' return_stat : RETURN expr NEWLINE 
#                    | RETURN NEWLINE
#    '''
#    if len(p) == 4:
#        p[0] = Node(vtype=v.RETURN_STATEMENT, children=[p[2]])
#    else:
#        p[0] = Node(vtype=v.RETURN_STATEMENT)     


def p_stat_function_call(p):
    ''' stat : scope function_call 
             | function_call 
    '''
    if len(p) == 3:
        p[0] = Node(vtype=v.IMPLICIT_PARAM, children=[p[1],p[2]])
    else:
        p[0]=p[1]

def p_formal_param_list(p):
    ''' formal_param_list : decl formal_param_comma
                          | epsilon
    '''  
    if len(p) == 3:
        params = [p[1]]
        if p[2]:
            params.extend(p[2].syn_value)
        p[0] = Node(vtype=v.FORMAL_PARAM_LIST, syn_value=params)
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
    if p[3] is not None:
        p[0] = Node(vtype=v.FUNCTION_CALL, symbol=p[1], children=p[3].children)
    else:
        p[0] = Node(vtype=v.FUNCTION_CALL, symbol=p[1])

def p_actual_param(p):
    ''' actual_param : expr
    '''
    p[0] = p[1]

def p_actual_param_list(p):
    ''' actual_param_list : actual_param actual_param_comma
                          | epsilon
    '''  
    if len(p) == 3:
        params = [p[1]]
        if (p[2]):
            params.extend(p[2].children)
        p[0] = Node(vtype=v.ACTUAL_PARAM_LIST, children=params)
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
    p[0] = Conditional(vtype=v.WHILE, expression=p[3], statements=p[6])

def p_repeat(p):
    ''' stat : REPEAT '(' expr ')' '{' stat_list_wrapper '}' 
    '''
    p[0] = Conditional(vtype=v.REPEAT, expression=p[3], statements=p[6])

#TODO: no newline allowed before elif/else, maybe fix this
def p_if(p):
    ''' stat : IF '(' expr ')' '{' stat_list_wrapper '}' opt_elifs opt_else  
    '''
    next_conditional = p[8] if p[8] else p[9]
    if next_conditional != p[9]:
        nc = p[8]
        if nc:
            while nc.next_conditional:
                nc = nc.next_conditional
            # we've got nc pointing at the last elif let's attach the else
            nc.next_conditional = p[9]
    p[0] = Conditional(vtype=v.IF, statements=p[6], expression=p[3], next_conditional=next_conditional)

def p_opt_elifs(p):
    ''' opt_elifs : epsilon
                  | ELIF '(' expr ')' '{' stat_list_wrapper '}' opt_elifs
    ''' 
    if len(p) == 9:
        p[0] = Conditional(vtype=v.ELIF, statements=p[6], expression=p[3], next_conditional=p[8])
    else: #len(p)==2
        p[0] = None

def p_opt_else(p):
    ''' opt_else : epsilon
                 | ELSE '{' stat_list_wrapper '}'
    '''
    if len(p) == 5:
        p[0] = Conditional(vtype=v.ELSE, statements=p[3])
    else:
        p[0] = None

#VFLOAT is non-negative
def p_pif(p):
    ''' stat : PIF '(' pow ')' '{' stat_list_wrapper '}' opt_pelifs opt_pelse
    '''
    total_prob = p[8][1] + p[3].syn_value if p[8] else p[3].syn_value
    if total_prob > 1:
        raise_error(SyntaxError, "Probability of pif-pelif-pelse cannot sum to greater than 1")

    next_conditional = p[8][0] if p[8] else p[9]
    if next_conditional != p[9]:
        nc = p[8][0]
        if nc:
            while nc.next_conditional:
                nc = nc.next_conditional
            # we've got nc pointing at the last elif let's attach the else
            nc.next_conditional = p[9]
    p[0] = Conditional(vtype=v.PIF, statements=p[6], expression=p[3], next_conditional=next_conditional)

def p_opt_pelifs(p):
    ''' opt_pelifs : epsilon
                   | PELIF '(' pow ')' '{' stat_list_wrapper '}' opt_pelifs
    '''
    if len(p) == 9:
        cond = p[8] if p[8] else (None, 0)
        p[0] = (Conditional(vtype=v.PELIF, statements=p[6], expression=p[3], next_conditional=cond[0]), p[3].syn_value+cond[1])
    else: #len(p)==2
        p[0] = None

def p_opt_pelse(p):
    ''' opt_pelse : epsilon   
                 | PELSE '{' stat_list_wrapper '}'
    '''
    if len(p) == 5:
        p[0] = Conditional(vtype=v.PELSE, statements=p[3])
    else:
        p[0] = None

##############################
## DECLARATIONS/ASSIGNMENTS ##
##############################

def p_stat_assign_scope(p):
    '''stat : scope NAME non_empty_brack '=' expr    
    '''
    kids = []
    if p[3].vtype == v.BRACKET_ACCESS:
        kids = [p[3]]
        if p[3].syn_value == -1:
            kids = [Node(vtype='?2')]
    id_node = Node(vtype=v.IDENTIFIER, symbol=p[2], children=kids)
    expression_node = p[5]
    p[0] = Node(vtype=v.ASSIGNMENT, children=[Node(vtype=v.IMPLICIT_PARAM, children=[p[1], id_node]), expression_node]) 

def p_stat_assign(p):
    '''stat : NAME non_empty_brack '=' expr    
    '''
    kids = []
    if p[2].vtype == v.BRACKET_ACCESS:
        kids = [p[2]]
        if p[2].syn_value == -1:
            kids = [Node(vtype='?2')]
    id_node = Node(vtype=v.IDENTIFIER, symbol=p[1], children=kids)
    expression_node = p[4]
    p[0] = Node(vtype=v.ASSIGNMENT, children=[id_node, expression_node]) 

def p_stat_decl_assign(p):
    '''stat : decl '=' expr                                                                                                  
    '''
    id_node = Node(vtype=v.IDENTIFIER, symbol=p[1].symbol)
    declaration_node = Node(vtype=v.DECLARATION, symbol=p[1].symbol, syn_vtype=p[1].syn_vtype)
    expression_node = p[3]
    assignment_node = Node(vtype=v.ASSIGNMENT, children=[id_node, expression_node])
    p[0] = Node(vtype=v.DECLARATION_ASSIGNMENT, children=[declaration_node,assignment_node] )

def p_stat_decl(p):
    '''stat : decl
    '''
    p[0] = p[1] 

#################
## EXPRESSIONS ##
#################

def p_expr_b(p):
    '''expr : b_expr
            | cast expr
    ''' 
    if len(p) == 2:
        p[0] = p[1]
    else: 
        p[0] = Node(vtype=v.CAST_EXPRESSION, children=[p[1],p[2]])

def p_cast(p):
    ''' cast : '(' type ')'
    '''
    p[0] = Node(vtype=v.EXPLICIT_CAST, children=[p[2]])

############################
## ARITHMETIC EXPRESSIONS ##
############################

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
    kids = [p[1]]
    if p[2]:
        kids.extend(p[2].children)
    p[0] = Node(vtype=v.WEIGHTED_VALUE_STAT, children=kids)

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
    p[0] = Node(vtype=v.WEIGHTED_VALUE_CLAUSE, children=[Node(vtype=v.INTEGER_VALUE, syn_value=int(p[1])),p[3]])


#########################
## BOOLEAN EXPRESSIONS ##
#########################

def p_exprb(p):
    ''' b_expr : b_expr OR b_term 
               | b_term 
    '''         
    if len(p) == 4:
        p[0] = Node(vtype=v.OR, syn_vtype=v.BOOLEAN_VALUE, children=[p[1], p[3]])
    else:
        p[0] = p[1]

def p_termb(p):
    ''' b_term : b_term AND b_factor
               | b_factor
    '''
    if len(p) == 4:
        p[0] = Node(vtype=v.AND, syn_vtype=v.BOOLEAN_VALUE, children=[p[1], p[3]])
    else:
        p[0] = p[1]

def p_factorb(p):
    ''' b_factor : NOT b_primary
                 | b_primary
    '''
    if len(p) == 3:
        p[0] = Node(vtype=v.NOT, syn_vtype=v.BOOLEAN_VALUE, children=[p[2]])
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
            p[0] = Node(vtype=v.LESS_THAN, syn_vtype=v.BOOLEAN_VALUE, children=[p[1], p[3]]) 
    elif p[2] == '>':
            p[0] = Node(vtype=v.GREATER_THAN, syn_vtype=v.BOOLEAN_VALUE, children=[p[1], p[3]])
    elif p[2] == '>=':
            p[0] = Node(vtype=v.GREATER_THAN_EQUAL, syn_vtype=v.BOOLEAN_VALUE, children=[p[1], p[3]])
    elif p[2] == '<=':
            p[0] = Node(vtype=v.LESS_THAN_EQUAL, syn_vtype=v.BOOLEAN_VALUE, children=[p[1], p[3]])
    elif p[2] == '==':
            p[0] = Node(vtype=v.EQUAL, syn_vtype=v.BOOLEAN_VALUE, children=[p[1], p[3]])
    elif p[2] == '!=':
            p[0] = Node(vtype=v.NOT_EQUAL, syn_vtype=v.BOOLEAN_VALUE, children=[p[1], p[3]])

################
## LIST TYPES ##
################

def p_list_declaration(p):
    ''' decl : '~' list_type NAME 
    '''
    # merge resolution may be incorrect @chris
    symbol = p[3]
    id_node = Node(vtype=v.IDENTIFIER, symbol=symbol)
    kids = [id_node]
    if p[2].vtype == v.LIST_TYPE:
        kids.append(p[2])
    p[0] = Node(vtype=v.DECLARATION, syn_vtype=p[2].vtype, symbol=symbol, children=kids)

def p_list_type(p):
    ''' list_type : type  brack
    '''
    if p[2].depths:  # for lists
        p[0] = Node(vtype=v.LIST_TYPE, syn_vtype=p[1].syn_vtype, depths=p[2].depths)
    else:  # for simple types
        p[0] = Node(vtype=p[1].syn_vtype)

###################
## list brackets ##
###################

def p_expr_bracket(p):
    ''' brack : '[' expr ']' brack
    '''
    kids=[p[2],]
    if p[4]:
        kids.extend(p[4].children)
    depths = []
    for x in kids:
        if x.symbol:
            depths.append(x.symbol)
        else:
            depths.append(x.syn_value)
    p[0] = Node(vtype=v.BRACKET_DECL, children=kids, depths=depths)
        
def p_no_expr_bracket(p):
    ''' brack : '[' ']' brack
    '''
    kids = [p[3].children]
    p[0] = Node(vtype=v.BRACKET_DECL, children=kids, depths=[p[3].syn_value])
              
def p_empty_bracket(p):
    ''' brack : epsilon
    '''
    p[0] = Node(vtype=v.BRACKET_DECL, syn_value=0)

#VINTEGER is non-negative
def p_non_empty_bracket(p):
    ''' non_empty_brack :  '[' expr ']' non_empty_brack
                        | epsilon
    '''
    if len(p) == 5:
        kids = [p[2]]
        if p[4]:
            kids.extend(p[4].children)
        p[0] = Node(vtype=v.BRACKET_ACCESS, children=kids, syn_value=[x.syn_value for x in kids])
    else:  
        # non_empty_bracket isn't always non-empty :/
        p[0] = Node(vtype=v.EMPTY_BRACKET, syn_value = -1)

########################
## PRIMITIVE KEYWORDS ##
########################

def p_type_int(p):
    '''type : INTEGER 
    '''        
    p[0] = Node(vtype=v.INT_KEYWORD, syn_vtype=v.INTEGER_VALUE)

def p_type_float(p):
    '''type : FLOAT                                                                                                    
    '''  
    p[0] = Node(vtype=v.FLOAT_KEYWORD, syn_vtype=v.FLOAT_VALUE)

def p_type_string(p):
    '''type : STRING 
    '''
    p[0] = Node(vtype=v.STRING_KEYWORD, syn_vtype=v.STRING_VALUE)

def p_type_boolean(p):
    '''type : BOOLEAN
    '''
    p[0] = Node(vtype=v.BOOLEAN_KEYWORD, syn_vtype=v.BOOLEAN_VALUE)

def p_type_agent(p):
    ''' type : NAME 
    '''
    p[0] = Node(vtype=v.AGENT_TYPE_KEYWORD, syn_vtype=v.AGENT_VALUE)

#def p_function(p):
    #'expr : NAME LPAREN expr RPAREN'
    #func = lexer.symbol_table.get(p[1])
    #p[0] = Node(vtype='FUNCTION', syn_value=func, children=[p[3]])

################################
## PRIMITIVES AND IDENTIFIERS ##
################################

def p_pow_function_call(p):
    ''' pow : scope function_call
             | function_call
    '''
    if len(p) == 3:
        p[0] = Node(vtype=v.IMPLICIT_PARAM, children=[p[1],p[2]])
    else:
        p[0] = p[1]

def p_integer(p):
    ''' pow : VINTEGER '''
    p[0] = Node(vtype=v.INTEGER_VALUE, syn_vtype=v.INTEGER_VALUE, syn_value=int(p[1]))#p[1], Depends on responsibility to decide value (backend) 

def p_float(p):
    ''' pow : VFLOAT '''
    p[0] = Node(vtype=v.FLOAT_VALUE, syn_vtype=v.FLOAT_VALUE, syn_value=float(p[1]))#p[1], see p_integer

def p_bool(p):
    ''' pow : VBOOLEAN '''
    boolean = True if p[1] == 'true' else False
    p[0] = Node(vtype=v.BOOLEAN_VALUE, syn_vtype=v.BOOLEAN_VALUE, syn_value=boolean)#p[1], see p_integer

def p_string(p):
    ''' pow : VSTRING '''
    p[0] = Node(vtype=v.STRING_VALUE, syn_vtype=v.STRING_VALUE, syn_value=str(p[1]))#p[1], see p_integer    

def p_none(p):
    ''' pow : NONE '''
    p[0] = Node(vtype=v.NONE_VALUE, syn_vtype=v.NONE_VALUE)

def p_id(p):
    ''' pow : scope NAME non_empty_brack 
            | NAME non_empty_brack
    '''
    kids = []
    if len(p) == 4:
        if p[3].vtype == v.BRACKET_ACCESS:
            kids = [p[3]]
        p[0] = Node(vtype=v.IMPLICIT_PARAM,children=[p[1],Node(vtype=v.IDENTIFIER, symbol=p[2], children=kids)])
    else:
        if p[2].vtype == v.BRACKET_ACCESS:
            kids = [p[2]]
        p[0] = Node(vtype=v.IDENTIFIER, symbol=p[1], children=kids)        

def p_scope(p):
    ''' scope : NAME '.'
    '''
    p[0] = Node(vtype=v.IMPLICIT_PARAM, symbol=p[1])
    


def p_expr_paren(p):
    ''' pow : '(' expr ')'
    '''
    p[0] = p[2]

def p_epsilon(p):
    '''epsilon :'''
    pass

# Error rule for syntax errors
def p_error(p):
    print p
    print(u'Syntax error in input:\n\tInput: {}'.format(p))

# Build the parser
parser = yacc.yacc()

backend.scopes[0]['TICKCOUNT'] = Node(vtype=v.INTEGER_VALUE, syn_vtype=v.INTEGER_VALUE, syn_value=1)

# very dirty hack to get the program to terminate on an error condition;
# before, it was continuing to run and failing somewhere later on in ply
# because the node wasnt constructed here properly
def raise_error(err, err_msg):
    try:
        raise err, err_msg
    except err:
        traceback.print_exc()
        exit(1)

if __name__ == '__main__':
    pass
