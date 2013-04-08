import ply.yacc as yacc
from ..lexer import lexer
from tree import Node
# hack to get the tokens since they are a global variable in the lexer object
tokens = lexer.tokens

def p_function(p):
    'expr : NAME LPAREN expr RPAREN'
    func = lexer.symbol_table.get(p[1])
    p[0] = Node(vtype='FUNCTION', syn_value=func, children=[p[3]])

def p_expr_string(p):
    'expr : QUOTE STRING QUOTE'
    p[0] = Node(vtype='STRING', syn_value=p[2])

# Error rule for syntax errors
def p_error(p):
    print p
    print "Syntax error in input!"

# Build the parser
parser = yacc.yacc()
