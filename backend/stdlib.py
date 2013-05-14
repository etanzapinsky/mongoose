#need this to have the print function work properly in the lambda function
from __future__ import print_function
import vtypes as v
from random import choice

class PrintFunction():
    vtype = 'PRINT'
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

equality_ops = {  v.EQUAL: lambda x, y: x == y,
                  v.NOT_EQUAL: lambda x, y: x != y,
                  }

boolean_ops = {
      v.NOT: lambda x: not x,
      v.AND: lambda x, y: bool(x and y),  # as implemented, and/or operators take any types
      v.OR: lambda x, y: bool(x or y),
}

def _print_scope(scope, when):
  print('Scope {}:'.format(when))
  for k,v in scope.items():
        try:
            print('\t{}: {}'.format(k, v.__str__()))
        except AttributeError, e:
            print('\t{}: {}'.format(k, v))

def list_assign(scope, nodes):
    sym = nodes[0].symbol
    val = nodes[1]
    # _print_scope(scope, "beforelist")
    indexes = nodes[0].children[0].syn_value
    scope[sym].store(val,indexes)  # store() does typechecking
    # _print_scope(scope, "afterlist")

def assign(scope, nodes):
    '''Modifies the scope parameter (side effect!) by inserting the assigned value.
    Example: x = val.'''
    sym = nodes[0].symbol
    val = nodes[1]
    if nodes[0].syn_vtype == v.AGENT_VALUE:
        val = val.syn_value
    # _print_scope(scope, "before")
    scope[sym] = val
    # _print_scope(scope, "after")

def weighted_value(weights, values):
    # total = sum(weights)
    # likelihoods = [ float(weight) / total for weight in weights ]
    # x = random()
    # val = None
    # for like in likelihoods:
    #     if x <= like:
    #         i = likelihoods.index(like)
    #         val = values[i].syn_value
    #         break
    #     x -= like
    # return val
    l = []
    for w, v in zip(weights, values):
        if w:
            l.extend([v]*w)
    return choice(l)
