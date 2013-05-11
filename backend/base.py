from stdlib import assign, boolean_ops, equality_ops, first_order_ops, builtins
import vtypes as v

class Backend():

    def __init__(self):
        symbols = dict()
        symbols.update(builtins)
        self.scopes = [symbols]

    def walk_ast(self, root, siblings=None, parent=None):

        # this function returns the scope of the symbol requested, practically
        # this means that we cant redefine variables that exist already in the
        # scope. e.g. if we defined `int x` at the global scope, at no more local
        # scope can we redefine `int x`
        def find(symbol):
            for scp in reversed(backend.scopes):
                if symbol in scp.keys():
                    return scp
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
                scp = find(root.symbol)
                if not scp:
                    raise NameError, "Function '{}' does not exist".format(root.symbol)
                # evaluating expressions passed into function before calling function
                for child in root.children:
                    backend.walk_ast(child)
                root.syn_value = scp[root.symbol].execute(*root.children)
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
                scp = find(root.children[0].symbol)
                if not scp:
                    raise NameError, "Variable '{}' does not exist".format(root.symbol)
                for child in root.children:
                    backend.walk_ast(child)
                assign(scp, root.children)  # scopes modified via side effect
            elif root.vtype == v.IDENTIFIER:
                scp = find(root.symbol)
                if scp[root.symbol]:
                    root.syn_value = scp[root.symbol].syn_value
                    root.syn_vtype = scp[root.symbol].syn_vtype
            elif root.vtype == v.DECLARATION:
                scp = find(root.symbol)
                if scp:
                    raise Exception, "Symbol '{}' cannot be re-declared".format(root.symbol)
                scope[root.symbol] = None
            elif root.vtype == v.DECLARATION_ASSIGNMENT:
                for child in root.children:
                    backend.walk_ast(child)
            elif root.vtype == v.IF:
                root.execute_if()
            elif root.vtype == v.PIF:
                root.execute_pif()
            elif root.vtype == v.WHILE:
                root.execute_while()
            elif root.vtype == v.REPEAT:
                root.execute_repeat()
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
