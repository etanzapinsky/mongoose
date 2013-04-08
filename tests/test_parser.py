from copy import deepcopy
from nose.tools import *
from ..parser import Node, parser

# We should fill these out to increase code coverage. @todo (bo)
# See https://nose.readthedocs.org/en/latest/
# Also see: https://nose.readthedocs.org/en/latest/testing_tools.html

def test_print_node():
    eq_(parser.parse(r'"hello"').__str__(),'[Node: STRING, None, hello, []]')

def test_parse_string_literal():
    src = r'"hello"'
    node = Node(vtype='STRING', syn_value='hello')
    eq_(parser.parse(src), node)

# TODO: use setup/teardown properly
def test_equality():
    node_one = Node(vtype='STRING', syn_value='hello')
    node_two = Node(vtype='STRING', syn_value='hello')
    eq_(node_one, node_two)
    node_three = Node(vtype='STRING', syn_value='bye')
    node_one.children = [deepcopy(node_three), deepcopy(node_three)]
    node_two.children = [deepcopy(node_three), deepcopy(node_three)]
    # TODO find nose not equal
    assert node_two != Node(vtype='STRING', syn_value='hello')
    eq_(node_one, node_two)
    node_four = Node(vtype='STRING', children=[deepcopy(node_one)])
    node_five = Node(vtype='STRING', children=[deepcopy(node_two)])
    eq_(node_four, node_five)

