#need this to have the print function work properly in the lambda function
from __future__ import print_function

builtins = {'_print': lambda x: print(x)}

first_order_ops = {'ADD': lambda x, y: x + y,
                   'SUBTRACT': lambda x, y: x - y,
                   'MULTIPLY': lambda x, y: x * y,
                   'DIVIDE': lambda x, y: x / y,
                   'POWER': lambda x, y: x ** y,
                   'MODULUS': lambda x, y: x % y,
                   'LESS_THAN': lambda x, y: x < y,
                   'GREATER_THAN': lambda x, y: x > y,
                   'LESS_THAN_EQUAL': lambda x, y: x <= y,
                   'GREATER_THAN_EQUAL': lambda x, y: x >= y,
                   }
