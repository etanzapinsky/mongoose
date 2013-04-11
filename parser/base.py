import ply.yacc as yacc
from lexer import lexer
from tree import Node
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
    ('right', 'NOT', 'UMINUS'),           
)

start = 'stat'

#(prob correct) unsure if literals should be in single quotes
#add int x = y,   x = y
def p_stat_assign(p):
    '''stat : NAME '=' expr    
    '''
    p[0] = Node(vtype='ASSIGNMENT', children=[Node(vtype='NAME', syn_value=p[1]), p[3]])

def p_stat_decl_assign(p):
    '''stat : decl '=' expr                                                                                                                             
    '''
    p[0] = Node(vtype='DECLARATION_ASSIGNMENT', children=[p[1], p[3]])

def p_stat_decl(p):
    '''stat : decl
    '''
    p[0] = p[1] #Node(vtype='DECLARATION2', children=[p[1]]) #might just be  p[0]=p[1]

def p_expr_a(p):
    '''expr : arith_expr'''
    p[0] = p[1]

def p_expr_b(p):
    '''expr : b_expr'''
    p[0] = p[1]

def p_expr_s(p):
    '''expr : s_expr'''
    p[0] = p[1]

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
            p[0] = Node(vtype='ADDITION', children=[p[1], p[3]])
        else: 
            p[0] = Node(vtype='SUBTRACTION', children=[p[1], p[3]])
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
            p[0] = Node(vtype='MULTIPLICATION', children=[p[1], p[3]])
        elif p[2] == '/':
            p[0] = Node(vtype='DIVISION', children=[p[1], p[3]])
        else: #p[2] == '%'
            p[0] = Node(vtype='MODULUS', children=[p[1], p[3]])
    else: #len(p) == 2
        p[0] = p[1]

def p_factor(p):
    '''factor : factor '^' pow
              | pow             
    '''
    if len(p) == 4:
       p[0] = Node(vtype='POWER', children=[p[1], p[3]])
    else:#len(p) == 2
       p[0] = p[1]

def p_power(p):
    ''' pow : '(' arith_expr ')'
            | '-' arith_expr %prec UMINUS
    '''
    if len(p) == 4:
        p[0] = p[2] 
    else: #len(p) == 3                                                                                                   
        p[0] = Node(vtype='UMINUS', children=[p[2]])

def p_integer(p):
    ''' pow : VINTEGER '''
    p[0] = Node(vtype='INTEGER_VALUE', syn_value=p[1])#p[1], Depends on responsibility to decide value 

def p_float(p):
    ''' pow : VFLOAT '''
    p[0] = Node(vtype='FLOAT_VALUE', syn_value=p[1])#p[1], see p_integer

# (fixed) NOT my be incorrect (should have highest precedence) -same with uminus?
def p_exprb(p):
    ''' b_expr : b_term 
               | b_expr OR b_term 
    '''         
    if len(p) == 4:
        p[0] = Node(vtype='OR', children=[p[1], p[3]])
    else:
        p[0] = p[1]

def p_termb(p):
    ''' b_term : b_factor                                                                                       
               | b_term AND b_factor                                                                                    
    '''
    if len(p) == 4:
        p[0] = Node(vtype='AND', children=[p[1], p[3]])
    else:
        p[0] = p[1]

def p_factorb(p):
    ''' b_factor : NOT b_primary
                 | b_primary
    '''
    if len(p) == 3:
        p[0] = Node(vtype='NOT', children=[p[2]])
    else:
        p[0] = p[1]        
          
def p_primaryb(p):
    ''' b_primary : b_condition 
                  | '(' b_expr ')'
    '''
    if len(p) == 4:                                                                                                                                                      
        p[0] = p[2] 
    else:
        p[0] = p[1] 

def p_primaryb_bool(p):
    ''' b_primary : VBOOLEAN '''
    p[0] = Node(vtype='BOOL_VALUE', syn_value=p[1])#p[1], see p_integer   

def p_conditionb(p):
    ''' b_condition : arith_expr '<' arith_expr
               | arith_expr '>' arith_expr
               | arith_expr GEQ arith_expr
               | arith_expr LEQ arith_expr
               | expr EQ expr
               | expr NEQ expr
    '''
    if p[2] == '<':
            p[0] = Node(vtype='LT', children=[p[1], p[3]])
    elif p[2] == '>':
            p[0] = Node(vtype='GT', children=[p[1], p[3]])
    elif p[2] == 'GEQ':
            p[0] = Node(vtype='GEQ', children=[p[1], p[3]])
    elif p[2] == 'LEQ':
            p[0] = Node(vtype='LEQ', children=[p[1], p[3]])
    elif p[2] == 'EQ':
            p[0] = Node(vtype='EQUAL', children=[p[1], p[3]])
    elif p[2] == 'NEQ':
            p[0] = Node(vtype='NOT_EQUAL', children=[p[1], p[3]])

