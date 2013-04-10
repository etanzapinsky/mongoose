from stdlib import first_order_ops

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
        
    # How does this deal with return values? @todo
