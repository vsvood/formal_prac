"""This module defines functions to apply changes to state machine"""
from state_machine import StateMachine, Node


def build_nfa_from_doa(text: str) -> StateMachine:
    """This function build nondeterministic finite-state automata according to the description in
    the doa format"""
    machine = StateMachine()
    lines = text.split('\n')
    if lines[0] != "DOA: v1":
        raise Exception("Format error: header. Expected 'DOA: v1' line, '%s' found" % lines[0])
    start = lines[1].split()
    if start[0] != "Start:":
        raise Exception("Format error: start. Expected 'Start:' line, '%s' found" % start[0])
    machine.start_idx = start[1]
    machine.nodes[start[1]] = Node()
    acceptance = lines[2].split()
    if acceptance[0] != "Acceptance:":
        raise Exception("Format error: acceptance. Expected 'Acceptance:' line, '%s' found"
                        % acceptance[0])
    machine.end_idx.update(acceptance[1::2])
    for node in acceptance[1::2]:
        machine.nodes[node] = Node()
    if lines[3] != "--BEGIN--":
        raise Exception("Format error: begin. Expected '--BEGIN--' line, '%s' found" % lines[3])
    cur_node = None
    for statement in lines[4:]:
        parsed = statement.split()
        if parsed[0] == "State:":
            cur_node = parsed[1]
            machine.nodes[cur_node] = Node()
        elif parsed[0] == "->":
            if cur_node is None:
                raise Exception("Format error: '->' statement before State declaration")
            machine.nodes[cur_node].transitions[parsed[1]].add(parsed[2])
        elif parsed[0] == "--END--":
            break
        else:
            raise Exception("Format error: '->' or 'State:' statement expected, '%s' found"
                            % parsed[0])
    return machine


def convert_nfa_to_doa(machine: StateMachine) -> str:
    """This function convert nondeterministic finite-state automata to the doa format"""
    res = "DOA: v1\n"
    res += "Start: %s\n" % str(machine.start_idx)
    res += "Acceptance: %s\n" % " & ".join([str(x) for x in machine.end_idx])
    res += "--BEGIN--\n"
    for idx, node in machine.nodes.items():
        res += "State: %s\n" % idx
        for trigger, idx_list in node.transitions.items():
            for to_idx in idx_list:
                res += "    -> %s %s\n" % (trigger, str(to_idx))
    res += "--END--\n"
    return res
