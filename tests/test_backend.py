import unittest
import vtypes as v

from nose.tools import *
from parser import Node
from backend import backend
from backend.stdlib import first_order_ops


class BackendTests(unittest.TestCase):
    @classmethod
    def setup_class(self):
        self.int_node_zero = Node(vtype=v.INTEGER_VALUE, syn_value=0)
        self.int_node_one = Node(vtype=v.INTEGER_VALUE, syn_value=1)
        self.int_node_two = Node(vtype=v.INTEGER_VALUE, syn_value=2)
        self.int_node_neg_one = Node(vtype=v.INTEGER_VALUE, syn_value=-1)
        self.float_node_one = Node(vtype=v.FLOAT_VALUE, syn_value=1.0)
        self.float_node_two = Node(vtype=v.FLOAT_VALUE, syn_value=2.0)
        self.float_node_neg_one = Node(vtype=v.FLOAT_VALUE, syn_value=-1.0)
        self.string_node_empty = Node(vtype=v.FLOAT_VALUE, syn_value='')
        self.string_node_one = Node(vtype=v.STRING_VALUE, syn_value='1')
        self.bool_node_true = Node(vtype=v.BOOLEAN_VALUE, syn_value=True)
        self.bool_node_false = Node(vtype=v.BOOLEAN_VALUE, syn_value=False)
        self.none_node = Node(vtype=v.NONE_VALUE, syn_value=None)
        self.backend = Backend()

    def test_int_add(self):
        int_node_add = Node(vtype=v.ADD,
                             children=[self.int_node_one, self.int_node_two])
        self.backend.walk_ast(int_node_add)
        eq_(int_node_add.syn_value, 3)
        int_node_neg_two = Node(vtype=v.ADD,
                                children=[self.int_node_neg_one, self.int_node_neg_one])
        int_node_neg_four = Node(vtype=v.ADD,
                                 children=[int_node_neg_two, int_node_neg_two])
        int_node_four = Node(vtype=v.ADD,
                             children=[self.int_node_two, self.int_node_two])
        int_node_result = Node(vtype=v.ADD,
                               children=[int_node_four, int_node_neg_four])
        self.backend.walk_ast(int_node_result)
        eq_(int_node_result.syn_value, 0)

    def test_int_subtract(self):
        int_node_subtract = Node(vtype=v.SUBTRACT,
                             children=[self.int_node_one, self.int_node_two])
        self.backend.walk_ast(int_node_subtract)
        eq_(int_node_subtract.syn_value, -1)

    def test_int_multiply(self):
        int_node_multiply = Node(vtype=v.MULTIPLY,
                             children=[self.int_node_one, self.int_node_two])
        self.backend.walk_ast(int_node_multiply)
        eq_(int_node_multiply.syn_value, 2)

    def test_int_divide(self):
        int_node_divide = Node(vtype=v.DIVIDE,
                             children=[self.int_node_one, self.int_node_two])
        self.backend.walk_ast(int_node_divide)
        eq_(int_node_divide.syn_value, 0)

    def test_int_power(self):
        int_node_power = Node(vtype=v.POWER,
                             children=[self.int_node_one, self.int_node_two])
        self.backend.walk_ast(int_node_power)
        eq_(int_node_power.syn_value, 1)

    def test_int_modulus(self):
        int_node_modulus = Node(vtype=v.MODULUS,
                             children=[self.int_node_one, self.int_node_two])
        self.backend.walk_ast(int_node_modulus)
        eq_(int_node_modulus.syn_value, 1)

    def test_int_less_than(self):
        int_node_less_than = Node(vtype=v.LESS_THAN,
                             children=[self.int_node_one, self.int_node_two])
        self.backend.walk_ast(int_node_less_than)
        eq_(int_node_less_than.syn_value, True)

    def test_int_less_than_equal(self):
        int_node_less_than_equal = Node(vtype=v.LESS_THAN_EQUAL,
                             children=[self.int_node_one, self.int_node_one])
        self.backend.walk_ast(int_node_less_than_equal)
        eq_(int_node_less_than_equal.syn_value, True)

    def test_int_greater_than(self):
        int_node_greater_than = Node(vtype=v.GREATER_THAN,
                             children=[self.int_node_one, self.int_node_two])
        self.backend.walk_ast(int_node_greater_than)
        eq_(int_node_greater_than.syn_value, False)

    def test_int_greater_than_equal(self):
        int_node_greater_than_equal = Node(vtype=v.GREATER_THAN_EQUAL,
                             children=[self.int_node_one, self.int_node_one])
        self.backend.walk_ast(int_node_greater_than_equal)
        eq_(int_node_greater_than_equal.syn_value, True)

    def test_ints_equal(self):
        int_node_equal = Node(vtype=v.EQUAL,
                              children=[self.int_node_one, self.int_node_one])
        self.backend.walk_ast(int_node_equal)
        eq_(int_node_equal.syn_value, True)

    def test_ints_not_equal(self):
        int_node_not_equal = Node(vtype=v.NOT_EQUAL,
                                    children=[self.int_node_one, self.int_node_two])
        self.backend.walk_ast(int_node_not_equal)
        eq_(int_node_not_equal.syn_value, True)

    # Incomparable types
    @raises(TypeError)
    def test_int_float_incomparable_equal(self):
        equal_node = Node(vtype=v.EQUAL, children=[self.int_node_one, self.float_node_one])
        self.backend.walk_ast(equal_node)

    @raises(TypeError)
    def test_float_string_incomparable_equal(self):
        equal_node = Node(vtype=v.EQUAL, children=[self.float_node_one, self.string_node_one])
        self.backend.walk_ast(equal_node)

    @raises(TypeError)
    def test_float_bool_incomparable_equal(self):
        equal_node = Node(vtype=v.EQUAL, children=[self.float_node_one, self.bool_node_true])
        self.backend.walk_ast(equal_node)

    # Boolean operators
    @raises(TypeError)
    def test_boolean_op_and_no_args(self):
        node = Node(vtype=v.AND, children=[])
        self.backend.walk_ast(node)

    @raises(TypeError)
    def test_boolean_op_and_one_arg(self):
        node = Node(vtype=v.AND, children=[self.float_node_one])
        self.backend.walk_ast(node)

    def test_boolean_op_and(self):
        node = Node(vtype=v.AND, children=[self.float_node_one, self.int_node_neg_one])
        self.backend.walk_ast(node)
        eq_(node.syn_value, True)
        node = Node(vtype=v.AND, children=[self.float_node_one, self.int_node_zero])
        self.backend.walk_ast(node)
        eq_(node.syn_value, False)

    def test_boolean_op_or(self):
        node = Node(vtype=v.OR, children=[self.int_node_zero, self.int_node_neg_one])
        self.backend.walk_ast(node)
        eq_(node.syn_value, True)
        node = Node(vtype=v.OR, children=[self.int_node_zero, self.int_node_zero])
        self.backend.walk_ast(node)
        eq_(node.syn_value, False)

    def test_boolean_op_not(self):
        node = Node(vtype=v.NOT, children=[self.int_node_zero])
        self.backend.walk_ast(node)
        eq_(node.syn_value, True)
        node = Node(vtype=v.NOT, children=[self.string_node_empty])
        self.backend.walk_ast(node)
        eq_(node.syn_value, True)
        node = Node(vtype=v.NOT, children=[self.float_node_neg_one])
        self.backend.walk_ast(node)
        eq_(node.syn_value, False)

    @nottest  # requires scope
    def test_assignment(self):
        x_node = Node(vtype=v.IDENTIFIER, symbol='x')
        val_node = self.int_node_two
        assignment_node = Node(vtype=v.ASSIGNMENT, children=[x_node, val_node])
        self.backend.walk_ast(assignment_node)
        symbol_record = self.backend.scopes[-1][x_node.symbol]
        eq_(symbol_record, val_node)