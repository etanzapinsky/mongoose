import random
import vtypes as v
from default_values import default_values
from backend import backend

class Node:
    def __init__(self, vtype, symbol=None, inh_value=None, syn_value=None, children=[], 
                 syn_vtype=None, depths=None):
        """
        @param vtype: str
        @param symbol: str
        @param inh_value: <anything>
        @param syn_value: <anything>
        @param children: list(Node)
        """
        self.symbol = symbol
        self.vtype = vtype
        self.inh_value = inh_value
        self.syn_value = syn_value
        self.children = children
        self.depths = depths
        self.syn_vtype = syn_vtype
    
    # Useful for testing 
    def __eq__(self, other):

        if (self is  None and other is not None) or (self is not None and other is None): 
            return False               

        if self is None and other is None:
            return True

        if self.vtype != other.vtype:
            # We're currently just raising a python error #FIXME @todo
            raise TypeError, "'{}' is not comparable with '{}'".format(self.vtype, other.vtype)

# @todo #FIXME expanding IDENTIFIER (so we can say x == 32)

        if self.children == None:
            return bool(self.inh_value == other.inh_value
                        and self.syn_value == other.syn_value
                        and self.symbol == other.symbol
                        #and self.params == other.params
                        ) 

        else:
            self_comp = bool(self.inh_value == other.inh_value
                             and self.syn_value == other.syn_value
                             and self.symbol == other.symbol
                             #and self.params == other.params
                             )
            return self_comp and all([self_c == other_c for self_c, other_c in
                                      zip(self.children, other.children)])

    # Useful for debugging
    def __str__(self):
        if self.symbol:
            sym = 'sym={}'.format(self.symbol)
        else:
            sym = ''
        if self.inh_value:
            iv = 'inh_val={}'.format(self.inh_value)
        else:
            iv = ''
        if self.syn_value != None:
            sv = 'syn_val={}'.format(self.syn_value)
        else:
            sv = ''
        if self.syn_vtype:
            svt = 'syn_vtype={}'.format(self.syn_vtype)
        else:
            svt = ''
        if self.depths:
            dep = 'depths={}'.format(self.depths)
        else:
            dep = ''
        return '{}: {} {} {} {} {}'.format(self.vtype, sym, iv, sv, svt, dep)

# **IMPORTANT** the interface specified by function just has to have the
# function execute, this allows us to be able to have print functions or other
# builtin functions that we want to act as functions, but break the nice
# structure of walking the AST of all the children statements
class Function(Node):
    def __init__(self, return_type, symbol, parameter_pairs, statements, return_value):
        '''Called when a function is defined.
        vtype checking is done in the frontend (parser)'''
        Node.__init__(self, vtype=v.FUNCTION_DEFINITION, syn_vtype=return_type)
        self.return_type = return_type
        self.symbol = symbol
        self.statements = statements
        self.parameter_pairs = parameter_pairs
        self.return_value = return_value

    def execute(self, *args):
        backend.scopes.append(self._bind_params(*args))
        backend.walk_ast(self.statements)
        r = backend.walk_ast(self.return_value)
        backend.scopes.pop()
        return r

    def _bind_params(self, *args):
        bindings = {}
        if len(args) != len(self.parameter_pairs):
            raise Exception, "InvalidParameters (incorrect number of parameters)"

        # typechecking - gone!
        for arg, (syn_vtype, symbol) in zip(args, self.parameter_pairs):
            # if arg.syn_vtype != syn_vtype:
            #     raise TypeError, "Invalid parameter of type '{}'".format(arg.syn_vtype)
            if arg.vtype == v.IDENTIFIER:
                bindings[symbol] = backend.find(arg.symbol)[arg.symbol]
            else:
                bindings[symbol] = arg
        return bindings

    def __eq__(self, other):

        if (self is  None and other is not None) or (self is not None and other is None): 
            return False               

        if self is None and other is None:
            return True

        if self.vtype != other.vtype:
            # We're currently just raising a python error #FIXME @todo
            raise TypeError, "'{}' is not comparable with '{}'".format(self.vtype, other.vtype)

            # @todo #FIXME expanding IDENTIFIER (so we can say x == 32)

        if self.statements == None:
            return bool(self.return_type == other.return_type
                        and self.parameter_pairs == other.parameter_pairs
                        and self.symbol == other.symbol
                        and self.return_value == return_value
                        ) 

        else:
            self_comp = bool(self.return_type == other.return_type
                        and self.parameter_pairs == other.parameter_pairs
                        and self.symbol == other.symbol
                        and self.return_value == return_value
                        ) 
            return self_comp and all([self_c == other_c for self_c, other_c in
                                  zip(self.statements, other.statements)])

    def __str__(self):
        if self.return_type:
            rt = 'ret_type={}'.format(self.return_type)
        else:
            rt = ''
        if self.parameter_pairs:
            pp = 'param_pairs={}'.format(self.parameter_pairs)
        else:
            pp = ''
        return '{} sym={} {} {}'.format('FUNCTION DEFINITION:', self.symbol, rt, pp)

