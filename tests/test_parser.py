import vtypes as v

from copy import deepcopy
from nose.tools import *
from parser import Node, parser

# We should fill these out to increase code coverage. @todo (bo)
# See https://nose.readthedocs.org/en/latest/
# Also see: https://nose.readthedocs.org/en/latest/testing_tools.html

# all of these tests are failing since it's obviously not valid to just do
# "hello" @captainbox22

@nottest
def test_print_node():
    eq_(parser.parse(r'"hello"').__str__(),'[Node: None STRING, None, hello, []]')

@nottest
def test_parse_string_literal():
    src = r'"hello"'
    node = Node(vtype=v.STRING_VALUE, syn_value='hello')
    print parser.parse(src)
    eq_(parser.parse(src), node)

# TODO: use setup/teardown properly
@nottest
def test_equality():
    node_one = Node(vtype=v.STRING_VALUE, syn_value='hello')
    node_two = Node(vtype=v.STRING_VALUE, syn_value='hello')
    eq_(node_one, node_two)
    node_three = Node(vtype=v.STRING_VALUE, syn_value='bye')
    node_one.children = [deepcopy(node_three), deepcopy(node_three)]
    node_two.children = [deepcopy(node_three), deepcopy(node_three)]
    # TODO find nose not equal
    assert node_two != Node(vtype=v.STRING_VALUE, syn_value='hello')
    eq_(node_one, node_two)
    node_four = Node(vtype=v.STRING_VALUE, children=[deepcopy(node_one)])
    node_five = Node(vtype=v.STRING_VALUE, children=[deepcopy(node_two)])
    eq_(node_four, node_five)

