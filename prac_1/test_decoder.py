import pytest

from state_machine import StateMachine, Node
from state_machine_utils import build_nfa_from_doa


def test_broken_header():
    data = """XXX
Start: 0
Acceptance: 2
--BEGIN--
--END--
"""
    with pytest.raises(Exception,
                       match=r"Format error: header\. Expected 'DOA: v1' line, '.+' found"):
        build_nfa_from_doa(data)


def test_no_start():
    data = """DOA: v1
Acceptance: 2
--BEGIN--
--END--
"""
    with pytest.raises(Exception,
                       match=r"Format error: start\. Expected 'Start:' line, '.+' found"):
        build_nfa_from_doa(data)


def test_no_acceptance():
    data = """DOA: v1
Start: 0
--BEGIN--
--END--
"""
    with pytest.raises(Exception,
                       match=r"Format error: acceptance\. Expected 'Acceptance:' line, '.+' found"):
        build_nfa_from_doa(data)


def test_no_begin():
    data = """DOA: v1
Start: 0
Acceptance: 2
--END--
"""
    with pytest.raises(Exception,
                       match=r"Format error: begin\. Expected '--BEGIN--' line, '.+' found"):
        build_nfa_from_doa(data)


def test_broken_state_block():
    data = """DOA: v1
Start: 0
Acceptance: 2
--BEGIN--
    -> ab 1
--END--
"""
    with pytest.raises(Exception,
                       match=r"Format error: '->' statement before State declaration"):
        build_nfa_from_doa(data)


def test_unknown_statement():
    data = """DOA: v1
Start: 0
Acceptance: 2
--BEGIN--
abobabass
--END--
"""
    with pytest.raises(Exception,
                       match=r"Format error: '->' or 'State:' statement expected, '.+' found"):
        build_nfa_from_doa(data)


def test_simple_build():
    data = """DOA: v1
Start: 0
Acceptance: 1
--BEGIN--
State: 0
    -> a 1
--END--
"""
    machine = build_nfa_from_doa(data)

    assert machine.start_idx == '0'
    assert machine.end_idx == {'1', }
    assert len(machine.nodes) == 2
    assert len(machine.nodes['0'].transitions) == 1
    assert machine.nodes['0'].transitions['a'] == {'1', }
    assert len(machine.nodes['1'].transitions) == 0
