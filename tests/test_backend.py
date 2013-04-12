import unittest
import vtypes as v

from nose.tools import *
from parser import Node
from backend import walk_ast, SCOPES
from backend.stdlib import first_order_ops


class BackendTests(unittest.TestCase):
    @classmethod
    def setup_class(self):
        self.int_node_zero = Node(vtype='INT', syn_value=0)
        self.int_node_one = Node(vtype='INT', syn_value=1)
        self.int_node_two = Node(vtype='INT', syn_value=2)
        self.int_node_neg_one = Node(vtype='INT', syn_value=-1)
        self.float_node_one = Node(vtype='FLOAT', syn_value=1.0)
        self.float_node_two = Node(vtype='FLOAT', syn_value=2.0)
        self.float_node_neg_one = Node(vtype='FLOAT', syn_value=-1.0)
        self.string_node_empty = Node(vtype='FLOAT', syn_value='')
        self.string_node_one = Node(vtype='STRING', syn_value='1')
        self.bool_node_true = Node(vtype='BOOLEAN', syn_value=True)
        self.bool_node_false = Node(vtype='BOOLEAN', syn_value=False)
        self.none_node = Node(vtype='NONE', syn_value=None)

    def test_int_add(self):
        int_node_add = Node(vtype='ADD',
                             children=[self.int_node_one, self.int_node_two])
        walk_ast(int_node_add)
        eq_(int_node_add.syn_value, 3)

    def test_int_subtract(self):
        int_node_subtract = Node(vtype='SUBTRACT',
                             children=[self.int_node_one, self.int_node_two])
        walk_ast(int_node_subtract)
        eq_(int_node_subtract.syn_value, -1)

    def test_int_multiply(self):
        int_node_multiply = Node(vtype='MULTIPLY',
                             children=[self.int_node_one, self.int_node_two])
        walk_ast(int_node_multiply)
        eq_(int_node_multiply.syn_value, 2)

    def test_int_divide(self):
        int_node_divide = Node(vtype='DIVIDE',
                             children=[self.int_node_one, self.int_node_two])
        walk_ast(int_node_divide)
        eq_(int_node_divide.syn_value, 0)

    def test_int_power(self):
        int_node_power = Node(vtype='POWER',
                             children=[self.int_node_one, self.int_node_two])
        walk_ast(int_node_power)
        eq_(int_node_power.syn_value, 1)

    def test_int_modulus(self):
        int_node_modulus = Node(vtype='MODULUS',
                             children=[self.int_node_one, self.int_node_two])
        walk_ast(int_node_modulus)
        eq_(int_node_modulus.syn_value, 1)

    def test_int_less_than(self):
        int_node_less_than = Node(vtype='LESS_THAN',
                             children=[self.int_node_one, self.int_node_two])
        walk_ast(int_node_less_than)
        eq_(int_node_less_than.syn_value, True)

    def test_int_less_than_equal(self):
        int_node_less_than_equal = Node(vtype='LESS_THAN_EQUAL',
                             children=[self.int_node_one, self.int_node_one])
        walk_ast(int_node_less_than_equal)
        eq_(int_node_less_than_equal.syn_value, True)

    def test_int_greater_than(self):
        int_node_greater_than = Node(vtype='GREATER_THAN',
                             children=[self.int_node_one, self.int_node_two])
        walk_ast(int_node_greater_than)
        eq_(int_node_greater_than.syn_value, False)

    def test_int_greater_than_equal(self):
        int_node_greater_than_equal = Node(vtype='GREATER_THAN_EQUAL',
                             children=[self.int_node_one, self.int_node_one])
        walk_ast(int_node_greater_than_equal)
        eq_(int_node_greater_than_equal.syn_value, True)

    def test_ints_equal(self):
        int_node_equal = Node(vtype="EQUAL",
                              children=[self.int_node_one, self.int_node_one])
        walk_ast(int_node_equal)
        eq_(int_node_equal.syn_value, True)

    def test_ints_not_equal(self):
        int_node_not_equal = Node(vtype="NOT_EQUAL",
                                    children=[self.int_node_one, self.int_node_two])
        walk_ast(int_node_not_equal)
        eq_(int_node_not_equal.syn_value, True)

    # Incomparable types
    @raises(TypeError)
    def test_int_float_incomparable_equal(self):
        equal_node = Node(vtype="EQUAL", children=[self.int_node_one, self.float_node_one])
        walk_ast(equal_node)

    @raises(TypeError)
    def test_float_string_incomparable_equal(self):
        equal_node = Node(vtype="EQUAL", children=[self.float_node_one, self.string_node_one])
        walk_ast(equal_node)

    @raises(TypeError)
    def test_float_bool_incomparable_equal(self):
        equal_node = Node(vtype="EQUAL", children=[self.float_node_one, self.bool_node_true])
        walk_ast(equal_node)

    # Boolean operators
    @raises(TypeError)
    def test_boolean_op_and_no_args(self):
        node = Node(vtype="AND", children=[])
        walk_ast(node)

    @raises(TypeError)
    def test_boolean_op_and_one_arg(self):
        node = Node(vtype="AND", children=[self.float_node_one])
        walk_ast(node)

    def test_boolean_op_and(self):
        node = Node(vtype="AND", children=[self.float_node_one, self.int_node_neg_one])
        walk_ast(node)
        eq_(node.syn_value, True)
        node = Node(vtype="AND", children=[self.float_node_one, self.int_node_zero])
        walk_ast(node)
        eq_(node.syn_value, False)

    def test_boolean_op_or(self):
        node = Node(vtype="OR", children=[self.int_node_zero, self.int_node_neg_one])
        walk_ast(node)
        eq_(node.syn_value, True)
        node = Node(vtype="OR", children=[self.int_node_zero, self.int_node_zero])
        walk_ast(node)
        eq_(node.syn_value, False)

    def test_boolean_op_not(self):
        node = Node(vtype='NOT', children=[self.int_node_zero])
        walk_ast(node)
        eq_(node.syn_value, True)
        node = Node(vtype='NOT', children=[self.string_node_empty])
        walk_ast(node)
        eq_(node.syn_value, True)
        node = Node(vtype='NOT', children=[self.float_node_neg_one])
        walk_ast(node)
        eq_(node.syn_value, False)

    def test_assignment(self):
        x_node = Node(vtype="IDENTIFIER", symbol='x')
        val_node = self.int_node_two
        assignment_node = Node(vtype="IDENTIFIER", children=[x_node, val_node])
        walk_ast(assignment_node)
        symbol_record = SCOPES[-1][x_node.symbol]
        eq_(symbol_record[0], val_node.vtype)
        eq_(symbol_record[1], val_node.syn_value)
