import unittest
import vtypes as v
from nose.tools import *
from parser import Node, FunctionDefinition
from backend import backend
from backend.stdlib import first_order_ops

class FunctionDefinitionsTests(unittest.TestCase):
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

        # return z
        self.z_statement = Node(vtype=v.STATEMENT, children=[self.z,])
        self.return_node = Node(vtype=v.RETURN_STATEMENT, syn_value=self.z_statement)

        # FunctionDefinitions
        self.sum_function = FunctionDefinition(return_type=v.INTEGER_VALUE,
                                     symbol='sum',
                                     parameter_pairs=((self.x, v.INTEGER_VALUE),
                                                      (self.y, v.INTEGER_VALUE)),
                                     statements=[self.assignment_node])

        self.sum_with_return_function = FunctionDefinition(return_type=v.INTEGER_VALUE,
                                                 symbol='sum_with_return',
                                                 parameter_pairs=((self.x, v.INTEGER_VALUE),
                                                               (self.y, v.INTEGER_VALUE)),
                                                 statements=[self.assignment_node,
                                                          self.return_node,
                                                          ])
        

    def test_bind_params(self):
        local_scope = self.sum_function._bind_params(self.int_node_one, self.int_node_two)
        assert local_scope['x'] == self.int_node_one
        assert local_scope['y'] == self.int_node_two

    def test_scopeless_add(self):
        scopeless_add_node = Node(vtype=v.ADD, children=(self.int_node_one, self.int_node_two))
        scopeless_add_function = FunctionDefinition(return_type=v.INTEGER_VALUE,
                                           symbol="add",
                                           parameter_pairs=(),
                                           statements=[scopeless_add_node,])
        scopeless_add_function.execute()

    def test_execute_sum_function_no_return(self):
        self.sum_function.execute(self.int_node_one, self.int_node_two)
        # assert self.sum_function.syn_value == self.int_node_three

    @nottest
    def test_execute_sum_with_return_function(self):
        self.sum_with_return_function.execute(self.int_node_one, self.int_node_two)
        print self.sum_with_return_function.syn_value
        assert self.sum_with_return_function.syn_value == 3
        assert self.int_node_three.syn_value == 3
