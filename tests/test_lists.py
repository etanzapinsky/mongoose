from parser.tree import List
import vtypes as v

def test_access_list():
    index = (1,0,1)
    value = 42
    l = List(symbol='x', depths=[2,2,2], syn_vtype=v.INTEGER_VALUE)
    assert l.data == [None for i in range(8)]
    l.store(value, index)
    stored_value = l.get(index)
    assert value == stored_value