from .cf_grammar import CFGrammar
from . import mutator


def test_drop_non_gen():
    with open("tests/non_gen_in_1") as f:
        in_grammar = CFGrammar(f.read())
    with open("tests/non_gen_out_1") as f:
        out_grammar = CFGrammar(f.read())
    in_grammar = mutator.drop_non_gen(in_grammar)
    assert (out_grammar.rel == in_grammar.rel)


def test_drop_unreachable():
    with open("tests/unreachable_in_1") as f:
        in_grammar = CFGrammar(f.read())
    with open("tests/unreachable_out_1") as f:
        out_grammar = CFGrammar(f.read())
    in_grammar = mutator.drop_unreachable(in_grammar)
    assert (out_grammar.rel == in_grammar.rel)


def test_fix_mixed_rules():
    with open("tests/mixed_in_1") as f:
        in_grammar = CFGrammar(f.read())
    with open("tests/mixed_out_1") as f:
        out_grammar = CFGrammar(f.read())
    in_grammar = mutator.fix_mixed_rules(in_grammar)
    assert (out_grammar.rel == in_grammar.rel)


def test_fix_mixed_rules_1():
    with open("tests/mixed_in_2") as f:
        in_grammar = CFGrammar(f.read())
    with open("tests/mixed_out_2") as f:
        out_grammar = CFGrammar(f.read())
    in_grammar = mutator.fix_mixed_rules(in_grammar)
    assert (out_grammar.rel == in_grammar.rel)


def test_drop_non_gen_1():
    with open("tests/greetings_non_gen_in") as f:
        in_grammar = CFGrammar(f.read())
    with open("tests/greetings_unreachable_in") as f:
        out_grammar = CFGrammar(f.read())
    in_grammar = mutator.drop_non_gen(in_grammar)
    assert (out_grammar.rel == in_grammar.rel)


def test_drop_unreachable_1():
    with open("tests/greetings_unreachable_in") as f:
        in_grammar = CFGrammar(f.read())
    with open("tests/greetings_mixed_in") as f:
        out_grammar = CFGrammar(f.read())
    in_grammar = mutator.drop_unreachable(in_grammar)
    assert (out_grammar.rel == in_grammar.rel)


def test_fix_mixed_rules_2():
    with open("tests/greetings_mixed_in") as f:
        in_grammar = CFGrammar(f.read())
    with open("tests/greetings_long_in") as f:
        out_grammar = CFGrammar(f.read())
    in_grammar = mutator.fix_mixed_rules(in_grammar)
    assert (out_grammar.rel == in_grammar.rel)


def test_fix_long_rules():
    with open("tests/greetings_long_in") as f:
        in_grammar = CFGrammar(f.read())
    with open("tests/greetings_eps_in") as f:
        out_grammar = CFGrammar(f.read())
    in_grammar = mutator.fix_long_rules(in_grammar)
    assert (out_grammar.rel == in_grammar.rel)


def test_fix_eps_rules():
    with open("tests/greetings_eps_in") as f:
        in_grammar = CFGrammar(f.read())
    with open("tests/greetings_single_in") as f:
        out_grammar = CFGrammar(f.read())
    in_grammar = mutator.fix_eps_rules(in_grammar)
    assert (out_grammar.rel == in_grammar.rel)


def test_fix_eps_rules_1():
    with open("tests/eps_in_1") as f:
        in_grammar = CFGrammar(f.read())
    with open("tests/eps_out_1") as f:
        out_grammar = CFGrammar(f.read())
    in_grammar = mutator.fix_eps_rules(in_grammar)
    assert (out_grammar.rel == in_grammar.rel)


def test_fix_eps_rules_2():
    with open("tests/eps_in_2") as f:
        in_grammar = CFGrammar(f.read())
    with open("tests/eps_out_2") as f:
        out_grammar = CFGrammar(f.read())
    in_grammar = mutator.fix_eps_rules(in_grammar)
    assert (out_grammar.rel == in_grammar.rel)


def test_fix_single_rules():
    with open("tests/single_in_1") as f:
        in_grammar = CFGrammar(f.read())
    with open("tests/single_out_2") as f:
        out_grammar = CFGrammar(f.read())
    in_grammar = mutator.fix_single_rules(in_grammar)
    assert (out_grammar.rel == in_grammar.rel)


def test_chomsky_normal_form():
    with open("tests/unified_test_in") as f:
        in_grammar = CFGrammar(f.read())
    with open("tests/unified_test_out") as f:
        out_grammar = CFGrammar(f.read())
    in_grammar = mutator.convert_to_chomsky(in_grammar)
    assert (out_grammar.rel == in_grammar.rel)


def test_very_special_case():
    with open("tests/very_special_case_in") as f:
        in_grammar = CFGrammar(f.read())
    with open("tests/very_special_case_out") as f:
        out_grammar = CFGrammar(f.read())
    in_grammar = mutator.fix_mixed_rules(in_grammar)
    assert (out_grammar.rel == in_grammar.rel)
