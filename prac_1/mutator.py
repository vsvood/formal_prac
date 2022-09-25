import copy
from collections import defaultdict

from state_machine import StateMachine, Node


def split_complex_links(machine: StateMachine) -> StateMachine:
    """Split multi-letter links to several single-letter"""
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


def renumber_vertices(machine: StateMachine) -> StateMachine:
    """Rename vertices with numbers from 0 to len(machine.nodes)-1"""
    result = StateMachine()
    translate = defaultdict(lambda: len(result.nodes))
    for key in machine.nodes:
        result.nodes[translate[key]] = Node()
    for key in machine.nodes:
        new_key = translate[key]
        for trigger, nodes_list in machine.nodes[key].transitions.items():
            result.nodes[new_key].transitions[trigger] = \
                set([translate[x] for x in nodes_list])
    result.start_idx = translate[machine.start_idx]
    result.end_idx = set([translate[x] for x in machine.end_idx])
    return result


def transitive_eps_closure(machine: StateMachine) -> StateMachine:
    """Build transitive epsilon closure of machine using Floyd-Warshall algorithm"""
    result = copy.deepcopy(machine)
    for mid_node in result.nodes:
        for from_node in result.nodes:
            if "" in result.nodes[mid_node].transitions:
                for to_node in result.nodes[mid_node].transitions[""]:
                    if "" in result.nodes[from_node].transitions:
                        if mid_node in result.nodes[from_node].transitions[""]:
                            result.nodes[from_node].transitions[""].add(to_node)
    return result


def extend_final_states(machine: StateMachine) -> StateMachine:
    """Add state to final states if one of them is reachable with epsilon link"""
    result = copy.deepcopy(machine)
    for first in result.nodes:
        if "" in result.nodes[first].transitions:
            for second in result.nodes[first].transitions[""]:
                if second in result.end_idx:
                    result.end_idx.add(first)
    return result


def extend_links(machine: StateMachine):
    """Add link A--trigger-->B to machine if in original version
    A--eps-->C and c--trigger-->B links present"""
    result = copy.deepcopy(machine)
    for first in result.nodes:
        if "" in result.nodes[first].transitions:
            for second in result.nodes[first].transitions[""]:
                for trigger, node_list in result.nodes[second].transitions.items():
                    if trigger != "":
                        result.nodes[first].transitions[trigger].update(node_list)
    return result


def drop_eps_links(machine: StateMachine) -> StateMachine:
    """Delete all epsilon links"""
    result = copy.deepcopy(machine)
    for node in result.nodes:
        result.nodes[node].transitions.pop("", None)
    return result


def drop_unreachable_state(machine: StateMachine):
    """Delete all states that are not reachable from start one"""
    result = copy.deepcopy(machine)
    queue = [result.start_idx, ]
    processed = defaultdict(lambda: False)
    while queue:
        node = queue.pop()
        if not processed[node]:
            if node in result.end_idx:
                result.end_idx.add(node)
            result.nodes[node] = result.nodes[node]
            for node_list in result.nodes[node].transitions.values():
                for to in node_list:
                    queue.append(to)
            processed[node] = True
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
    result = copy.deepcopy(machine)
    processed = defaultdict(lambda: False)
    queue = [(result.start_idx,)]
    result.start_idx = (result.start_idx,)
    nodes = dict()
    end_idx = set()
    while queue:
        node = queue.pop()
        if not processed[node]:
            if node not in nodes:
                nodes[node] = Node()
                for sub_node in node:
                    if sub_node in result.end_idx:
                        end_idx.add(node)
                for sub_node in node:
                    for trigger, node_list in result.nodes[sub_node].transitions.items():
                        nodes[node].transitions[trigger].update(node_list)
                for trigger, node_list in nodes[node].transitions.items():
                    nodes[node].transitions[trigger] = [tuple(sorted(node_list))]

            for to_node in nodes[node].transitions.values():
                if to_node[0] != ():
                    queue.append(to_node[0])
            processed[node] = True
    result.nodes = nodes
    result.end_idx = end_idx
    return result


def strong_determine(machine: StateMachine) -> StateMachine:
    """Build deterministic finite automaton."""
    result = simplify_machine(machine)
    result = weak_determine(result)
    return result


def supplement(machine: StateMachine, alpha: set) -> StateMachine:
    """Add missing links from each state to Black Hole state according to specified alpha"""
    result = copy.deepcopy(machine)
    result.nodes["X"] = Node({})
    for letter in alpha:
        for node in result.nodes.values():
            if not node.transitions[letter]:
                node.transitions[letter] = ("X",)
    return result


def full_determine(machine: StateMachine, alpha: set) -> StateMachine:
    """Build complete deterministic finite automaton."""
    result = strong_determine(machine)
    result = supplement(result, alpha)
    return result
