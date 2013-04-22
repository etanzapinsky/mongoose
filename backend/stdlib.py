#need this to have the print function work properly in the lambda function
from __future__ import print_function
import vtypes as v

builtins = {'_print': lambda x: print(x)}

first_order_ops = {v.ADD: lambda x, y: x + y,
                   v.SUBTRACT: lambda x, y: x - y,
                   v.MULTIPLY: lambda x, y: x * y,
                   v.DIVIDE: lambda x, y: x / y,
                   v.POWER: lambda x, y: x ** y,
                   v.MODULUS: lambda x, y: x % y,
                   v.LESS_THAN: lambda x, y: x < y,
                   v.GREATER_THAN: lambda x, y: x > y,
                   v.LESS_THAN_EQUAL: lambda x, y: x <= y,
                   v.GREATER_THAN_EQUAL: lambda x, y: x >= y,
                   }

equality_ops = {  v.EQUAL: lambda x, y: x.__eq__(y),
                  v.NOT_EQUAL: lambda x, y: not x.__eq__(y),
                  }

boolean_ops = {
      v.NOT: lambda x: not x,
      v.AND: lambda x, y: bool(x and y),  # as implemented, and/or operators take any types
      v.OR: lambda x, y: bool(x or y),
}

def assignment(scope, *nodes):
    '''Stores the assigned value in the given scope. 
    Example: x = val.'''
    x = nodes[0]
    value = nodes[1]
    scope[x.symbol] = value