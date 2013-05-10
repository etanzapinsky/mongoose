from stdlib import assign, boolean_ops, equality_ops, first_order_ops, builtins
import vtypes as v

class Backend():

    def __init__(self):
        symbols = dict()
        symbols.update(builtins)
        self.scopes = [symbols]

    def walk_ast(self, root, siblings=None, parent=None):

        def find(symbol):
            for scp in reversed(backend.scopes):
                val = scp.get(symbol)
                if val:
                    return val
            return None
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
            if root.vtype == v.FUNCTION_DEFINITION:
                scope[root.symbol] = root
                # root.syn_value = evaluate_function(f=root, scope=scope,
                #                                    args=[child.syn_value for child in root.children])
            elif root.vtype == v.FUNCTION_CALL:
                func = find(root.symbol)
                if not func:
                    raise NameError, "Function '{}' does not exist".format(root.symbol)
                # evaluating expressions passed into function before calling function
                for child in root.children:
                    backend.walk_ast(child)
                root.syn_value = func.execute(*root.children)
            elif root.vtype in first_order_ops:
                for kid in root.children:
                    backend.walk_ast(kid)
                root.syn_value = first_order_ops[root.vtype](*[child.syn_value for child in root.children])
                root.syn_vtype = root.children[0].syn_vtype
            elif root.vtype in boolean_ops:
                root.syn_value = boolean_ops[root.vtype](*[child.syn_value for child in root.children])
                root.syn_vtype = root.children[0].syn_vtype
            elif root.vtype in equality_ops:
                root.syn_value = equality_ops[root.vtype](*root.children)  # does this break for len(root.children) > 2?
                root.syn_vtype = root.children[0].syn_vtype
            elif root.vtype == v.ASSIGNMENT:
                for child in root.children:
                    backend.walk_ast(child)
                assign(backend.scopes[-1], root.children)  # scopes modified via side effect
            elif root.vtype == v.IDENTIFIER:
                val = find(root.symbol)
                if val:
                    root.syn_value = val.syn_value
                    root.syn_vtype = val.syn_vtype
            elif root.vtype == v.DECLARATION:
                symbols = backend.scopes[-1]
                if root.symbol in symbols.keys():
                    raise Exception, "Symbol '{}' cannot be re-declared".format(root.symbol)
                else:
                    symbols[root.symbol] = None
            elif root.vtype == v.DECLARATION_ASSIGNMENT:
                for child in root.children:
                    backend.walk_ast(child)
            elif root.vtype == v.IF:
                root.execute()
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
            elif root.vtype == v.BRACKET_ACCESS:
                pass  # @todo
            elif root.vtype == v.AGENT_LIST:
                pass  # @todo
            elif root.vtype == v.ENVIRONMENT:
                pass  # @todo
            elif root.vtype == v.TERMINATE:
                pass  # @todo
            elif root.vtype == v.ANALYSIS:
                pass  # @todo
            else:
                pass  # @todo


        return root.syn_value
        # How does this deal with return values? @todo

backend = Backend()  # backend is a global singleton variable
