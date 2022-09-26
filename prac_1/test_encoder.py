"""Encoder tests"""
from state_machine import StateMachine, Node
from encoder import encode


def test_convert():
    machine = StateMachine()
    machine.start_idx = {0, }
    machine.end_idx = {1, }
    machine.nodes[0] = Node({'a': {1, }})
    machine.nodes[1] = Node()

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
