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

def test_comments():
    expected = ''
    output = run('sample_code/working/comments.mon')
    assert output == expected

def test_return_statements():
    expected = '''add_ten: 20
concat: hi there!
bar: None
'''
    output = run('sample_code/working/return_statements.mon')
    assert output == expected

def test_weighted_value():
    weights = (1, 3, 7)
    values = (5, 4, 8)
    total = sum(weights)
    likelihoods = ( float(weight) / total for weight in weights )
    expectation = sum(( like * val for like, val in zip(likelihoods, values)))

    num_tests = 50
    num_total = 0
    bin_total = 0
    for i in range(num_tests):
        output = run('sample_code/working/weighted_value.mon')
        output = output.split('\n')
        num = int(output[0])
        bin = int(output[1])
        num_total += num
        bin_total += bin

    avg_value = num_total / num_tests
    epsilon = abs(expectation - avg_value) / expectation
    assert epsilon < 0.5
    epsilon = abs((num_tests / 2) - bin_total) / (num_tests / 2)
    assert epsilon < 0.5

def test_environment_terminate():
    expected = '''I print on populate
I print on action
I print on action
I print on action
I print on action
I should print on turn 4
'''
    output = run('sample_code/working/environment_terminate.mon')
    assert output == expected

def test_analysis():
    expected = 'I am being analyzed!\n'
    output = run('sample_code/working/analysis.mon')
    assert output == expected

def test_list_parameter_call():
    expected = '12\n'
    output = run('sample_code/working/list_parameter_call.mon')
    assert output == expected

def test_most_agent_things():
    expected = '''On create A
On create B
On create B
a.x: 1
b.n: 3
c.n: 10
hi
5
six: 6
done
'''
    output = run('sample_code/working/agent.mon')
    assert output == expected

def test_one_agent_turn():
    expected = '''On create A
a.x: 1
a.x: 2
a.x: 3
a.x: 4
done
'''
    output = run('sample_code/working/agent_turn.mon')
    assert output == expected

def test_multiple_agents():
    expected = '''On create A
On create B
one.x: 1
two.x: 2
one.x: 2
two.x: 3
one.x: 3
two.x: 4
done
'''
    output = run('sample_code/working/multiple_agents.mon')
    assert output == expected
