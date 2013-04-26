from parser import parser
import sys
import vtypes as v

def traverse(root):
    traversePost(root, 0)

def traversePost(root, indent): #postorder
    if type(root) is str:
        print root, "is a str. oops"

    if(root is not None ):
        if(root.vtype==v.FUNCTION_DEFINITION):
            print '     '*indent + root.__str__()#vtype,':',root.return_type,':',root.symbol,':',root.parameter_pairs
            traversePost(root.statements, indent+1)
        else: #regular Node
            print '     '*indent + root.__str__()#vtype,':',root.syn_value,':',root.symbol,':',root.inh_value,':',root.params
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
