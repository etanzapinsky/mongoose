import unittest

from nose.tools import *
from parser import Node
from backend import walk_ast
from backend.stdlib import first_order_ops


def setup(self):
    self.int_node_one = Node(vtype='INT', syn_value=1)
    self.int_node_two = Node(vtype='INT', syn_value=2)
    self.int_node_neg_one = Node(vtype='INT', syn_value=-1)
    self.float_node_one = Node(vtype='FLOAT', syn_value=1.0)
    self.float_node_two = Node(vtype='FLOAT', syn_value=2.0)
    self.float_node_neg_one = Node(vtype='FLOAT', syn_value=-1.0)
    self.string_node_one = Node(vtype='STRING', syn_value='1')
    self.bool_node_true = Node(vtype='BOOLEAN', syn_value=True)
    self.bool_node_false = Node(vtype='BOOLEAN', syn_value=False)
    self.none_node = Node(vtype='NONE', syn_value=None)
    return self

class BackendTests(unittest.TestCase):
    @classmethod
    def setup_class(self):
        self = setup(self)

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


class EqualityOperatorBackendTests(unittest.TestCase):
    @classmethod
    def setup_class(self):
        self = setup(self)

    # self.int_node_one = Node(vtype='INT', syn_value=1)
    # self.int_node_two = Node(vtype='INT', syn_value=2)
    # self.int_node_neg_one = Node(vtype='INT', syn_value=-1)
    # self.float_node_one = Node(vtype='FLOAT', syn_value=1.0)
    # self.float_node_two = Node(vtype='FLOAT', syn_value=2.0)
    # self.float_node_neg_one = Node(vtype='FLOAT', syn_value=-1.0)
    # self.string_node_one = Node(vtype='STRING', syn_value='1')
    # self.bool_node_true = Node(vtype='BOOLEAN', syn_value=True)
    # self.bool_node_false = Node(vtype='BOOLEAN', syn_value=False)
    # self.none_node = Node(vtype='NONE', syn_value=None)

    def test_int_equal(self):
        int_node_equal = Node(vtype="EQUAL",
                              children=[self.int_node_one, self.int_node_one])
        walk_ast(int_node_equal)
        eq_(int_node_equal.syn_value, True)

    def test_int_not_equal(self):
        int_node_not_equal = Node(vtype="NOT_EQUAL",
                              children=[self.int_node_one, self.int_node_two])
        walk_ast(int_node_not_equal)
        eq_(int_node_not_equal.syn_value, True)