from operator import mul
class List(Node):
    def __init__(self, symbol, depths, syn_vtype):
        '''Called when a list is defined.'''
        Node.__init__(self, vtype=v.LIST_TYPE, symbol=symbol, syn_vtype=syn_vtype )
        self.depths = depths

        # Generate the internal list of the correct size
        length = reduce(mul, depths, 1)
        default_value = default_values[syn_vtype]
        self.data = [default_value for i in range(length)]

    def _calc_index(self, indexes):
        r = len(self.data)
        i = 0
        for (d, n) in zip(indexes, self.depths):
            r = r / n
            i += r * d
        return i

    def store(self, value, indexes):
        '''The list stores only the syn_value, but relies upon the syn_vthpe for type checking.'''
        #if value.vtype == self.syn_vtype:
        self.data[self._calc_index(indexes)] = value.syn_value
        #else:
        #    raise TypeError, "Cannot store value of type '{}' in list of type '{}'.".format(value.vtype, self.syn_vtype)
        
    def get(self, indexes):
        return Node(vtype=self.syn_vtype, syn_vtype=self.syn_vtype, syn_value=self.data[self._calc_index(indexes)])

    def __str__(self):
        return "<<{}> list: dimensions={} values={}>".format(self.syn_vtype, self.depths.__str__(), self.data.__str__())

class Conditional(Node):
    def __init__(self, vtype, statements, expression=None, next_conditional=None):
        '''
        Used when creating any type of conditional
        '''
        self.statements = statements
        self.expression = expression
        self.next_conditional = next_conditional
        Node.__init__(self, vtype=vtype)

    def execute_if(self):
        if not self.expression:
            backend.scopes.append({})
            backend.walk_ast(self.statements)
            backend.scopes.pop()
            return

        backend.walk_ast(self.expression)
        if self.expression.syn_value:
            backend.scopes.append({})
            backend.walk_ast(self.statements)
            backend.scopes.pop()
        elif self.next_conditional:
            self.next_conditional.execute_if()

    def execute_pif(self, prob=-1):
        if prob == -1:
            prob = random.uniform(0, 1)

        if not self.expression:
            backend.scopes.append({})
            backend.walk_ast(self.statements)
            backend.scopes.pop()
            return

        if self.expression.syn_value > prob:
            backend.scopes.append({})
            backend.walk_ast(self.statements)
            backend.scopes.pop()
        elif self.next_conditional:
            self.next_conditional.execute_pif(prob - self.expression.syn_value)

    def execute_while(self):
        if not self.expression:
            backend.scopes.append({})
            backend.walk_ast(self.statements)
            backend.scopes.pop()
            return

        backend.walk_ast(self.expression)
        expr = self.expression.syn_value
        while expr:
            backend.scopes.append({})
            backend.walk_ast(self.statements)
            backend.scopes.pop()
            backend.walk_ast(self.expression)
            expr = self.expression.syn_value

    def execute_repeat(self):
        if not self.expression:
            backend.scopes.append({})
            backend.walk_ast(self.statements)
            backend.scopes.pop()
            return

        backend.walk_ast(self.expression)
        if self.expression.syn_vtype != v.INTEGER_VALUE:
            raise TypeError, "Expression in repeat statement has to be of type int"
        for i in xrange(self.expression.syn_value):
            backend.scopes.append({})
            backend.walk_ast(self.statements)
            backend.scopes.pop()

    def __str__(self):
        return '{}:'.format(self.vtype)

class Agent(Node):
    def __init__(self, symbol, statements, create, action, destroy):
        '''
        Called when an agent is defined
        '''
        Node.__init__(self, vtype=v.AGENT, syn_vtype=v.AGENT_VALUE)
        self.symbol = symbol
        self.statements = statements
        self.create = create
        self.action = action
        self.destroy = destroy
        self.scope = {}

    def __str__(self):
        return '{}: sym={}'.format(self.vtype, self.symbol)
