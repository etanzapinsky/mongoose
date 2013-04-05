import ply.yacc as yacc
from ..lexer import lexer
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

    # Useful for testing 
    def __eq__(self, other):
        return bool(self.vtype == other.vtype and
                    self.value == other.value and
                    self.children == other.children) # shallow

    # Useful for debugging
    def __str__(self):
        return '[Node: {vtype}, {val}, {kids}]'.format(vtype=self.vtype,
                                                        val=self.value,
                                                        kids=self.children)

def p_function(p):
    'expr : NAME LPAREN expr RPAREN'
    func = lexer.symbol_table.get(p[1])
    p[0] = Node(vtype='FUNCTION', value=func, children=[p[3]])

def p_expr_string(p):
    'expr : QUOTE STRING QUOTE'
    p[0] = Node(vtype='STRING', value=p[2], children=[])

# Error rule for syntax errors
def p_error(p):
    print p
    print "Syntax error in input!"

# Build the parser
parser = yacc.yacc()
