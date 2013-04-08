def walk_ast(root):
    # this is obviously not extentable since the content of an arg for a function
    # can be an arbitrary expression, this is just to get something working
    if root.vtype == 'FUNCTION':
        root.syn_value(*[child.syn_value for child in root.children])
        
    # How does this deal with return values? @todo
