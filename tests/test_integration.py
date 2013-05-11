from nose.tools import *
import subprocess
from collections import defaultdict

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
1
1
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

def test_if_elif_else():
    expected = '''I should print
I should print
I should print
I should print
'''
    output = run('sample_code/working/if_elif_else.mon')
    assert output == expected

def test_pif_pelif_pelse():
    num_tests = 100
    expected = {'x: 3\n': 0.2 * num_tests,
                'y: 7\n': 0.5 * num_tests,
                'b: False\n': 0.3 * num_tests}
    actual = defaultdict(int)
    for i in range(num_tests):
        output = run('sample_code/working/pif_pelif_pelse.mon')
        actual[output] += 1
    for k,v in expected.iteritems():
        epsilon = abs(v - actual[k]) / v
        if epsilon > 0.5:
            print k.strip(), ' epsilon: ', epsilon
            print actual
            assert False
    assert True

def test_while_loop():
    expected = '''0
1
2
3
4
'''
    output = run('sample_code/working/while_loops.mon')
    assert output == expected

def test_while_loop():
    expected = '''0
1
2
3
4
'''
    output = run('sample_code/working/repeat_statement.mon')
    assert output == expected
