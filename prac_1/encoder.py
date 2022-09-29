"""This module defines functions to apply changes to state machine"""
from state_machine import StateMachine, State


def decode(text: str) -> StateMachine:
    """This function build nondeterministic finite-state automata according to the description in
    the doa format"""
    machine = StateMachine()
    lines = text.split('\n')
    if lines[0] != "DOA: v1":
        raise Exception("Format error: header. Expected 'DOA: v1' line, '%s' found" % lines[0])
    start = lines[1].split()
    if start[0] != "Start:":
        raise Exception("Format error: start. Expected 'Start:' line, '%s' found" % start[0])
    machine.start_idx.update(start[1::2])
    acceptance = lines[2].split()
    if acceptance[0] != "Acceptance:":
        raise Exception("Format error: acceptance. Expected 'Acceptance:' line, '%s' found"
                        % acceptance[0])
    machine.end_idx.update(acceptance[1::2])
    if lines[3] != "--BEGIN--":
        raise Exception("Format error: begin. Expected '--BEGIN--' line, '%s' found" % lines[3])
    cur_state = None
    for statement in lines[4:]:
        parsed = statement.split()
        if parsed[0] == "--END--":
            break
        if parsed[0] == "State:":
            cur_state = parsed[1]
            machine.states[cur_state] = State()
        elif len(parsed) < 2:
            raise Exception("Format error: '->' or 'State:' statement expected, '%s' found"
                            % statement)
        elif parsed[0] == "->":
            if cur_state is None:
                raise Exception("Format error: '->' statement before State declaration")
            if parsed[1] != "EPS":
                machine.states[cur_state].links[parsed[1]].add(parsed[2])
            else:
                machine.states[cur_state].links[''].add(parsed[2])
            if parsed[2] not in machine.states:
                machine.states[parsed[2]] = State()
        else:
            raise Exception("Format error: '->' or 'State:' statement expected, '%s' found"
                            % statement)
    return machine


def encode(machine: StateMachine) -> str:
    """This function convert nondeterministic finite-state automata to the doa format"""
    res = "DOA: v1\n"
    res += "Start: %s\n" % " & ".join([str(x) for x in machine.start_idx])
    res += "Acceptance: %s\n" % " & ".join([str(x) for x in machine.end_idx])
    res += "--BEGIN--\n"
    for idx, state in machine.states.items():
        res += "State: %s\n" % str(idx)
        for trigger, idx_list in state.links.items():
            for to_idx in idx_list:
                res += "    -> %s %s\n" % (trigger if trigger != "" else "EPS", str(to_idx))
    res += "--END--\n"
    return res
