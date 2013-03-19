import ply.lex as lex
from stdlib import builtins

class Lexer:
    tokens = (
        'NAME',
        'STRING',
        'COMMENT',
        'QUOTE',
        'LPAREN',
        'RPAREN',
    )

    def __init__(self):
        # symbol table is going to be a dict of
        # <mongoose function name>: <python function> key value pairs
        # call dict(builtins) even though builtins is a dict since we want copy,
        # and not to accidentally mutate any of the data
        self.symbol_table = dict(builtins)

    # parser was confusing NAME and STRING when no underscore infront of name
    # not sure why, have to look into it
    t_NAME = r'_[a-zA-Z_]+'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_QUOTE = r'\"'
    # this is just temporary, we have to have a better def of what a string is
    t_STRING = r'[a-zA-Z0-9 ]+'

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_COMMENT(self, t):
        r'\#.*'
        pass

    t_ignore  = ' \t'

    def t_error(self, t):
        t.lexer.skip(1)

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def test(self, data):
        self.lexer.input(data)
        for tok in self.lexer:
            print tok.type, tok.value

lexer = Lexer()
lexer.build()
