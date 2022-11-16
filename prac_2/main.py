import argparse

from cf_grammar import CFGrammar, mutator
from cyk_algo import cyk_check

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='cyk_check',
        description='Check if a phrase is in a language defined grammar',
        epilog='(c) 2022, @vsvood')
    parser.add_argument('grammar', type=str, help='Path to grammar file')
    parser.add_argument('phrase', type=str, help='Phrase to check')
    args = parser.parse_args()
    with open(args.grammar) as f:
        grammar = CFGrammar(f.read())
    grammar = mutator.convert_to_chomsky(grammar)
    print(cyk_check(grammar, args.phrase))
