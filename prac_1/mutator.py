import copy
from collections import defaultdict

from state_machine import StateMachine, Node


def split_complex_links(machine: StateMachine) -> StateMachine:
    result = copy.deepcopy(machine)
    translate = defaultdict(lambda: len(result.nodes))
    for key, node in machine.nodes.items():
        for trigger, node_list in node.transitions.items():
            if len(trigger) < 2:
                continue
            result.nodes[key].transitions.pop(trigger)
            last_key = key
            for new_key in trigger[:-1]:
                result.nodes[last_key].transitions[new_key].add(translate[new_key])
                result.nodes[translate[new_key]] = Node()
                last_key = translate[new_key]
            result.nodes[last_key].transitions[trigger[-1]].update(node_list)
    return result
