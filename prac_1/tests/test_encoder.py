"""Encoder tests"""
from automaton_lib.state_machine import StateMachine, State
from automaton_lib.encoder import encode


def test_convert():
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

    assert encode(machine) == data
