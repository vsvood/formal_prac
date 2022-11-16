"""This module provides methods for modifying cf-grammars"""
import copy

from cf_grammar import CFGrammar


def convert_to_chomsky(grammar: CFGrammar) -> CFGrammar:
    """This function converts grammar to chomsky normal form"""
    new_grammar = drop_non_gen(grammar)
    new_grammar = drop_unreachable(new_grammar)
    new_grammar = fix_mixed_rules(new_grammar)
    new_grammar = fix_long_rules(new_grammar)
    new_grammar = fix_eps_rules(new_grammar)
    new_grammar = fix_single_rules(new_grammar)
    return new_grammar


def drop_non_gen(grammar: CFGrammar) -> CFGrammar:
    """This function delete non generating rules from grammar"""
    gen_list = set()
    rule_list = []
    new_grammar = CFGrammar()
    new_grammar.start = copy.deepcopy(grammar.start)
    new_grammar.alpha = copy.deepcopy(grammar.alpha)
    new_grammar.var = copy.deepcopy(grammar.var)

    def check(g_rule: str):
        for char in g_rule:
            if char in grammar.alpha or char == "" or char in gen_list:
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
        if key in grammar.rel:
            for g_rule in grammar.rel[key]:
                for char in g_rule:
                    if char.isupper() and char not in reachable:
                        dfs(char)

    dfs(grammar.start)
    new_grammar = CFGrammar()
    new_grammar.start = copy.deepcopy(grammar.start)
    new_grammar.var = copy.deepcopy(grammar.var)
    new_grammar.alpha = copy.deepcopy(grammar.alpha)
    for key in reachable:
        new_grammar.rel[key] = copy.deepcopy(grammar.rel[key])
    return new_grammar


def get_new_var(grammar: CFGrammar, rule: tuple[str]) -> str:
    """This function return new variable name associated with rule"""
    var = "+".join(["(%s)" % token.upper() for token in rule])
    if var not in grammar.var and var not in grammar.alpha:
        return var
    idx = 1
    var_i = var + "_%d" % idx
    while var_i in grammar.var or \
            var_i in grammar.alpha:
        idx += 1
        var_i = var + "_%d" % idx

    return var_i


def get_var(grammar: CFGrammar, rule: tuple[str]) -> str:
    """This function return existing or new variable associated with rule"""
    for key, rule_set in grammar.rel.items():
        if rule_set == {rule, }:
            return key
    return get_new_var(grammar, rule)


def get_generator(grammar: CFGrammar, token: str) -> str:
    """This function returns variable which produces token"""
    return get_var(grammar, (token,))


def fix_rule_set(rule_set: set[tuple[str]], token: str, token_gen: str) -> set[tuple[str]]:
    """This function replace token to variable associated with it"""
    new_rule_set = set()
    for rule in rule_set:
        new_rule_set.add(tuple((word, token_gen)[word == token] for word in rule))
    return new_rule_set


def fix_mixed_rules(grammar: CFGrammar) -> CFGrammar:
    """This function converts mixed rules to single-type rules"""
    new_grammar = CFGrammar()
    new_grammar.start = copy.deepcopy(grammar.start)
    new_grammar.var = copy.deepcopy(grammar.var)
    new_grammar.alpha = copy.deepcopy(grammar.alpha)
    new_grammar.rel = copy.deepcopy(grammar.rel)

    new_rel = {}
    for token in grammar.alpha:
        token_gen = get_generator(new_grammar, token)
        new_grammar.var.add(token_gen)
        for key, rule_set in new_grammar.rel.items():
            new_rel[key] = fix_rule_set(rule_set, token, token_gen)
        new_rel[token_gen] = {(token,), }
        new_grammar.rel = copy.deepcopy(new_rel)
        new_rel = {}

    return new_grammar


