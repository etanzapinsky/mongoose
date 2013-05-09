import vtypes as v
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
        if self.syn_value:
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
    def __init__(self, return_type, symbol, parameter_pairs, statements):
        '''Called when a function is defined.
        vtype checking is done in the frontend (parser)'''
        Node.__init__(self, vtype=v.FUNCTION_DEFINITION)
        self.return_type = return_type
        self.symbol = symbol
        self.statements = Node(vtype=v.STATEMENT_LIST, children=[statements])
        self.parameter_pairs = parameter_pairs

    def execute(self, *args):
        backend.scopes.append(self._bind_params(*args))
        r = backend.walk_ast(self.statements)
        backend.scopes.pop()
        return r

    def _bind_params(self, *args):
        bindings = {}
        if len(args) != len(self.parameter_pairs):
            raise Exception, "InvalidParameters (incorrect number of parameters)"

        # typechecking
        for arg, (id_node, vtype) in zip(args, self.parameter_pairs):
            if arg.vtype != vtype:
                raise TypeError, "Invalid parameter type"
            bindings[id_node.symbol] = arg
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
                        ) 

        else:
            self_comp = bool(self.return_type == other.return_type
                        and self.parameter_pairs == other.parameter_pairs
                        and self.symbol == other.symbol
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
        return '{} {} {}'.format(super.__str__(), rt, pp)
