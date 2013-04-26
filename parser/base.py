import ply.yacc as yacc
from lexer import lexer
from tree import Node, Function
import vtypes as v
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

start = 'stat_list_wrapper'

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

#def p_stat_list_wrapper_2(p):
#    ''' stat_list_wrapper : stat_list NEWLINE
#    '''
#    p[0] = p[1]

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


def p_stat_assign(p):
    '''stat : NAME '=' expr    
    '''
    p[0] = Node(vtype=v.ASSIGNMENT, children=[Node(vtype=v.IDENTIFIER, symbol=p[1]), p[3]]) 

def p_stat_decl_assign(p):
    '''stat : decl '=' expr                                                                                                  '''
    p[0] = Node(vtype=v.DECLARATION_ASSIGNMENT, children=[p[1], p[3]] )#, symbol=p[1].children[1].symbol)

def p_stat_decl(p):
    '''stat : decl
    '''
    p[0] = p[1] 

#def p_expr_a(p):
#    '''expr : arith_expr'''
#    p[0] = p[1]

def p_expr_b(p):
    '''expr : b_expr'''
    p[0] = p[1]

#def p_expr_s(p):
#    '''expr : s_expr'''
#    p[0] = p[1]

#def p_expr_none(p):
    #'''expr : NONE'''
    #p[0] = None

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
    #else: #len(p) == 3
    #    p[0] = Node(vtype='UMINUS', children=[p[2]])

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
    '''# | '(' arith_expr ')' 
    #if len(p) == 4:
    #    p[0] = p[2] 
    #else: #len(p) == 3                                                                                                 
    p[0] = Node(vtype=v.UMINUS, children=[p[2]])

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
    ''' pow : NAME '''
    p[0] = Node(vtype=v.IDENTIFIER, symbol=p[1])

def p_expr_paren(p):
    ''' pow : '(' expr ')'
    '''
    p[0] = p[2]

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
    ''' #| '(' b_expr ')' 
    #if len(p) == 4:
    #    p[0] = p[2] 
    #else:
    p[0] = p[1] 

def p_primaryb_aexpr(p):
    ''' b_primary : arith_expr
    '''
    p[0] = p[1] 

#def p_bool_id(p):
#    ''' b_primary : NAME 
#    '''
#    p[0] = Node(vtype=v.IDENTIFIER, symbol=p[1])

#def p_primaryb_bool(p):
#    ''' b_primary : VBOOLEAN '''
#    p[0] = Node(vtype=v.BOOLEAN_VALUE, syn_value=p[1])#p[1], see p_integer   

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

#def p_exprs(p):
#    '''s_expr : s_expr '+' s_expr
#              | VSTRING
#    '''
#    if len(p) == 4:
#        p[0] = Node(vtype=v.CONCATENATE, children=[p[1], p[3]])
#    else: #len(p) == 2
#        p[0] = Node(vtype=v.STRING_VALUE, syn_value=p[1].strip("\'\""))

#def p_string_id(p):
#    ''' s_expr : NAME
#    '''
#    p[0] = Node(vtype=v.IDENTIFIER, symbol=p[1])

def p_decl(p):
    '''decl : list_type NAME
    '''
    p[0] = Node(vtype=v.DECLARATION, children=[p[1], Node(vtype=v.IDENTIFIER, symbol=p[2])]) #name is syn_value or symbol?

def p_list_type(p):
    ''' list_type : type brack
    '''
    p[0] = Node(vtype=v.LIST_TYPE, children=[p[1],p[2]], inh_value=p[2].inh_value) #TODO: change these (and below) to syn_value

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
