from nose.tools import *
from mongoose import mongoose

# For the stdout hack
from cStringIO import StringIO
import sys

# Dirty hack until we get return values implemented in the backend
def stdout(fn):
    def wrapped():
        backup = sys.stdout  # set up the environment
        sys.stdout = StringIO()  # capture output
        fn()
        out = sys.stdout.getvalue()  # get output
        sys.stdout.close()  # close the stream
        sys.stdout = backup  # restore original stdout
        return out
    return wrapped

@stdout
def _print():
    mongoose.interpret(source=r'_print(\"hello world\")')

# by default our print function will be newline terminated, so have to include
# that in the check
eq_(_print(), 'hello world\n')
