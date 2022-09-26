import encoder
import mutator
from mutator import split_complex_links, renumber_vertices


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
    assert machine.start_idx == {'0', }
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
    assert machine.start_idx == {'0', }
    assert machine.end_idx == {'1', }
    assert len(machine.nodes) == 3
    assert len(machine.nodes['0'].transitions) == 1
    assert machine.nodes['0'].transitions['a'] == {'1', 2, }
    assert len(machine.nodes['1'].transitions) == 0
    assert len(machine.nodes[2].transitions) == 1
    assert machine.nodes[2].transitions['b'] == {'1', }


def test_renumber_vertices():
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
    machine = renumber_vertices(machine)
    assert machine.start_idx == {0, }
    assert machine.end_idx == {1, }
    assert len(machine.nodes) == 3
    assert len(machine.nodes[0].transitions) == 1
    assert machine.nodes[0].transitions['a'] == {1, 2, }
    assert len(machine.nodes[1].transitions) == 0
    assert len(machine.nodes[2].transitions) == 1
    assert machine.nodes[2].transitions['b'] == {1, }


def test_full_determine():
    data = """DOA: v1
Start: 6
Acceptance: 2 & 5
--BEGIN--
State: 0
    ->  2
State: 1
    -> a 0
State: 2
    ->  1
State: 3
    ->  5
State: 4
    -> b 3
State: 5
    ->  4
State: 6
    ->  2
    ->  5
--END--
"""
    machine = encoder.decode(data)
    alpha = {'a', 'b'}
    machine = mutator.full_determine(machine, alpha)
    machine = renumber_vertices(machine)
    assert machine.start_idx == {0, }
    assert machine.end_idx == {0, 1, 2}
    assert len(machine.nodes) == 4
    for node in machine.nodes.values():
        assert len(node.transitions) == len(alpha)
    assert (machine.nodes[0].transitions['b'] == {1, }
            and machine.nodes[1].transitions['a'] == {3, }
            and machine.nodes[1].transitions['b'] == {1, }
            and machine.nodes[0].transitions['a'] == {2, }
            and machine.nodes[2].transitions['b'] == {3, }
            and machine.nodes[2].transitions['a'] == {2, }) \
           or (machine.nodes[0].transitions['a'] == {1, }
               and machine.nodes[1].transitions['b'] == {3, }
               and machine.nodes[1].transitions['a'] == {1, }
               and machine.nodes[0].transitions['b'] == {2, }
               and machine.nodes[2].transitions['a'] == {3, }
               and machine.nodes[2].transitions['b'] == {2, })
    assert machine.nodes[3].transitions['a'] == {3, }
    assert machine.nodes[3].transitions['b'] == {3, }


def test_minimise_and_determine():
    data = """DOA: v1
Start: 0
Acceptance: 3
--BEGIN--
State: 0
    -> a 1
    -> a 2
    -> b 2
State: 1
    -> a 2
    -> b 3
State: 2
    -> a 1
    -> a 2
    -> b 3
--END--
"""
    machine = encoder.decode(data)
    alpha = {'a', 'b'}
    machine = mutator.minimize_and_determine(machine, alpha)
    assert machine.start_idx == {0, }
    assert machine.end_idx == {2, }
    assert len(machine.nodes) == 4
    for node in machine.nodes.values():
        assert len(node.transitions) == len(alpha)
    assert machine.nodes[0].transitions['a'] == {1, }
    assert machine.nodes[0].transitions['b'] == {1, }
    assert machine.nodes[1].transitions['a'] == {1, }
    assert machine.nodes[1].transitions['b'] == {2, }
    assert machine.nodes[2].transitions['a'] == {3, }
    assert machine.nodes[2].transitions['b'] == {3, }
    assert machine.nodes[3].transitions['a'] == {3, }
    assert machine.nodes[3].transitions['b'] == {3, }
