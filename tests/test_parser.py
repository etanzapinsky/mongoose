from nose.tools import *
from ..parser import Node, parser

# We should fill these out to increase code coverage. @todo (bo)
# See https://nose.readthedocs.org/en/latest/
# Also see: https://nose.readthedocs.org/en/latest/testing_tools.html

def test_print_node():
	eq_(parser.parse(r'"hello"').__str__(),'[Node: STRING, hello, []]')

def test_parse_string_literal():
	src = r'"hello"'
	node = Node(vtype='STRING', value='hello', children=[])
	eq_(parser.parse(src), node)
