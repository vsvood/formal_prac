from state_machine import StateMachine, Node
from state_machine_utils import convert_nfa_to_doa


def test_convert():
    machine = StateMachine()
    machine.start_idx = 0
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

    assert convert_nfa_to_doa(machine) == data
