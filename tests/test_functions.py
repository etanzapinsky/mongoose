import unittest
import vtypes as v
from nose.tools import *
from parser import Node, Function
from backend import Backend
from backend.stdlib import first_order_ops

class FunctionsTests(unittest.TestCase):
    @classmethod
    def setup_class(self):
        # Constants
        self.int_node_one = Node(vtype=v.INTEGER_VALUE, syn_value=1)
        self.int_node_two = Node(vtype=v.INTEGER_VALUE, syn_value=2)
        self.int_node_three = Node(vtype=v.INTEGER_VALUE, syn_value=3)

        # Variables
        self.x = Node(vtype=v.IDENTIFIER, symbol='x')
        self.y = Node(vtype=v.IDENTIFIER, symbol='y')
        self.z = Node(vtype=v.IDENTIFIER, symbol='z')

        # z = x + y
        self.int_node_add = Node(vtype=v.ADD, children=(self.x, self.y))
        self.assignment_node = Node(vtype=v.ASSIGNMENT, children=[self.z, self.int_node_add])

        # Functions
        self.sum_function = Function(return_type=v.INTEGER_VALUE,
                                     parameter_pairs=((self.x, v.INTEGER_VALUE),
                                                      (self.y, v.INTEGER_VALUE)),
                                     expressions=[self.assignment_node,])

        self.backend = Backend()
        

    def test_bind_params(self):
        self.sum_function._bind_params(self.int_node_one, self.int_node_two)
        assert self.sum_function.bindings['x'] == self.int_node_one

    def test_scopeless_add(self):
        scopeless_add_node = Node(vtype=v.ADD, children=(self.int_node_one, self.int_node_two))
        scopeless_add_function = Function(return_type=v.INTEGER_VALUE,
                                               parameter_pairs=(),
                                               expressions=[scopeless_add_node,])
        scopeless_add_function.execute()

    @nottest
    def test_execute_statement_without_scope(self):
        self.sum_function.execute(self.int_node_one, self.int_node_two)
        assert self.scope
        assert self.sum_function.bindings['z'] == self.int_node_three
        # assert self.sum_function.syn_value == self.int_node_three