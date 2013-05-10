from nose.tools import *
import subprocess

def run(path):
    cmd = ['sh', 'manage.sh', 'mongoose.py', path]
    output = subprocess.check_output(cmd)
    print output
    return output

def test_declarations_assignment():
    expected = '''7
3
3
'''
    output = run('sample_code/working/declarations_assignments.mon')
    assert output == expected


@nottest
def test_print():
    expected = '''
    '''
    output = run('sample_code/working/print.mon')
    assert output == expected