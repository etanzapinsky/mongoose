from stdlib import assign, boolean_ops, equality_ops, first_order_ops
import vtypes as v

class Backend():

    def __init__(self):
        symbols = dict()
        self.scopes = [symbols]

    def walk_ast(self, root, siblings=None, parent=None):

        # not popping b/c we only pop when *destroying* scope
        # (here we are just modifying)
        scope = backend.scopes[-1]

        # this is obviously not extentable since the content of an arg for a function
        # can be an arbitrary expression, this is just to get something working
        # ---
        # Another issue is that this won't work recurssively --> we have to think a
        # little bit more about how we should recursively evaulate this function
        # what should it return / how should it interact with syn_value
        # ---
        
        # Here we're evaluating all the children that are stored in a node before we
        # evaluate the node itself, doing a proper post-order traversal of the nodes.
        # Also, since we are iterating through the nodes of the tree using the 'in'
        # operator, we are doing a L-attributed evaluation as well, letting us get
        # inherited as well as syntysized values.
        # The only issue here is that we have to have some mechanism to know who the
        # children are at out level (and our parent) for the inherited attributes,
        # so we'll probably pass them in.

        if root != None:
            # if root.vtype == v.FUNCTION_DEFINITION:
            #     root.syn_value = evaluate_function(f=root, scope=scope,
            #                                        args=[child.syn_value for child in root.children])
            if root.vtype == v.FUNCTION_CALL:
                find_function(root.symbol).execute(root.children) # look up the function in the scope stack and execute it
            elif root.vtype in first_order_ops:
                for kid in root.children:
                    backend.walk_ast(kid)
                root.syn_value = first_order_ops[root.vtype](*[child.syn_value for child in root.children])
            elif root.vtype in boolean_ops:
                root.syn_value = boolean_ops[root.vtype](*[child.syn_value for child in root.children])
            elif root.vtype in equality_ops:
                root.syn_value = equality_ops[root.vtype](*root.children)  # does this break for len(root.children) > 2?
            elif root.vtype == v.ASSIGNMENT:
                assign(backend.scopes[-1], root.children)  # scopes modified via side effect
            elif root.vtype == v.IDENTIFIER:
                root.syn_value = root.symbol
            elif root.vtype == v.DECLARATION:
                symbols = backend.scopes[-1]
                root.inh_value = root.children[0].inh_value
                root.symbol = root.children[1].symbol
                symbols[root.symbol] = None # can we do this, or do we have a none type?
            elif root.vtype == v.DECLARATION_ASSIGNMENT:
                backend.walk_ast(root.children[0]) # the declaration
                assign(backend.scopes[-1], root.children)
            elif root.vtype == v.PROGRAM:
                for kid in root.children:
                    backend.walk_ast(kid)
            elif root.vtype == v.STATEMENT_LIST:
                for kid in root.children:
                    backend.walk_ast(kid)
            elif root.vtype == v.STATEMENT:
                for kid in root.children:
                    backend.walk_ast(kid)
                # for debugging
                # print root.children, backend.scopes
            elif root.vtype in v.RETURN_STATEMENT:
                root.syn_value = backend.walk_ast(root.children)


def find_function(function_name):
    for scope in sorted(backend.scopes, reverse=True):
        try:
            return scope[function_name]
        except KeyError:
            pass # try the next stack level
    # If we've gotten this far, then function_name isn't in the scope stack
    raise Exception, u'Function "{}" was not found in the scope stack.'.format(function_name)


backend = Backend()  # backend is a global singleton variable