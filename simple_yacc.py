import ply.yacc as yacc

from simple_lex import lexer
# hack to get the tokens since they are a global variable in the lexer object
tokens = lexer.tokens

class Node:
    def __init__(self, vtype, value, children):
        """
        @param vtype: str
        @param value: <anything>
        @param children: list(Node)
        """
        self.vtype = vtype
        self.value = value
        self.children = children

def p_function(p):
    'expr : NAME LPAREN expr RPAREN'
    func = lexer.symbol_table.get(p[1])
    p[0] = Node('FUNCTION', func, [p[3]])

def p_expr_string(p):
    'expr : QUOTE STRING QUOTE'
    p[0] = Node('STRING', p[2], [])

# Error rule for syntax errors
def p_error(p):
    print p
    print "Syntax error in input!"

# Build the parser
parser = yacc.yacc()
