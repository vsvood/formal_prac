"""Decoder tests"""
import pytest

from automaton_lib.encoder import decode


def test_broken_header():
    data = """XXX
Start: 0
Acceptance: 2
--BEGIN--
--END--
"""
    with pytest.raises(Exception,
                       match=r"Format error: header\. Expected 'DOA: v1' line, '.+' found"):
        decode(data)


def test_no_start():
    data = """DOA: v1
Acceptance: 2
--BEGIN--
--END--
"""
    with pytest.raises(Exception,
                       match=r"Format error: start\. Expected 'Start:' line, '.+' found"):
        decode(data)


def test_no_acceptance():
    data = """DOA: v1
Start: 0
--BEGIN--
--END--
"""
    with pytest.raises(Exception,
                       match=r"Format error: acceptance\. Expected 'Acceptance:' line, '.+' found"):
        decode(data)


def test_no_begin():
    data = """DOA: v1
Start: 0
Acceptance: 2
--END--
"""
    with pytest.raises(Exception,
                       match=r"Format error: begin\. Expected '--BEGIN--' line, '.+' found"):
        decode(data)


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
        decode(data)


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
        decode(data)


def test_unknown_statement_long():
    data = """DOA: v1
Start: 0
Acceptance: 2
--BEGIN--
a b c d e f g h i j k l m n o p
--END--
"""
    with pytest.raises(Exception,
                       match=r"Format error: '->' or 'State:' statement expected, '.+' found"):
        decode(data)


def test_simple_build():
    data = """DOA: v1
Start: 0
Acceptance: 1
--BEGIN--
State: 0
    -> a 1
--END--
"""
    machine = decode(data)

    assert machine.start_idx == {'0', }
    assert machine.end_idx == {'1', }
    assert len(machine.states) == 2
    assert len(machine.states['0'].links) == 1
    assert machine.states['0'].links['a'] == {'1', }
    assert len(machine.states['1'].links) == 0