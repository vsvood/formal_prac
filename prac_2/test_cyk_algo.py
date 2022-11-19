from cf_grammar import CFGrammar, mutator
from cyk_algo import cyk_check


def test_cyk_algo():
    with open("tests/unified_test_out") as f:
        grammar = CFGrammar(f.read())

    with open("tests/test") as f:
        lines = f.readlines()
        for idx, line in enumerate(lines):
            phrase, truth = line.split()
            assert cyk_check(grammar, phrase) != truth
