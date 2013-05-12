#!/usr/bin/env python

import sys
from parser import parser
from backend import backend

def main():
    if len(sys.argv) != 2:
        print 'Invalid number of arguments: <mongoose> <mongoose src code>'
        exit(1)
    src = open(sys.argv[1])
    backend.walk_ast(parser.parse(src.read()))
    backend.run()

if __name__ == '__main__':
    main()
