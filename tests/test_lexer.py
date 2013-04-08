from nose.tools import *
from ..lexer import lexer

# We should fill these out to increase code coverage. @todo (bo)
# See https://nose.readthedocs.org/en/latest/
# Also see: https://nose.readthedocs.org/en/latest/testing_tools.html

def test_lex_string_literals():
    eq_([['STRING', 'string']], lexer.test('string'))

    eq_([['QUOTE', r'"'],
         ['STRING', 'string'],
         ['QUOTE', r'"']],
        lexer.test(r'"string"'))
