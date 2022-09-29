import encoder
import mutator
from mutator import split_complex_links, renumber_states


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
    assert machine.start_idx == {0, }
    assert machine.end_idx == {1, }
    assert len(machine.states) == 3
    assert len(machine.states[0].links) == 1
    assert machine.states[0].links['a'] == {2, }
    assert len(machine.states[1].links) == 0
    assert len(machine.states[2].links) == 1
    assert machine.states[2].links['b'] == {1, }


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
    assert machine.start_idx == {0, }
    assert machine.end_idx == {1, }
    assert len(machine.states) == 3
    assert len(machine.states[0].links) == 1
    assert machine.states[0].links['a'] == {1, 2, }
    assert len(machine.states[1].links) == 0
    assert len(machine.states[2].links) == 1
    assert machine.states[2].links['b'] == {1, }


def test_renumber_states():
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
    machine = renumber_states(machine)
    assert machine.start_idx == {0, }
    assert machine.end_idx == {1, }
    assert len(machine.states) == 3
    assert len(machine.states[0].links) == 1
    assert machine.states[0].links['a'] == {1, 2, }
    assert len(machine.states[1].links) == 0
    assert len(machine.states[2].links) == 1
    assert machine.states[2].links['b'] == {1, }


def test_full_determine():
    data = """DOA: v1
Start: 6
Acceptance: 2 & 5
--BEGIN--
State: 0
    -> EPS 2
State: 1
    -> a 0
State: 2
    -> EPS 1
State: 3
    -> EPS 5
State: 4
    -> b 3
State: 5
    -> EPS 4
State: 6
    -> EPS 2
    -> EPS 5
--END--
"""
    machine = encoder.decode(data)
    alpha = {'a', 'b'}
    machine = mutator.full_determine(machine, alpha)
    machine = renumber_states(machine)
    assert machine.start_idx == {0, }
    assert machine.end_idx == {0, 1, 2}
    assert len(machine.states) == 4
    for state in machine.states.values():
        assert len(state.links) == len(alpha)
    assert (machine.states[0].links['b'] == {1, }
            and machine.states[1].links['a'] == {3, }
            and machine.states[1].links['b'] == {1, }
            and machine.states[0].links['a'] == {2, }
            and machine.states[2].links['b'] == {3, }
            and machine.states[2].links['a'] == {2, }) \
           or (machine.states[0].links['a'] == {1, }
               and machine.states[1].links['b'] == {3, }
               and machine.states[1].links['a'] == {1, }
               and machine.states[0].links['b'] == {2, }
               and machine.states[2].links['a'] == {3, }
               and machine.states[2].links['b'] == {2, })
    assert machine.states[3].links['a'] == {3, }
    assert machine.states[3].links['b'] == {3, }


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
    machine = mutator.minimize_and_determine(machine)
    assert machine.start_idx == {0, }
    assert machine.end_idx == {2, }
    assert len(machine.states) == 3
    assert machine.states[0].links['a'] == {1, }
    assert machine.states[0].links['b'] == {1, }
    assert machine.states[1].links['a'] == {1, }
    assert machine.states[1].links['b'] == {2, }
