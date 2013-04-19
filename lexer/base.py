import ply.lex as lex
from backend.stdlib import builtins

class Lexer:
    """V prefix denotes value, not reserved word 
       INTEGER/FLOAT unsigned, unary minus dealt with in yacc"""

    #symbol_table = {}
    
    #later add things like 'env', etc
    reserved = {
        'string' : 'STRING',
        'int' : 'INTEGER',
        'float' : 'FLOAT',
        'boolean' : 'BOOLEAN',
        'and' : 'AND',
        'or' : 'OR',       
        'not' : 'NOT',
        'while' : 'WHILE',
        'if' : 'IF',
        'elif' : 'ELIF',
        'else' : 'ELSE',
        'pif' : 'PIF',
        'pelif' : 'PELIF',
        'pelse' : 'PELSE',
    }

    #add 'none' later
    tokens = [
        'NEWLINE',
        'NAME',
        'VSTRING',
        'VINTEGER',
        'VFLOAT',
        'VBOOLEAN',
        'EQ',
        'NEQ',
        'LEQ',
        'GEQ',
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
    
    literals = "+-*/%^()=\'\"<>[]{}"    #type=value for single characters
        
    t_VSTRING = r'("[^"]*")|(\'[^\']*\')'
    t_VINTEGER = r'[0-9]+'
    t_VFLOAT = r'[0-9]*\.[0-9]+'
    t_EQ = r'\=\='
    t_NEQ = r'\!\='
    t_LEQ = r'\<\='
    t_GEQ = r'\>\='
    
    def t_VBOOLEAN(self, t):
        r'true|false'
        t.type = "VBOOLEAN"    
        return t

    def t_NAME(self, t):
        r'[a-zA-Z_]+[a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value,'NAME')    # Check for reserved words    
        #if t.type == 'NAME':
            #symbol_table[t.value] = t.type
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        t.type = 'NEWLINE'
        return t

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
