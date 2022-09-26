"""This module define functions to apply common operations on state machine"""
import copy
from collections import defaultdict

from state_machine import StateMachine, State


def split_complex_links(machine: StateMachine) -> StateMachine:
    """Split multi-letter links to several single-letter"""
    result = copy.deepcopy(machine)
    translate = defaultdict(lambda: len(result.states))
    for key, state in machine.states.items():
        for trigger, state_list in state.links.items():
            if len(trigger) < 2:
                continue
            result.states[key].links.pop(trigger)
            last_key = key
            for new_key in trigger[:-1]:
                result.states[last_key].links[new_key].add(translate[new_key])
                result.states[translate[new_key]] = State()
                last_key = translate[new_key]
            result.states[last_key].links[trigger[-1]].update(state_list)
    return result


def renumber_vertices(machine: StateMachine) -> StateMachine:
    """Rename vertices with numbers from 0 to len(machine.states)-1"""
    result = StateMachine()
    translate = defaultdict(lambda: len(result.states))
    for key in machine.states:
        result.states[translate[key]] = State()
    for key in machine.states:
        new_key = translate[key]
        for trigger, states_list in machine.states[key].links.items():
            result.states[new_key].links[trigger] = \
                set([translate[x] for x in states_list])
    result.start_idx = set([translate[state] for state in machine.start_idx])
    result.end_idx = set([translate[x] for x in machine.end_idx])
    return result


def transitive_eps_closure(machine: StateMachine) -> StateMachine:
    """Build transitive epsilon closure of machine using Floyd-Warshall algorithm"""
    result = copy.deepcopy(machine)
    for mid_state in result.states:
        for from_state in result.states:
            if "" in result.states[mid_state].links:
                for to_state in result.states[mid_state].links[""]:
                    if "" in result.states[from_state].links:
                        if mid_state in result.states[from_state].links[""]:
                            result.states[from_state].links[""].add(to_state)
    return result


def extend_final_states(machine: StateMachine) -> StateMachine:
    """Add state to final states if one of them is reachable with epsilon link"""
    result = copy.deepcopy(machine)
    for first in result.states:
        if "" in result.states[first].links:
            for second in result.states[first].links[""]:
                if second in result.end_idx:
                    result.end_idx.add(first)
    return result


def extend_links(machine: StateMachine):
    """Add link A--trigger-->B to machine if in original version
    A--eps-->C and c--trigger-->B links present"""
    result = copy.deepcopy(machine)
    for first in result.states:
        if "" in result.states[first].links:
            for second in result.states[first].links[""]:
                for trigger, state_list in result.states[second].links.items():
                    if trigger != "":
                        result.states[first].links[trigger].update(state_list)
    return result


def drop_eps_links(machine: StateMachine) -> StateMachine:
    """Delete all epsilon links"""
    result = copy.deepcopy(machine)
    for state in result.states:
        result.states[state].links.pop("", None)
    return result


def drop_unreachable_state(machine: StateMachine):
    # TODO drop states from which end is not acceptable
    """Delete all states that are not reachable from start one"""
    result = StateMachine()
    result.start_idx = machine.start_idx
    queue = list(machine.start_idx)
    processed = defaultdict(lambda: False)
    while queue:
        state = queue.pop()
        if not processed[state]:
            if state in machine.end_idx:
                result.end_idx.add(state)
            result.states[state] = machine.states[state]
            for state_list in machine.states[state].links.values():
                for to in state_list:
                    queue.append(to)
            processed[state] = True
    return result


def simplify_machine(machine: StateMachine) -> StateMachine:
    """Prepare machine for determination.
    Build machine with strict-single-letter links"""
    result = split_complex_links(machine)
    result = transitive_eps_closure(result)
    result = extend_final_states(result)
    result = extend_links(result)
    result = drop_eps_links(result)
    result = drop_unreachable_state(result)
    return result


def weak_determine(machine: StateMachine) -> StateMachine:
    """Build deterministic finite automaton.
    Require machine to have strict-single-letter links"""
    result = StateMachine()
    processed = defaultdict(lambda: False)
    result.start_idx = {tuple(sorted(machine.start_idx)), }
    queue = list(result.start_idx)
    while queue:
        state = queue.pop()
        if not processed[state]:
            if state not in result.states:
                result.states[state] = State()
                for sub_state in state:
                    if sub_state in machine.end_idx:
                        result.end_idx.add(state)
                for sub_state in state:
                    for trigger, state_list in machine.states[sub_state].links.items():
                        result.states[state].links[trigger].update(state_list)
                for trigger, state_list in result.states[state].links.items():
                    result.states[state].links[trigger] = {tuple(sorted(state_list)), }

            for to_states in result.states[state].links.values():
                for to_state in to_states:
                    queue.append(to_state)
            processed[state] = True
    return result


def strong_determine(machine: StateMachine) -> StateMachine:
    """Build deterministic finite automaton."""
    result = simplify_machine(machine)
    result = weak_determine(result)
    return result


def supplement(machine: StateMachine, alpha: set) -> StateMachine:
    """Add missing links from each state to Black Hole state according to specified alpha
    Require machine to have strict-single-letter links"""
    result = renumber_vertices(machine)
    new_state = len(result.states)
    added_links = 0
    for letter in alpha:
        for state in result.states.values():
            if not state.links[letter]:
                state.links[letter] = {new_state, }
                added_links += 1
    if added_links:
        result.states[new_state] = State()
        for letter in alpha:
            result.states[new_state].links[letter] = {new_state, }
    return result


def full_determine(machine: StateMachine, alpha: set) -> StateMachine:
    """Build complete deterministic finite automaton."""
    result = strong_determine(machine)
    result = supplement(result, alpha)
    return result


def reverse(machine: StateMachine) -> StateMachine:
    """Reverse machine
    new start states are old end states
    new end states are old start states
    links has reversed direction"""
    result = StateMachine()
    result.start_idx = set(machine.end_idx)
    result.end_idx = set(machine.start_idx)
    for key in machine.states:
        result.states[key] = State()
    for key, state in machine.states.items():
        for trigger, to_key_list in state.links.items():
            for to_key in to_key_list:
                result.states[to_key].links[trigger].add(key)
    return result


def minimize_and_determine(machine: StateMachine) -> StateMachine:
    """Build minimal complete deterministic finite automaton.
    Uses Brzozowski's algorithm"""
    result = simplify_machine(machine)
    result = reverse(result)
    result = drop_unreachable_state(result)
    result = weak_determine(result)
    result = renumber_vertices(result)
    result = reverse(result)
    result = weak_determine(result)
    result = renumber_vertices(result)
    result = renumber_vertices(result)
    return result
