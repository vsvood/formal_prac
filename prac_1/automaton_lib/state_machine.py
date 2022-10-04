"""This module provides State Machine class"""
import copy
from collections import defaultdict


class State:
    """This class represent State Machine node structure"""

    def __init__(self, links: dict = None):
        if links is None:
            links = {}
        self.links = defaultdict(set, links)


class StateMachine:
    """This class represents State Machine structure"""

    def __init__(self, token: str = None):
        self.states = dict()
        if token is None:
            self.end_idx = set()
            self.start_idx = set()
        else:
            self.start_idx = {0}
            self.states[0] = State({token: {1}})
            self.states[1] = State()
            self.end_idx = {1}

    def extend_vertices(self, other):
        translate = defaultdict(lambda: len(self.states))
        for key in other.states:
            self.states[translate[key]] = State()
        for key in other.states:
            new_key = translate[key]
            for trigger, state_list in other.states[key].links.items():
                self.states[new_key].links[trigger] = {translate[x] for x in state_list}
        return translate

    def __add__(self, other):
        result = copy.deepcopy(self)
        translate = result.extend_vertices(other)
        new_start = translate["*"]
        result.start_idx.update({translate[idx] for idx in other.start_idx})
        result.states[new_start] = State({"": result.start_idx})
        result.start_idx = {new_start}
        result.end_idx.update({translate[idx] for idx in other.end_idx})
        return result

    def __mul__(self, other):
        result = copy.deepcopy(self)
        translate = result.extend_vertices(other)
        other_new_begin = {translate[state] for state in other.start_idx}
        for idx in result.end_idx:
            result.states[idx].links[''].update(other_new_begin)
        result.end_idx = {translate[idx] for idx in other.end_idx}
        return result

    def kleene_star(self):
        result = self.kleene_plus()
        result.start_idx = result.end_idx
        return result

    def kleene_plus(self):
        result = copy.deepcopy(self)
        new_state = len(result.states)
        result.states[new_state] = State({'': result.start_idx})
        for idx in result.end_idx:
            result.states[idx].links[''].add(new_state)
        result.end_idx = {new_state}
        return result

    def power(self, power: int):
        result = StateMachine("")
        for _ in range(power):
            result *= self
        return result

    def __pow__(self, power):
        if power == "*":
            return self.kleene_star()
        elif power == "+":
            return self.kleene_plus()
        elif power.isdigit():
            return self.power(int(power))
        else:
            raise Exception("bad power " + power)
