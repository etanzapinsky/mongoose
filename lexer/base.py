import ply.lex as lex
from backend.stdlib import builtins

class Lexer:
    """V prefix denotes value, not reserved word 
       INTEGER/FLOAT unsigned, unary minus dealt with in yacc"""
    
    #later add things like 'env', etc
    reserved = {
        'string' : 'STRING',
        'int' : 'INTEGER',
        'float' : 'FLOAT',
        'boolean' : 'BOOLEAN',
        'and' : 'AND',
        'or' : 'OR',       
        'not' : 'NOT',

    }

    tokens = [
        'NAME',
        'VSTRING',
        #'STRING',
        'VINTEGER',
        #'INTEGER',
        'VFLOAT',
        #'FLOAT',
        'VBOOLEAN',
        #'BOOLEAN',
        #'NONE',
        #'KNONE',
        #'SINGLEQUOTE',
        #'DOUBLEQUOTE',
        #'LPAREN',
        #'RPAREN',
        #'ASSIGNMENT',
        #'PLUS',
        #'MINUS',
        #'MULTIPLY',
        #'DIVIDE',
        #'MOD',
        #'POWER',
        #'LT',
        #'GT',
        'EQ',
        'NEQ',
        'LEQ',
        'GEQ',
        #'AND',
        #'OR',
        #'NOT',
    ] + list(reserved.values())

    def __init__(self):
        # symbol table is going to be a dict of
        # <mongoose function name>: <python function> key value pairs
        # call dict(builtins) even though builtins is a dict since we want copy,
        # and not to accidentally mutate any of the data
        self.symbol_table = dict(builtins)

    # parser was confusing NAME and STRING when no underscore infront of name
    # not sure why, have to look into it
    # (etan) i think i know what the issue is, name and strign should be the same
    # token, the meaning, i.e. is one a function name, variable name or string
    # is derived from the symbols surronding it.
    
    literals = "+-*/%^()=\'\"<>"    #type=value for single characters
        
    #t_NAME = r'[a-zA-Z_]+[a-zA-Z_0-9]*'
    t_VSTRING = r'("[^"]*")|(\'[^\']*\')'
    #t_STRING = r'string'
    t_VINTEGER = r'[0-9]+'
    #t_INTEGER = r'int'
    t_VFLOAT = r'[0-9]*\.[0-9]+'
    #t_FLOAT = r'float'
    #t_VBOOLEAN = r'true|false'
    #t_BOOLEAN = r'boolean'
    #t_SINGLEQUOTE = r'\''
    #t_DOUBLEQUOTE = r'"'
    #t_NONE = r'none' 
    #t_KNONE = r'none'
    #t_LPAREN = r'\('
    #t_RPAREN = r'\)'
    #t_ASSIGNMENT = r'='    
    #t_PLUS = r'\+'
    #t_MINUS = r'-'
    #t_MULTIPLY = r'\*'
    #t_DIVIDE = r'\\'
    #t_MOD = r'%'
    #t_POWER = r'\^'
    #t_LT = r'\<'
    #t_GT = r'\>'
    t_EQ = r'\=\='
    t_NEQ = r'\!\='
    t_LEQ = r'\<\='
    t_GEQ = r'\>\='
    #t_AND = r'and'
    #t_OR = r'or'
    #t_NOT = r'not'

    def t_VBOOLEAN(self, t):
        r'true|false'
        #if t.value == 'true':
        t.type = "VBOOLEAN"    
        return t

    def t_NAME(self, t):
        r'[a-zA-Z_]+[a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value,'NAME')    # Check for reserved words    
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    #def t_COMMENT(self, t):
        #r'\#.*'
        #pass

    t_ignore  = ' \t'

    def t_error(self, t):
        t.lexer.skip(1)

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def test(self, data):
        self.lexer.input(data)
        tokens = []
        for tok in self.lexer:
            print tok.type, tok.value
            tokens.append([tok.type, tok.value])
        return tokens

lexer = Lexer()
lexer.build()

while True:
    data = raw_input(">>   ")
    lexer.test(data)
