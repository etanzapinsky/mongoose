from nose.tools import *
import subprocess

def run(path):
    cmd = ['sh', 'manage.sh', 'mongoose.py', path]
    output = subprocess.check_output(cmd)
    print output
    return output

def test_declarations_assignment_mon():
    expected = '''7
3
3
'''
    output = run('sample_code/working/declarations_assignments.mon')
    assert output == expected


def test_print_mon():
    expected = '''hello world!
x: 10
y: 10
sum: 20
x + y: 20
'''
    output = run('sample_code/working/print.mon')
    assert output == expected

def test_list_declaration_and_access_mon():
    expected = '''1
'''
    output = run('sample_code/working/list_declaration_and_access.mon')
    assert output == expected

def test_simple_assignment_mon():
    expected = '''3
4
'''
    output = run('sample_code/working/simple_assignment.mon')
    assert output == expected

def test_simple_function_call_mon():
    expected = '''20
40
105
300
'''
    output = run('sample_code/working/simple_function_call.mon')
    assert output == expected