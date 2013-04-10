import ply.lex as lex
from backend.stdlib import builtins

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
    # (etan) i think i know what the issue is, name and strign should be the same
    # token, the meaning, i.e. is one a function name, variable name or string
    # is derived from the symbols surronding it.
    t_NAME = r'_[a-zA-Z_]+'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_QUOTE = r'\"'
    t_STRING = r'[a-zA-Z0-9 ]+' # doesn't match the empty string @todo


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
        tokens = []
        for tok in self.lexer:
            print tok.type, tok.value
            tokens.append([tok.type, tok.value])
        return tokens

lexer = Lexer()
lexer.build()
