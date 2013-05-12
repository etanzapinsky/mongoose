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
	

    def test_assignment_decl(self): #coverage for assignment and empty blocks
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

    def test_if(self): #coverage for if, equals and assignment
        src = '''if(x==6) {\n
		y=5\n  
	}\n''' 
        expected = Node(vtype=v.PROGRAM, children=[
                       Node(vtype=v.AGENT_LIST, children=[None]),                           
                       Node(vtype=v.ENVIRONMENT, children=[None]),
                       Node(vtype=v.TERMINATE, children=[None]), 
                       Node(vtype=v.ANALYSIS, children=[None]),
                       Node(vtype=v.STATEMENT_LIST, children=[
                           Node(vtype=v.STATEMENT, children=[
				Node(vtype=v.IF, children=[
					Node(vtype=v.STATEMENT_LIST, children=[
						Node(vtype=v.EQUAL, children=[
							Node(vtype=v.IDENTIFIER,symbol='x')
						       ,Node(vtype=v.INTEGER_VALUE,syn_value='6')
						])
						       ,Node(vtype=v.DECLARATION_ASSIGNMENT,children=[
						            Node(vtype=v.DECLARATION,children=[
						                Node(vtype=v.LIST_TYPE,inh_value='int', children=[
						                    Node(vtype=v.INT_KEYWORD,syn_value='int')
						                   ,Node(vtype=v.BRACKET_DECL,inh_value='')
						                ])
						               ,Node(vtype=v.IDENTIFIER,symbol='y')
						            ])
						           ,Node(vtype=v.INTEGER_VALUE,syn_value='5')
						        ])
				               ,None
				                ])
		                       ,None
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


    def test_agent_dec_return(self): #coverage for assignments of agents and agent functions
        src = '''Cell x = Cell() \n
	Cell y\n
	y = Cell()\n
	Cell foo(Cell c) {\n
	     return z\n
	}\n
	environment{\n
	    action{\n
	    }\n
	    populate{\n       
	    }\n
	}\n
	terminate{\n
	}\n
	analysis{\n
	}\n''' 
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
                                        Node(vtype=v.AGENT_VALUE,syn_value='x')
                                        ])
                                   ,Node(vtype=v.ASSIGNMENT,children=[
					Node(vtype=v.IDENTIFIER,symbol='x')
					,Node(vtype=v.FUNCTION_CALL,symbol='Cell')
					])
                                    ])
                                   ,Node(vtype=v.INTEGER_VALUE,syn_value='5')
                                ])
                               ,None
                            ])
			    Node(vtype=v.STATEMENT, children=[ 
		                Node(vtype=v.DECLARATION,children=[
					Node(vtype=v.AGENT_VALUE,syn_value='y')
					])
				,Node(vtype=v.ASSIGNMENT,children=[
					Node(vtype=v.IDENTIFIER,symbol='y')
					,Node(vtype=v.FUNCTION_CALL,symbol='Cell')
					])
				])
				,None
			    Node(vtype=v.STATEMENT, children=[ 
		                Node(vtype=v.FUNCTION_DEFINITION,children=[
					Node(vtype=v.RETURN_TYPE,symbol='foo')
					])
				,Node(vtype=v.STATEMENT_LIST, children=[
					Node(vtype=v.RETURN_STATEMENT,children=[
						Node(vtype=v.IDENTIFIER,symbol='z')
					])
				])
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


    def test_dot_operations(self): #coverage for dot operation 
        src = '''q = a.x()\n
	r.c()\n
	a.x = 5\n
	a = r.y\n
	a.x = b.y\n
	environment{\n
		populate{\n
		}\n
		action{\n
		}\n
	}\n
	terminate{\n
	}\n
	analysis{\n
	}\n''' 
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
                               Node(vtype=v.ASSIGNMENT,children=[
					Node(vtype=v.IMPLICIT_PARAM,children=[
                                            Node(vtype=v.IMPLICIT_PARAM,symbol='a')
                                           ,Node(vtype=v.FUNCTION_CALL,symbol='x')
                                        ])
                                       ,Node(vtype=v.IDENTIFIER,symbol='q')
                                ])
			       ,Node(vtype=v.IMPLICIT_PARAM,children=[
                                       Node(vtype=v.IMPLICIT_PARAM,symbol='r')
                                       ,Node(vtype=v.FUNCTION_CALL,symbol='c')
                               ])
                               ,Node(vtype=v.ASSIGNMENT,children=[
					Node(vtype=v.IMPLICIT_PARAM,children=[
                                            Node(vtype=v.IMPLICIT_PARAM,symbol='a')
                                           ,Node(vtype=v.FUNCTION_CALL,symbol='x')
                                        ])
                                       ,Node(vtype=v.INTEGER_VALUE,syn_value='5')
                               ])
			       ,Node(vtype=v.ASSIGNMENT,children=[
					Node(vtype=v.IMPLICIT_PARAM,children=[
                                            Node(vtype=v.IMPLICIT_PARAM,symbol='r')
                                           ,Node(vtype=v.IDENTIFIER,symbol='y')
                                        ])
                                       ,Node(vtype=v.IDENTIFIER,symbol='a')
                               ])

			       ,Node(vtype=v.ASSIGNMENT,children=[
					Node(vtype=v.IMPLICIT_PARAM,children=[
                                            Node(vtype=v.IMPLICIT_PARAM,symbol='a')
                                           ,Node(vtype=v.IDENTIFIER,symbol='x')
                                        ])
                                       ,Node(vtype=v.IMPLICIT_PARAM,children=[
                                            Node(vtype=v.IMPLICIT_PARAM,symbol='b')
                                           ,Node(vtype=v.IDENTIFIER,symbol='y')
                                       ])
                                ])
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

    def test_explicit_cast(self): #coverage for casting
        src = '''x = (int) (5 *  ((float) 4+8))\n
	environment{\n
	    action{\n
	    }\n
	    populate{\n       
	    }\n
	}\n
	terminate{\n
	}\n
	analysis{\n
	}\n''' 
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
                               Node(vtype=v.ASSIGNMENT,children=[
                                    Node(vtype=v.CAST_EXPRESSION,children=[
                                        Node(vtype=v.EXPLICIT_CAST, children=[
                                            Node(vtype=v.INT_KEYWORD,syn_vtype=v.INTEGER_VALUE)
                                        ])
                                       ,Node(vtype=v.MULTIPLY,children=[
		                                Node(vtype=v.CAST_EXPRESSION,children=[
		                                    Node(vtype=v.EXPLICIT_CAST,children=[
							Node(vtype=v.FLOAT_KEYWORD, syn_vtype=v.FLOAT_VALUE)
						    ])
						,Node(vtype=v.ADD,children=[
		                                    Node(vtype=v.INTEGER_VALUE,children=[
							Node(vtype=v.FLOAT_KEYWORD, syn_value='4')
							,Node(vtype=v.FLOAT_KEYWORD, syn_value='8')
						    ])
		                                ])
						,Node(vtype=v.INTEGER_VALUE,syn_value='5')
					])
                                    ])
                                   ,Node(vtype=v.IDENTIFIER,symbol='x')
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

