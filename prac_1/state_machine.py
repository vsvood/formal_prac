"""This module provides State Machine class"""
from collections import defaultdict


class State:
    """This class represent State Machine node structure"""
    def __init__(self, links: dict = None):
        if links is None:
            links = {}
        self.links = defaultdict(set, links)


class StateMachine:
    """This class represents State Machine structure"""
    def __init__(self):
        self.states = dict()
        self.end_idx = set()
        self.start_idx = set()
