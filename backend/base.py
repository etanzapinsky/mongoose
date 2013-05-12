from stdlib import assign, list_assign, boolean_ops, equality_ops, first_order_ops, builtins
from stdlib import weighted_value
import vtypes as v
from collections import defaultdict
import copy

class Backend():

    def __init__(self):
        symbols = dict()
        symbols.update(builtins)
        self.scopes = [symbols]
        self.invariants = defaultdict(list)
        self.populate = None
        self.action = None
        self.analysis = None
        self.tick = 1
        self.agent_list = list()

    # this function returns the scope of the symbol requested, practically
    # this means that we cant redefine variables that exist already in the
    # scope. e.g. if we defined `int x` at the global scope, at no more local
    # scope can we redefine `int x`
    def find(self, symbol):
        for scp in reversed(backend.scopes):
            if symbol in scp.keys():
                return scp
        return None

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
            if root.vtype == v.FUNCTION_DEFINITION:
                scope[root.symbol] = root
                # root.syn_value = evaluate_function(f=root, scope=scope,
                #                                    args=[child.syn_value for child in root.children])
            elif root.vtype == v.FUNCTION_CALL:
                scp = backend.find(root.symbol)
                if not scp:
                    raise NameError, "Function '{}' does not exist".format(root.symbol)
                # evaluating expressions passed into function before calling function
                for child in root.children:
                    backend.walk_ast(child)
                func = scp[root.symbol]
                if func.vtype == v.AGENT:
                    agent = copy.deepcopy(func)
                    self.agent_list.append(agent)
                    backend.scopes.append(agent.scope)
                    for st in agent.statements:
                        backend.walk_ast(st)
                    agent.create.execute(*root.children)
                    root.syn_value = agent
                    backend.scopes.pop()
                else:
                    root.syn_value = func.execute(*root.children)
            elif root.vtype == v.RETURN_STATEMENT:
                if root.children:
                    backend.walk_ast(root.children[0])
                    root.syn_value = root.children[0].syn_value
                else:
                    root.syn_value = None
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
            
            # Assignment
            elif root.vtype == v.ASSIGNMENT:
                if root.children[0].vtype == v.IMPLICIT_PARAM:
                    obj = root.children[0].children[0]
                    inner = root.children[0].children[1]
                    scp = backend.find(obj.symbol)
                    val_scp = scp[obj.symbol].scope
                    backend.walk_ast(root.children[1])
                    assign(val_scp, (inner, root.children[1]))
                else:
                    scp = backend.find(root.children[0].symbol)
                    if not scp:
                        raise NameError, "Variable '{}' does not exist".format(root.children[0].symbol)
                    for child in root.children:
                        backend.walk_ast(child)
                    # this should have been disambiguated in the frontend
                    try:  # list assignment
                        grandchild = root.children[0].children[0]
                        assert grandchild.vtype == v.BRACKET_ACCESS
                        depths = grandchild.syn_value
                        list_assign(scp, root.children)
                    except IndexError:  # not a list assignment
                        assign(scp, root.children)  # scopes modified via side effect

            elif root.vtype == v.IDENTIFIER:
                scp = backend.find(root.symbol)
                for kid in root.children:
                    backend.walk_ast(kid)

                # list access
                try:
                    root.children[0].vtype == v.BRACKET_ACCESS
                    # identifier as index
                    iden = root.children[0].children[0]
                    if (iden.vtype == v.IDENTIFIER):
                        backend.walk_ast(iden)
                        root.children[0].syn_value = [iden.syn_value]
                    item = scp[root.symbol].get(indexes=root.children[0].syn_value)
                    root.syn_value = item.syn_value
                    root.syn_vtype = item.syn_vtype
                # simple element access
                except IndexError: # scp[root.symbol]:
                    root.syn_value = scp[root.symbol].syn_value
                    root.syn_vtype = scp[root.symbol].syn_vtype

            # Declaration
            elif root.vtype == v.DECLARATION:
                scp = backend.find(root.symbol)
                if scp:
                    raise Exception, "Symbol '{}' cannot be re-declared".format(root.symbol)
                from parser import Node, List
                # We store different Node types acc. to the root syn_vtype
                if root.syn_vtype == v.LIST_TYPE:
                    depths = root.children[1].depths
                    syn_vtype = root.children[1].syn_vtype
                    none_obj = List(symbol=root.symbol, depths=depths, syn_vtype=syn_vtype)
                elif len(root.children) == 0:  # inside declaration assignment
                    # sorry, this is necessary b/c of wonkiness in the AST:
                    none_obj = Node(symbol=root.symbol, vtype=v.IDENTIFIER, syn_vtype=root.syn_vtype, syn_value=None)
                else:
                    assert len(root.children) > 0
                    identifier = root.children[0]
                    none_obj = Node(symbol=identifier.symbol, vtype=identifier.vtype, syn_vtype=root.syn_vtype, syn_value=None)
                scope[root.symbol] = none_obj

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
                pass
            elif root.vtype == v.AGENT_LIST:
                if root.children:
                    for child in root.children:
                        backend.walk_ast(child)
            elif root.vtype == v.AGENT:
                backend.scopes[-1][root.symbol] = root
            elif root.vtype == v.ENVIRONMENT:
                for child in root.children:
                    backend.walk_ast(child)
            elif root.vtype == v.POPULATE:
                backend.populate = root
            elif root.vtype == v.ACTION:
                backend.action = root
            elif root.vtype == v.TERMINATE:
                if root.children:
                    for child in root.children:
                        backend.walk_ast(child)
            elif root.vtype == v.INVARIANT_CLAUSE:
                freq = root.syn_value
                backend.invariants[freq].append(root)
            elif root.vtype == v.ANALYSIS:
                self.analysis = root
            elif root.vtype == v.WEIGHTED_VALUE_STAT:
                root.syn_value = weighted_value([k.children[0].syn_value for k in root.children ],
                                                [k.children[1] for k in root.children])
            elif root.vtype == v.IMPLICIT_PARAM:
                obj = root.children[0]
                inner = root.children[1]
                scp = backend.find(obj.symbol)
                val_scp = scp[obj.symbol].scope
                val = val_scp[inner.symbol]
                backend.scopes.append(val_scp)
                if inner.vtype == v.FUNCTION_CALL:
                    backend.walk_ast(inner)
                    root.syn_value = inner.syn_value
                else:
                    root.syn_value = val.syn_value
                backend.scopes.pop()
            else:
                pass  # @todo


        return root.syn_value
        # How does this deal with return values? @todo

    def run(self):
        backend.walk_ast(backend.populate.children[0])
        while True:
            backend.walk_ast(backend.action.children[0])
            for agent in self.agent_list:
                backend.scopes.append(agent.scope)
                for child in agent.action.children:
                    backend.walk_ast(child)
                backend.scopes.pop()
            invariants = [i for k,v in backend.invariants.iteritems()
                          if not self.tick % k for i in v]
            if invariants:
                stop = False
                for invariant in invariants:
                    condition = invariant.children[0]
                    statements = invariant.children[1]
                    backend.walk_ast(condition)
                    if condition.syn_value:
                        stop = True
                        backend.walk_ast(statements)
                if stop:
                    backend.walk_ast(backend.analysis.children[0])
                    break
            self.tick += 1

backend = Backend()  # backend is a global singleton variable
