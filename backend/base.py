from stdlib import boolean_ops, equality_ops, first_order_ops

# example symbol table entry: (type, value)
SYMBOLS = dict()
SCOPES = [SYMBOLS]  # Use append() and pop()

def walk_ast(root):
    # this is obviously not extentable since the content of an arg for a function
    # can be an arbitrary expression, this is just to get something working
    # ---
    # Another issue is that this won't work recursively --> we have to think a
    # little bit more about how we should recursively evaulate this function
    # what should it return / how should it interact with syn_value
    # ---
    if root.vtype == 'FUNCTION':
        root.syn_value(*[child.syn_value for child in root.children])
    elif root.vtype in first_order_ops:
        root.syn_value = first_order_ops[root.vtype](*[child.syn_value for child in root.children])
    elif root.vtype in boolean_ops:
        root.syn_value = boolean_ops[root.vtype](*[child.syn_value for child in root.children])
    elif root.vtype in equality_ops:
        root.syn_value = equality_ops[root.vtype](*root.children)  # does this break for len(root.children) > 2?
    elif root.vtype == 'ASSIGNMENT':
        root.syn_value = assignment(*root.children)
    elif root.vtype == 'IDENTIFIER':
        pass

    # How does this deal with return values? @todo


# should this be located elsewhere? @todo #FIXME
# I put it here so it could access SYMBOLS without any parameter passing
def assignment(*nodes):
    '''Stores the assigned value in the top symbol table on the scope stack. 
    Example: x = val.'''
    global SCOPES

    x = nodes[0]
    val = nodes[1] 
    SCOPES[-1][x.symbol] = (val.vtype, val.syn_value)