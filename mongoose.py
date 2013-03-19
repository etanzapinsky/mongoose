import sys

from simple_yacc import parser
from simple_backend import walk_ast

def main():
    if len(sys.argv) != 2:
        print 'Invalid number of arguments: <./mongoose.py> <mongoose src code>'
        exit(1)
    src = open(sys.argv[1])
    walk_ast(parser.parse(src.read()))

if __name__ == '__main__':
    main()
