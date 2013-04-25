import unittest
import vtypes as v
from nose.tools import *
from parser import Node, Function
from backend import backend
from backend.stdlib import first_order_ops

class ScopeTests(unittest.TestCase):
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