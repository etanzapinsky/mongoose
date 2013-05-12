from parser import parser
import sys
import vtypes as v
from parser import Conditional

def traverse(root):
    traversePost(root, 0)

def traversePost(root, indent): #preorder
    if type(root) is str:
        print root, "is a str. oops"

    if root is not None:
        if root.vtype == v.FUNCTION_DEFINITION:
            #print root.__class__.__name__
            print '     '*indent + root.__str__()#vtype,':',root.return_type,':',root.symbol,':',root.parameter_pairs
            traversePost(root.statements, indent+1)
            traversePost(root.return_value, indent+1)
        elif isinstance(root, Conditional):
            #print root.__class__.__name__
            # print '     '*indent + root.__str__()#vtype,':',root.return_type,':',root.symbol,':',root.parameter_pairs
            # traversePost(root.statements, indent+1)
            print '     '*indent + root.__str__()
            traversePost(root.expression, indent+1)
            traversePost(root.statements, indent+1)
            traversePost(root.next_conditional, indent+1)
        elif root.vtype == v.AGENT:
            print '     '*indent + root.__str__()
            traversePost(root.create, indent+1)
            traversePost(root.action, indent+1)
            traversePost(root.destroy, indent+1)
            for st in root.statements:
                traversePost(st, indent+1)
        else: #regular Node
            print '     '*indent + root.__str__()#vtype,':',root.syn_value,':',root.symbol,':',root.inh_value,':',root.params
            if root.children is not None:
                for n in root.children:
                    traversePost(n, indent+1)

if __name__ == "__main__": 
    #while True:
    #try:
        #s = raw_input('y>>   ')
    s = open(sys.argv[1], 'r')
    #except EOFError:
        #break
    #if not s: continue
    result = parser.parse(s.read())
    print "result is of type", type(result)
    traverse(result)
    print "done"