#########
#     ''' b_expr : b_expr AND b_expr
#               | b_expr OR b_expr
#               | b_expr2
#               | expr EQ expr
#               | expr NEQ expr
#               | VBOOLEAN
#               | arith_expr '<' arith_expr
#               | arith_expr '>' arith_expr 
#               | arith_expr GEQ arith_expr 
#               | arith_expr LEQ arith_expr  
#    '''
#   if len(p) == 4:
#        if p[2] == 'AND':
#            p[0] = Node(vtype='AND', children=[p[1], p[3]])
#        elif p[2] == 'OR':
#            p[0] = Node(vtype='OR', children=[p[1], p[3]])
#        elif p[2] == '<':
#            p[0] = Node(vtype='LT', children=[p[1], p[3]])
#        elif p[2] == '>':
#            p[0] = Node(vtype='GT', children=[p[1], p[3]])
#        elif p[2] == 'GEQ':
#            p[0] = Node(vtype='GEQ', children=[p[1], p[3]])
#        elif p[2] == 'LEQ':
#            p[0] = Node(vtype='LEQ', children=[p[1], p[3]])
#        elif p[2] == 'EQ':
#            p[0] = Node(vtype='EQUAL', children=[p[1], p[3]])
#        elif p[2] == 'NEQ':
#            p[0] = Node(vtype='NOT_EQUAL', children=[p[1], p[3]])
#        #else: #p[1] == '('
#        #    p[0] = p[2]
#    #elif len(p) == 3:
#    #    p[0] = Node(vtype='NOT', children=[p[2]])
#    else: #len(p) == 2
#        p[0] = Node(vtype='BOOL_VALUE', syn_value=p[1])#p[1], see p_integer

#def p_exprboolean2(p):
#    ''' b_expr2 : NOT b_expr
#                | '(' b_expr ')'
#    '''
#    if len(p) == 3:
#        p[0] = Node(vtype='NOT', children=[p[2]]) 
#    else: # if len(p)==4
#        p[0] = p[2]       


def p_exprs(p):
    '''s_expr : s_expr '+' s_expr
              | VSTRING
    '''
    if len(p) == 4:
        p[0] = Node(vtype='CONCAT', children=[p[1], p[3]])
    else: #len(p) == 2
        p[0] = Node(vtype='STRING_VALUE', syn_value=p[1])

def p_decl(p):
    '''decl : type NAME
    '''
    p[0] = Node(vtype='DECLARATION', children=[p[1], Node(vtype='NAME', syn_value=p[2])]) ##testing NAME

def p_type(p):
    '''type : INTEGER 
            | FLOAT 
            | STRING 
            | BOOLEAN'''
    p[0] = Node(vtype='BASIC_TYPE', syn_value=p[1]) ####using syn_value

#def p_function(p):
    #'expr : NAME LPAREN expr RPAREN'
    #func = lexer.symbol_table.get(p[1])
    #p[0] = Node(vtype='FUNCTION', syn_value=func, children=[p[3]])

#def p_string(p):
    #'string : QUOTE STRING QUOTE'
    #p[0] = Node(vtype='STRING', syn_value=p[2])


# Error rule for syntax errors
def p_error(p):
    print p
    print "Syntax error in input!"

# Build the parser
parser = yacc.yacc()


#test
def traverse(root):
    traversePost(root, 0)

def traversePost(root, indent): #postorder
    if type(root) is 'str':
        print root, "is a str. oops"

    if(root is not None ):
        for n in root.children:
            traversePost(n, indent+1)
        #print ' '*indent
        if len(root.children) == 0: #leaf
            print '     '*indent + root.vtype,':',root.syn_value
        else: #non-leaf
            print '    '*indent + root.vtype

if __name__ == "__main__": 
    while True:
        try:
            s = raw_input('y>>   ')
        except EOFError:
            break
        if not s: continue
        result = parser.parse(s)
        print "result is of type", type(result)
        traverse(result)
        print "done"
