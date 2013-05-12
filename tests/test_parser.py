import vtypes as v
import unittest
from copy import deepcopy
from nose.tools import *
from parser import Node, parser
#from test_lexer import LexerTests
from lexer import lexer

# We should fill these out to increase code coverage. @todo (bo)
# See https://nose.readthedocs.org/en/latest/
# Also see: https://nose.readthedocs.org/en/latest/testing_tools.html

# all of these tests are failing since it's obviously not valid to just do
# "hello" @captainbox22

@nottest  # broken test
class ParserTests(unittest.TestCase):
    @classmethod                                                                                                                   
    def setup_class(self):
        pass

    @nottest
    def test_print_node():
        eq_(parser.parse(r'"hello"').__str__(),'[Node: None STRING, None, hello, []]')
	

    def test_assignment_decl(self):
        src = '''int x = 5\n
        environment{\n 
                populate{\n
                }\n
                action{\n
                }\n
        }\n
        terminate{\n
        }\n
        analysis{\n
        }''' # "int x = 5"
        expected = Node(vtype=v.PROGRAM, children=[
                       Node(vtype=v.AGENT_LIST, children=[None]),                           
                       Node(vtype=v.ENVIRONMENT, children=[
                           Node(vtype=v.POPULATE, children=[
                               Node(vtype=v.STATEMENT_LIST, children=[None])
                           ]),
                           Node(vtype=v.ACTION, children=[
                               Node(vtype=v.STATEMENT_LIST, children=[None])
                           ]),
                           Node(vtype=v.STATEMENT_LIST, children=[None]),
                           Node(vtype=v.STATEMENT_LIST, children=[None]),
                           Node(vtype=v.STATEMENT_LIST, children=[None])
                       ]),
                       Node(vtype=v.TERMINATE, children=[None]), 
                       Node(vtype=v.ANALYSIS, children=[
                           Node(vtype=v.STATEMENT_LIST, children=[None])
                       ]),
                       Node(vtype=v.STATEMENT_LIST, children=[
                           Node(vtype=v.STATEMENT, children=[
                               Node(vtype=v.DECLARATION_ASSIGNMENT,children=[
                                    Node(vtype=v.DECLARATION,children=[
                                        Node(vtype=v.LIST_TYPE,inh_value='int', children=[
                                            Node(vtype=v.INT_KEYWORD,syn_value='int')
                                           ,Node(vtype=v.BRACKET_DECL,inh_value='')
                                        ])
                                       ,Node(vtype=v.IDENTIFIER,symbol='x')
                                    ])
                                   ,Node(vtype=v.INTEGER_VALUE,syn_value='5')
                                ])
                               ,None

                            ])
                           ,None
                        ]),
                        Node(vtype=v.STATEMENT_LIST, children=[None]),
                        Node(vtype=v.STATEMENT_LIST, children=[None]),
                        Node(vtype=v.STATEMENT_LIST, children=[None]),
                        Node(vtype=v.STATEMENT_LIST, children=[None])
                    ])    
        
        result = parser.parse(src)
        assert isinstance(result,Node)
        assert isinstance(expected,Node) 
        print result.__str__()
        print expected.__str__()
        assert result == expected


#    @nottest
#    def test_if(self):
#	src = "if(x==6) { \n y=5 \n } \n"
#	result = parser.parse(src) #have this
#	expected = Node(vtype=v.STATEMENT_LIST, children=[
#			Node(vtype.STATEMENT, children=[
#				Node(v.type=IF, children=[ #hmm
#					Node(vtype.STATEMENT_LIST, children=[
#						Node(vtype.STATEMENT, children=[
#							Node(vtype.ASSIGNMENT, children=[
#								Node(v.type=IDENTIFIER, symbol ='y'	
 #                                                       	
#	assert result == expected #have this








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

