"""This module provides methods for modifying cf-grammars"""
import copy

from cf_grammar import CFGrammar


def convert_to_chomsky(grammar: CFGrammar) -> CFGrammar:
    """This function converts grammar to chomsky normal form"""
    new_grammar = drop_non_gen(grammar)
    new_grammar = drop_unreachable(new_grammar)
    new_grammar = fix_mixed_rules(new_grammar)
    return new_grammar


def drop_non_gen(grammar: CFGrammar) -> CFGrammar:
    """This function delete non generating rules from grammar"""
    gen_list = set()
    rule_list = []
    new_grammar = CFGrammar()
    new_grammar.start = grammar.start

    def check(g_rule: str):
        for char in g_rule:
            if char.islower() or char == "" or char in gen_list:
                continue
            return False
        return True

    added = True
    while added:
        added = False
        for key, rule_set in grammar.rel.items():
            for rule in rule_set:
                if (key, rule) in rule_list:
                    continue
                if check(rule):
                    added = True
                    rule_list.append((key, rule))
                    gen_list.add(key)
                    break
    for key, rule in rule_list:
        if key not in new_grammar.rel:
            new_grammar.rel[key] = set()
        new_grammar.rel[key].add(rule)

    return new_grammar


def drop_unreachable(grammar: CFGrammar) -> CFGrammar:
    """This function delete unreachable rules"""
    reachable = set()

    def dfs(key: str):
        reachable.add(key)
        for g_rule in grammar.rel[key]:
            for char in g_rule:
                if char.isupper() and char not in reachable:
                    dfs(char)

    dfs(grammar.start)
    new_grammar = CFGrammar()
    new_grammar.start = grammar.start
    for key in reachable:
        new_grammar.rel[key] = grammar.rel[key]
    return new_grammar


def get_generator(grammar: CFGrammar, token: str) -> str:
    for key, rule_set in grammar.rel.items():
        if rule_set == {(token,), }:
            return key
    generator = token.upper()
    if generator not in grammar.rel:
        return generator
    idx = 1
    while generator+"_"+str(idx) in grammar.rel:
        idx += 1
    return generator+"_"+str(idx)


def fix_rule_set(rule_set: set[tuple[str]], token: str, token_gen: str) -> set[tuple[str]]:
    new_rule_set = set()
    for rule in rule_set:
        new_rule_set.add(tuple([(word, token_gen)[word == token] for word in rule]))
    return new_rule_set


def fix_mixed_rules(grammar: CFGrammar) -> CFGrammar:
    """This function converts mixed rules to single-type rules"""
    new_grammar = CFGrammar()
    new_grammar.start = grammar.start
    new_grammar.alpha = grammar.alpha

    rel = copy.deepcopy(grammar.rel)
    new_rel = {}
    new_var = []
    for token in grammar.alpha:
        token_gen = get_generator(grammar, token)
        new_var.append(token_gen)
        for key, rule_set in rel.items():
            new_rel[key] = fix_rule_set(rule_set, token, token_gen)
        new_rel[token_gen] = {(token,), }
        rel = new_rel
        new_rel = {}

    new_grammar.var = grammar.var
    new_grammar.var.update(new_var)
    new_grammar.rel = rel

    return new_grammar
        
