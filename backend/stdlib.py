#need this to have the print function work properly in the lambda function
from __future__ import print_function
import vtypes as v

class PrintFunction():
    @classmethod
    def execute(self, *args):
        print(*[a.syn_value for a in args])

builtins = {'print': PrintFunction}

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

def assign(scope, nodes):
    '''Modifies the scope parameter (side effect!) by inserting the assigned value.
    Example: x = val.'''
    # print('pre: ', scope)
    sym = nodes[0].symbol
    val = nodes[1]
    try:
        scope[sym] = val
    except KeyError:
        raise 'Variable does not exist'
    # print('post: ', scope)