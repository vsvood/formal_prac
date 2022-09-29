from collections import defaultdict

from .state_machine import StateMachine
from .mutator import minimize_and_determine


def check_isomorphism(first: StateMachine, second: StateMachine) -> bool:
    translate = {}
    rtranslate = {}
    first_queue = list(first.start_idx)
    second_queue = list(second.start_idx)
    first_used = defaultdict(lambda: False)
    second_used = defaultdict(lambda: False)
    while first_queue:
        first_state = first_queue.pop(0)
        second_state = second_queue.pop(0)
        if first_used[first_state] != second_used[second_state]:
            return False
        if first_used[first_state] and second_used[second_state]:
            continue
        rtranslate[second_state] = first_state
        translate[first_state] = second_state
        if len(first.states[first_state].links) != len(second.states[second_state].links):
            return False
        for trigger, state_list in first.states[first_state].links.items():
            if trigger not in second.states[second_state].links:
                return False
            for state in state_list:
                first_queue.append(state)
            for state in second.states[second_state].links[trigger]:
                second_queue.append(state)
        first_used[first_state] = True
        second_used[second_state] = True
    for state in first.end_idx:
        if translate[state] not in second.end_idx:
            return False
    for state in second.end_idx:
        if translate[state] not in first.end_idx:
            return False
    return True


def check_equality(first: StateMachine, second: StateMachine) -> bool:
    min_first = minimize_and_determine(first)
    min_second = minimize_and_determine(second)
    return check_isomorphism(min_first, min_second)