def fix_long_rules(grammar: CFGrammar) -> CFGrammar:
    """This function proceed and delete long rules"""
    new_grammar = CFGrammar()
    new_grammar.start = copy.deepcopy(grammar.start)
    new_grammar.var = copy.deepcopy(grammar.var)
    new_grammar.alpha = copy.deepcopy(grammar.alpha)

    long_rule_list = []
    for key, rule_set in grammar.rel.items():
        new_grammar.rel[key] = set()
        for rule in rule_set:
            if len(rule) <= 2:
                new_grammar.rel[key].add(rule)
            else:
                long_rule_list.append((key, rule))

    for key, rule in long_rule_list:
        while len(rule) > 2:
            new_var = get_var(new_grammar, rule[0:2])
            new_grammar.var.add(new_var)
            new_grammar.rel[new_var] = {rule[0:2], }
            rule = (new_var,) + rule[2:]
        if key not in new_grammar.rel:
            new_grammar.rel[key] = set()
        new_grammar.rel[key].add(rule)

    return new_grammar


def get_new_start(grammar: CFGrammar) -> str:
    """Return new start var name"""
    return get_new_var(grammar, (grammar.start,))


def extend_rules_eps(grammar: CFGrammar, eps_gen_set: set[str]) -> bool:
    """This function extend rule list according to list of eps-gen vars"""
    modified = False
    for eps_gen in eps_gen_set:
        new_rel = {}
        for key, rule_set in grammar.rel.items():
            new_rel[key] = copy.deepcopy(rule_set)
            for rule in rule_set:
                for i in range(len(rule)):
                    if rule[i] == eps_gen:
                        if len(rule) > 1:
                            if rule[:i] + rule[i + 1:] not in rule_set:
                                modified = True
                            new_rel[key].add(rule[:i] + rule[i + 1:])
                        else:
                            if key not in eps_gen_set and key != grammar.start:
                                modified = True
                            new_rel[key].add(("",))
        grammar.rel = copy.deepcopy(new_rel)
    return modified


def fix_eps_gen(grammar: CFGrammar) -> set[str]:
    """This function delete eps gen rules and return list of eps gen vars"""
    new_rel = {}
    eps_gen_set = set()
    for key, rule_set in grammar.rel.items():
        new_rel[key] = set()
        for rule in rule_set:
            if rule == ("",) and key != grammar.start:
                eps_gen_set.add(key)
            else:
                new_rel[key].add(rule)
    grammar.rel = copy.deepcopy(new_rel)

    return eps_gen_set


def fix_eps_rules(grammar: CFGrammar) -> CFGrammar:
    """This function proceed and delete inappropriate eps rules"""
    new_start = get_new_start(grammar)
    new_grammar = copy.deepcopy(grammar)
    new_grammar.var.add(new_start)
    new_grammar.rel[new_start] = {(grammar.start,), }
    new_grammar.start = new_start

    modified = True
    eps_gen_set = set()
    while modified:
        eps_gen_set.update(fix_eps_gen(new_grammar))
        modified = extend_rules_eps(new_grammar, eps_gen_set)
    fix_eps_gen(new_grammar)

    return new_grammar


def build_single_closure(grammar: CFGrammar):
    """This function builds single variable rule closure using
    Floyd–Warshall algorithm"""
    rel = copy.deepcopy(grammar.rel)
    for mid in grammar.rel:
        for beg in grammar.rel:
            for end in grammar.rel:
                if (mid,) in rel[beg] and (end,) in rel[mid]:
                    rel[beg].add((end,))
    grammar.rel = rel


def extend_rules_single(grammar: CFGrammar):
    """This function add rules according to single variable rules"""
    rel = copy.deepcopy(grammar.rel)
    for from_key in grammar.rel:
        for to_key in grammar.rel:
            if (to_key,) in grammar.rel[from_key]:
                for rule in grammar.rel[to_key]:
                    if len(rule) == 2 or rule[0] in grammar.alpha:
                        rel[from_key].add(rule)
    grammar.rel = rel


def drop_single_rules(grammar: CFGrammar):
    """This function delete single rules"""
    rel = {}
    for key in grammar.rel:
        rel[key] = set()
        for rule in grammar.rel[key]:
            if len(rule) == 2 or rule[0] in grammar.alpha:
                rel[key].add(rule)
    grammar.rel = rel


def fix_single_rules(grammar: CFGrammar) -> CFGrammar:
    """This function proceed and delete single variable rules"""
    new_grammar = copy.deepcopy(grammar)
    build_single_closure(new_grammar)
    extend_rules_single(new_grammar)
    drop_single_rules(new_grammar)
    return new_grammar
