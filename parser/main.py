from parser import parser
import sys

def traverse(root):
    traversePost(root, 0)

def traversePost(root, indent): #postorder
    if type(root) is 'str':
        print root, "is a str. oops"

    if(root is not None ):
        for n in root.children:
            traversePost(n, indent+1)
        #print ' '*indent
        #if len(root.children) == 0: #leaf
        print '     '*indent + root.vtype,':',root.syn_value,':',root.symbol,':',root.inh_value
        #else: #non-leaf
        #    print '    '*indent + root.vtype

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
