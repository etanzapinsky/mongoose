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

def interpret(source=None, source_path=None):
    if source:
        src = source
    elif source_path:
        # Less space-efficient, but only one return path
        src = open(source, 'r').read()
    return backend.walk_ast(parser.parse(src))

if __name__ == '__main__':
    main()
