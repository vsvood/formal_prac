"""This module provides State Machine class"""
from collections import defaultdict


class Node:
    """This class represent State Machine node structure"""
    def __init__(self, transitions: dict = None):
        if transitions is None:
            transitions = {}
        self.transitions = defaultdict(set, transitions)


class StateMachine:
    """This class represents State Machine structure"""
    def __init__(self):
        self.nodes = dict()
        self.end_idx = set()
        self.start_idx = set()
