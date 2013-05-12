import unittest
from lexer import lexer

class LexerTests(unittest.TestCase):
    # @classmethod
    # def setup_class(self):
    #     pass

    def tokenize(self, data):
        self.lex = lexer.lexer
        self.lex.input(data)
        tokens = []
        for tok in self.lex:
            print tok
            # tokens = "{} {},".format(tok.type, tok.value)
            #print tok.type, tok.value
            # tokens += tok.type+" "+tok.value+","
            tokens.append(tok)
        return tokens

    def test_int_assignment_single_value(self):
        tokens = self.tokenize("int x = 5")
        token_parts = [(t.type, t.value) for t in tokens]

        expected_parts = [
            ('INTEGER', 'int'),
            ('NAME', 'x'),
            ('=', '='),
            ('VINTEGER', '5'),
        ]
        assert token_parts == expected_parts

    def test_float_assignment_single_value(self):
        tokens = self.tokenize("float x = 5.5")
        token_parts = [(t.type, t.value) for t in tokens]

        expected_parts = [
            ('FLOAT', 'float'),
            ('NAME', 'x'),
            ('=', '='),
            ('VFLOAT', '5.5'),
        ]
        assert token_parts == expected_parts

    def test_string_double_quotes(self):
        tokens = self.tokenize("string x = \"abc\"")
        token_parts = [(t.type, t.value) for t in tokens]

        expected_parts = [
            ('STRING', 'string'),
            ('NAME', 'x'),
            ('=', '='),
            ('VSTRING', 'abc'),
        ]
        assert token_parts == expected_parts    

    def test_string_single_quotes(self):
        tokens = self.tokenize("string x = \'abc\'")
        token_parts = [(t.type, t.value) for t in tokens]

        expected_parts = [
            ('STRING', 'string'),
            ('NAME', 'x'),
            ('=', '='),
            ('VSTRING', 'abc'),
        ]
        assert token_parts == expected_parts     

    def test_boolean_assignment_true(self):
        tokens = self.tokenize("boolean x = true")
        token_parts = [(t.type, t.value) for t in tokens]

        expected_parts = [
            ('BOOLEAN', 'boolean'),
            ('NAME', 'x'),
            ('=', '='),
            ('VBOOLEAN', 'true'),
        ]
        assert token_parts == expected_parts  

    def test_boolean_assignment_false(self):
        tokens = self.tokenize("boolean x = false")
        token_parts = [(t.type, t.value) for t in tokens]

        expected_parts = [
            ('BOOLEAN', 'boolean'),
            ('NAME', 'x'),
            ('=', '='),
            ('VBOOLEAN', 'false'),
        ]
        assert token_parts == expected_parts    

    def test_integer_addition(self):
        tokens = self.tokenize("int x = 3+5")
        token_parts = [(t.type, t.value) for t in tokens]

        expected_parts = [
            ('INTEGER', 'int'),
            ('NAME', 'x'),
            ('=', '='),
            ('VINTEGER', '3'),
            ('+', '+'),
            ('VINTEGER', '5'),
        ]
        assert token_parts == expected_parts 

    def test_float_addition(self):
        tokens = self.tokenize("int x = 3.0 + 5.0")
        token_parts = [(t.type, t.value) for t in tokens]

        expected_parts = [
            ('INTEGER', 'int'),
            ('NAME', 'x'),
            ('=', '='),
            ('VFLOAT', '3.0'),
            ('+', '+'),
            ('VFLOAT', '5.0'),
        ]
        assert token_parts == expected_parts 

    def test_float_division(self):
        tokens = self.tokenize("int x = 3.0 / 5.0")
        token_parts = [(t.type, t.value) for t in tokens]

        expected_parts = [
            ('INTEGER', 'int'),
            ('NAME', 'x'),
            ('=', '='),
            ('VFLOAT', '3.0'),
            ('/', '/'),
            ('VFLOAT', '5.0'),
        ]
        assert token_parts == expected_parts     

    def test_float_addition(self):
        tokens = self.tokenize("int x = 3.0 + 5.0")
        token_parts = [(t.type, t.value) for t in tokens]

        expected_parts = [
            ('INTEGER', 'int'),
            ('NAME', 'x'),
            ('=', '='),
            ('VFLOAT', '3.0'),
            ('+', '+'),
            ('VFLOAT', '5.0'),
        ]
        assert token_parts == expected_parts 

    def test_int_less_than(self):
        tokens = self.tokenize("int x = 3 < 5")
        token_parts = [(t.type, t.value) for t in tokens]

        expected_parts = [
            ('INTEGER', 'int'),
            ('NAME', 'x'),
            ('=', '='),
            ('VINTEGER', '3'),
            ('<', '<'),
            ('VINTEGER', '5'),
        ]
        assert token_parts == expected_parts 

    def test_float_less_than_or_equal(self):
        tokens = self.tokenize("int x = 3.0 <= 5.0")
        token_parts = [(t.type, t.value) for t in tokens]

        expected_parts = [
            ('INTEGER', 'int'),
            ('NAME', 'x'),
            ('=', '='),
            ('VFLOAT', '3.0'),
            ('LEQ', '<='),
            ('VFLOAT', '5.0'),
        ]
        assert token_parts == expected_parts 

    def test_float_greater_than_or_equal(self):
        tokens = self.tokenize("int x = 21.79 >= .512")
        token_parts = [(t.type, t.value) for t in tokens]

        expected_parts = [
            ('INTEGER', 'int'),
            ('NAME', 'x'),
            ('=', '='),
            ('VFLOAT', '21.79'),
            ('GEQ', '>='),
            ('VFLOAT', '.512'),
        ]
        assert token_parts == expected_parts 

    def test_float_equal_equal(self):
        tokens = self.tokenize("int x = -453.10 == 554.0")
        token_parts = [(t.type, t.value) for t in tokens]

        expected_parts = [
            ('INTEGER', 'int'),
            ('NAME', 'x'),
            ('=', '='),
            ('-','-'),
            ('VFLOAT', '453.10'),
            ('EQ', '=='),
            ('VFLOAT', '554.0'),
        ]
        assert token_parts == expected_parts 

    def test_int_not_equal(self):
        tokens = self.tokenize("int x = -23 != 5434")
        token_parts = [(t.type, t.value) for t in tokens]

        expected_parts = [
            ('INTEGER', 'int'),
            ('NAME', 'x'),
            ('=', '='),
            ('-','-'),
            ('VINTEGER', '23'),
            ('NEQ', '!='),
            ('VINTEGER', '5434'),
        ]
        assert token_parts == expected_parts 

    def test_true_or_not(self):
        tokens = self.tokenize("true and or not false")
        token_parts = [(t.type, t.value) for t in tokens]

        expected_parts = [
            ('VBOOLEAN', 'true'),
            ('AND', 'and'),
            ('OR', 'or'),
            ('NOT','not'),
            ('VBOOLEAN', 'false'),
        ]
        assert token_parts == expected_parts 

    def test_float_times_plus_paren(self):
         tokens = self.tokenize("3.0*(4.7+2.3)")
         token_parts = [(t.type, t.value) for t in tokens]
         expected_parts = [
             ('VFLOAT', '3.0'),
         ('*', '*'),
             ('(', '('),
             ('VFLOAT', '4.7'),
             ('+', '+'),
             ('VFLOAT', '2.3'),
             (')', ')'),
         ]
         assert token_parts == expected_parts


    def test_float_assoc_plus(self):
         tokens = self.tokenize("3.0+(4.7+2.3)")
         token_parts = [(t.type, t.value) for t in tokens]
         expected_parts = [
             ('VFLOAT', '3.0'),
             ('+', '+'),
             ('(', '('),
             ('VFLOAT', '4.7'),
             ('+', '+'),
             ('VFLOAT', '2.3'),
             (')', ')'),
         ]
         assert token_parts == expected_parts

    def test_boolean_joint_gt(self):
         tokens = self.tokenize("boolean xy = 4>5")
         token_parts = [(t.type, t.value) for t in tokens]
         expected_parts = [
             ('BOOLEAN', 'boolean'),
         ('NAME', 'xy'),
             ('=', '='),
             ('VINTEGER', '4'),
             ('>', '>'),
             ('VINTEGER', '5'),
         ]
         assert token_parts == expected_parts

    def test_string_joint_concat(self):
         tokens = self.tokenize("string x = \"ab\" + \'cd\'")
         token_parts = [(t.type, t.value) for t in tokens]
         expected_parts = [
             ('STRING', 'string'),
         ('NAME', 'x'),
             ('=', '='),
             ('VSTRING', 'ab'),
             ('+', '+'),
             ('VSTRING', 'cd'),
         ]
         assert token_parts == expected_parts

    def test_int_joint_arith(self):
         tokens = self.tokenize("int x = 4 + 5 * 6")
         token_parts = [(t.type, t.value) for t in tokens]
         expected_parts = [
             ('INTEGER', 'int'),
         ('NAME', 'x'),
             ('=', '='),
             ('VINTEGER', '4'),
             ('+', '+'),
             ('VINTEGER', '5'),
             ('*', '*'),
             ('VINTEGER', '6'),
         ]
         assert token_parts == expected_parts

    def test_unary_minus_float(self):
         tokens = self.tokenize("-4.0")
         token_parts = [(t.type, t.value) for t in tokens]
         expected_parts = [
             ('-', '-'),
         ('VFLOAT', '4.0'),
         ]
         assert token_parts == expected_parts

    def test_unary_minus_int(self):
         tokens = self.tokenize("-4")
         token_parts = [(t.type, t.value) for t in tokens]
         expected_parts = [
             ('-', '-'),
         ('VINTEGER', '4'),
         ]
         assert token_parts == expected_parts

    def test_if_elif_else_complex(self):
         tokens = self.tokenize("if(4 == 5) {int x = 9} elif(7<5){int x = 0} elif(3 != 4) {float c = 6.0} else {boolean t = true}")
         token_parts = [(t.type, t.value) for t in tokens]
         expected_parts = [
             ('IF', 'if'),
        ('(', '('),
        ('VINTEGER', '4'),
        ('EQ', '=='),
        ('VINTEGER', '5'),
        (')', ')'),
        ('{', '{'),
        ('INTEGER', 'int'),
        ('NAME', 'x'),
        ('=', '='),
        ('VINTEGER', '9'),
        ('}', '}'),
        ('ELIF', 'elif'),
        ('(', '('),
        ('VINTEGER', '7'),
        ('<', '<'),
        ('VINTEGER', '5'),
        (')', ')'),
        ('{', '{'),
        ('INTEGER', 'int'),
        ('NAME', 'x'),
        ('=', '='),
        ('VINTEGER', '0'),
        ('}', '}'),
        ('ELIF', 'elif'),
        ('(', '('),
        ('VINTEGER', '3'),
        ('NEQ', '!='),
        ('VINTEGER', '4'),
        (')', ')'),
        ('{', '{'),
        ('FLOAT', 'float'),
        ('NAME', 'c'),
        ('=', '='),
        ('VFLOAT', '6.0'),
        ('}', '}'),
        ('ELSE', 'else'),
        ('{', '{'),
        ('BOOLEAN', 'boolean'),
        ('NAME', 't'),
        ('=', '='),
        ('VBOOLEAN', 'true'),
        ('}', '}'),
                 ]
         assert token_parts == expected_parts

    def test_while(self):
         tokens = self.tokenize("while((3*4)<=(-4)) {int f = 0}")
         token_parts = [(t.type, t.value) for t in tokens]
         expected_parts = [
             ('WHILE', 'while'),
            ('(', '('),
            ('(', '('),
            ('VINTEGER', '3'),
            ('*', '*'),
            ('VINTEGER', '4'),
            (')', ')'),
            ('LEQ', '<='),
            ('(', '('),
            ('-', '-'),
            ('VINTEGER', '4'),
            (')', ')'),
            (')', ')'),
            ('{', '{'),
            ('INTEGER', 'int'),
            ('NAME', 'f'),
            ('=', '='),
            ('VINTEGER', '0'),
            ('}', '}'),
         ]
         assert token_parts == expected_parts

    def test_pif(self):
         tokens = self.tokenize("pif(5.6) {x = 5}")
         token_parts = [(t.type, t.value) for t in tokens]
         expected_parts = [
             ('PIF', 'pif'),
            ('(', '('),
            ('VFLOAT', '5.6'),
            (')', ')'),
            ('{', '{'),
            ('NAME', 'x'),
            ('=', '='),
            ('VINTEGER', '5'),
            ('}', '}'),
                     ]
         assert token_parts == expected_parts

    def test_list_decl_empty(self):
         tokens = self.tokenize("int[] x")
         token_parts = [(t.type, t.value) for t in tokens]
         expected_parts = [
             ('INTEGER', 'int'),
         ('[', '['),
         (']', ']'),
         ('NAME', 'x'),
         ]
         assert token_parts == expected_parts

    def test_list_decl_empty(self):
         tokens = self.tokenize("int[5] x")
         token_parts = [(t.type, t.value) for t in tokens]
         expected_parts = [
             ('INTEGER', 'int'),
         ('[', '['),
             ('VINTEGER', '5'),
         (']', ']'),
         ('NAME', 'x'),
         ]
         assert token_parts == expected_parts

    def test_pow_neq(self):
         tokens = self.tokenize("3 != 4^7")
         token_parts = [(t.type, t.value) for t in tokens]
         expected_parts = [
                ('VINTEGER', '3'),
                ('NEQ', '!='),
                ('VINTEGER', '4'),
                ('^', '^'),
                ('VINTEGER', '7'),
         ]
         assert token_parts == expected_parts

    def test_mod_eq(self):
         tokens = self.tokenize("3 == 44%7")
         token_parts = [(t.type, t.value) for t in tokens]
         expected_parts = [
             ('VINTEGER', '3'),
         ('EQ', '=='),
             ('VINTEGER', '44'),
         ('%', '%'),
         ('VINTEGER', '7'),
         ]
         assert token_parts == expected_parts

    def test_string(self):
         tokens = self.tokenize("string s = 'abc'")
         token_parts = [(t.type, t.value) for t in tokens]
         expected_parts = [
             ('STRING', 'string'),
         ('NAME', 's'),
             ('=', '='),
         ('VSTRING', 'abc'),
         ]
         assert token_parts == expected_parts    

# lexer = LexerTests() # dbug hack