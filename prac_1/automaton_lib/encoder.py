"""This module defines functions to apply changes to state machine"""
from .mutator import renumber_states
from .regexp_utils import regexp_to_rpn
from .state_machine import StateMachine, State


def decode(data: str, format: str) -> StateMachine:
    """This function build nondeterministic finite-state automata according to the description"""
    if format == "doa":
        return decode_doa(data)
    elif format == "regexp":
        return decode_regexp(data)
    else:
        raise Exception("Unknown format '%s'" % format)


def decode_doa(text: str) -> StateMachine:
    """This function build finite-state automata according to the description in
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


def decode_regexp(text: str) -> StateMachine:
    """This function build finite-state automata according to regexp"""
    rpn = regexp_to_rpn(text)
    stack = []
    for token in rpn:
        if token.isalpha() or token == "":
            stack.append(StateMachine(token))
        elif token == "|":
            machine = stack.pop()
            machine1 = stack.pop()
            stack.append(machine1 + machine)
        elif token == "&":
            machine = stack.pop()
            stack[-1] *= machine
        elif token in ["+", "*"] or token.isdigit():
            stack[-1] **= token
        else:
            raise Exception("Unknown token " + token)
    return stack.pop()


def encode(machine: StateMachine, format: str) -> str:
    """This function convert finite-state automata to format"""
    if format == "doa":
        return encode_doa(machine)
    elif format == "graphviz":
        return encode_graphviz(machine)
    else:
        raise Exception("Unknown format '%s'" % format)


def encode_doa(machine: StateMachine) -> str:
    """This function convert finite-state automata to the doa format"""
    machine = renumber_states(machine)
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


def encode_graphviz(machine: StateMachine) -> str:
    """This function convert finite-state automata to the graphviz format"""
    res = "digraph {\n"
    res += "  rankdir=LR\n"
    for idx in machine.start_idx:
        res += "  \"%s\" [color=green]\n" % str(idx)
    for idx in machine.end_idx:
        res += "  \"%s\" [style=filled, fillcolor=red]\n" % str(idx)
    for at, state in machine.states.items():
        for trigger, idx_list in state.links.items():
            for to in idx_list:
                res += "  \"%s\" -> \"%s\" [label=\"%s\"]\n" % (str(at), str(to), str(trigger))
    res += "}\n"
    return res
