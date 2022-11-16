from cf_grammar import CFGrammar, mutator
from cyk_algo import cyk_check

with open("tests/unified_test_in") as f:
    grammar = CFGrammar(f.read())
grammar = mutator.convert_to_chomsky(grammar)
print(grammar)

with open("tests/test") as f:
    count = 0
    for line in f.readlines():
        count += 1
        print(count)
        phrase, truth = line.split()
        assert cyk_check(grammar, phrase) != truth
