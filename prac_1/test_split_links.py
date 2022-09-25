import encoder
from mutator import split_complex_links


def test_simple_split():
    data = """DOA: v1
Start: 0
Acceptance: 1
--BEGIN--
State: 0
    -> ab 1
--END--
"""
    machine = encoder.decode(data)
    machine = split_complex_links(machine)
    assert machine.start_idx == '0'
    assert machine.end_idx == {'1', }
    assert len(machine.nodes) == 3
    assert len(machine.nodes['0'].transitions) == 1
    assert machine.nodes['0'].transitions['a'] == {2, }
    assert len(machine.nodes['1'].transitions) == 0
    assert len(machine.nodes[2].transitions) == 1
    assert machine.nodes[2].transitions['b'] == {'1', }


def test_merging_split():
    data = """DOA: v1
Start: 0
Acceptance: 1
--BEGIN--
State: 0
    -> a 1
    -> ab 1
--END--
"""
    machine = encoder.decode(data)
    machine = split_complex_links(machine)
    assert machine.start_idx == '0'
    assert machine.end_idx == {'1', }
    assert len(machine.nodes) == 3
    assert len(machine.nodes['0'].transitions) == 1
    assert machine.nodes['0'].transitions['a'] == {'1', 2, }
    assert len(machine.nodes['1'].transitions) == 0
    assert len(machine.nodes[2].transitions) == 1
    assert machine.nodes[2].transitions['b'] == {'1', }
