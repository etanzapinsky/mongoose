#need this to have the print function work properly in the lambda function
from __future__ import print_function

builtins = {'_print': lambda x: print(x)}
