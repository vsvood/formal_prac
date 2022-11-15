import mutator
from cf_grammar import CFGrammar

with open("tests/mutators/CBS") as f:
    grammar = CFGrammar(f.read())
grammar = mutator.convert_to_chomsky(grammar)
print(grammar)
