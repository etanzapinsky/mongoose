import unittest

from nose.tools import *
from ..parser import Node
from ..backend import walk_ast
from ..backend.stdlib import first_order_ops

class BackendTests(unittest.TestCase):
    @classmethod
    def setup_class(self):
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

    def test_int_plus(self):
        int_node_plus = Node(vtype='PLUS',
                             children=[self.int_node_one, self.int_node_two])
        walk_ast(int_node_plus)
        eq_(int_node_plus.syn_value, 3)
