import vtypes as v
from backend import backend

class Node:
    def __init__(self, vtype, symbol=None, inh_value=None, syn_value=None, children=[]):
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
            return bool(self.inh_value == other.inh_value and
                        self.syn_value == other.syn_value and
                        self.symbol == other.symbol ) 

        else:
            self_comp = bool(self.inh_value == other.inh_value and
                             self.syn_value == other.syn_value and
                             self.symbol == other.symbol )
            return self_comp and all([self_c == other_c for self_c, other_c in
                                  zip(self.children, other.children)])

    # Useful for debugging
    def __str__(self):
        return '[Node: {sym} {vtype}, {inh_val}, {syn_val}, {kids}]'.format(sym=self.symbol,
                                                                            vtype=self.vtype,
                                                                            inh_val=self.inh_value,
                                                                            syn_val=self.syn_value,
                                                                            kids=self.children)


class Function(Node):
    def __init__(self, return_type, symbol, parameter_pairs, statements):
        '''Called when a function is defined.
        vtype checking is done in the frontend (parser)'''
        Node.__init__(self, vtype=v.FUNCTION)
        self.return_type = return_type
        self.symbol = symbol
        self.statements = Node(vtype=v.STATEMENT_LIST, children=statements)
        self.parameter_pairs = parameter_pairs

    def execute(self, *args):
        backend.scopes.append(self._bind_params(*args))
        r = backend.walk_ast(self.statements)
        backend.scopes.pop()

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
