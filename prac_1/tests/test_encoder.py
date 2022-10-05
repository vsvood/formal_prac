"""Encoder tests"""
import pytest

from automaton_lib.state_machine import StateMachine, State
from automaton_lib.encoder import encode, decode


def test_bad_format():
    with pytest.raises(Exception, match=r"Unknown format '.+'"):
        encode(StateMachine(), "abracadabra")


def test_convert_doa():
    machine = StateMachine()
    machine.start_idx = {0, }
    machine.end_idx = {1, }
    machine.states[0] = State({'a': {1, }})
    machine.states[1] = State()

    data = """DOA: v1
Start: 0
Acceptance: 1
--BEGIN--
State: 0
    -> a 1
State: 1
--END--
"""

    assert encode(machine, "doa") == data


def test_encode_graphviz():
    data = """DOA: v1
Start: 0
Acceptance: 1
--BEGIN--
State: 0
    -> a 1
State: 1
--END--
"""
    g_gata = """digraph {
rankdir=LR
"0" [color=green]
"1" [style=filled, fillcolor=red]
"0" -> "1" [label="a"]
}
"""
    assert encode(decode(data, "doa"), "graphviz")
