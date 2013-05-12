from parser.tree import List, Node
import vtypes as v

def test_access_list():
    index = (1,0,1)
    value = Node(vtype=v.INTEGER_VALUE, syn_value=42)
    l = List(symbol='x', depths=[2,2,2], syn_vtype=v.INTEGER_VALUE)
    assert l.data == [0 for i in range(8)]

    # test storage and retrieval
    l.store(value, index)
    stored_value = l.get(index)
    assert value == stored_value

    # test print string
    expected_values = [0 for i in range(8)]
    expected_values[5] = value.syn_value
    expected_print_string = '<<INTEGER_VALUE> list: dimensions={} values={}>'.format([2,2,2], expected_values)
    print l.__str__()
    print expected_print_string
    assert l.__str__() == expected_print_string

