import mutator
from cf_grammar import CFGrammar


def test_drop_non_gen():
    with open("mutators/non_gen_in_1") as f:
        in_grammar = CFGrammar(f.read())
    with open("mutators/non_gen_out_1") as f:
        out_grammar = CFGrammar(f.read())
    in_grammar = mutator.drop_non_gen(in_grammar)
    assert (out_grammar.rel == in_grammar.rel)


def test_drop_unreachable():
    with open("mutators/unreachable_in_1") as f:
        in_grammar = CFGrammar(f.read())
    with open("mutators/unreachable_out_1") as f:
        out_grammar = CFGrammar(f.read())
    in_grammar = mutator.drop_unreachable(in_grammar)
    assert (out_grammar.rel == in_grammar.rel)


def test_fix_mixed_rules():
    with open("mutators/mixed_in_1") as f:
        in_grammar = CFGrammar(f.read())
    with open("mutators/mixed_out_1") as f:
        out_grammar = CFGrammar(f.read())
    in_grammar = mutator.fix_mixed_rules(in_grammar)
    assert (out_grammar.rel == in_grammar.rel)


def test_fix_mixed_rules_1():
    with open("mutators/mixed_in_2") as f:
        in_grammar = CFGrammar(f.read())
    with open("mutators/mixed_out_2") as f:
        out_grammar = CFGrammar(f.read())
    in_grammar = mutator.fix_mixed_rules(in_grammar)
    assert (out_grammar.rel == in_grammar.rel)
