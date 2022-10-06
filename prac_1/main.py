"""This module is responsible for cli interface"""
import argparse
import fileinput
import sys

from automaton_lib import encoder, mutator

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', metavar='<path>', dest='input', help='path to input file')
    parser.add_argument('--input-format', '-if', metavar='<format>', dest='input_format',
                        choices=["doa", "regexp"], default="doa", help='input file format')
    parser.add_argument('--action', '-A', metavar='<action>', dest='action',
                        choices=['reformat', 'determine', 'full_determine', 'min_determine', 'full_min_determine'],
                        default='reformat', help='action to do with imported automaton')
    parser.add_argument('--alphabet', '-a', metavar='<alpha>', dest='alpha', nargs='+',
                        default=['a', 'b'], help='alphabet, required if full_* action specified')
    parser.add_argument('--output', '-o', metavar='<path>', dest='output',
                        help='path to output file')
    parser.add_argument('--output-format', '-of', metavar='<format>', dest='output_format',
                        choices=["doa", "graphviz"], default="graphviz", help='output file format')
    args = parser.parse_args()

    if args.input:
        with open(args.input, 'r') as f:
            data = f.read()
    else:
        data = ''.join(sys.stdin.readlines())

    machine = encoder.decode(data, args.input_format)

    if args.action == "reformat":
        pass
    elif args.action == "determine":
        machine = mutator.strong_determine(machine)
    elif args.action == "full_determine":
        machine = mutator.full_determine(machine, args.alpha)
    elif args.action == "min_determine":
        machine = mutator.minimize_and_determine(machine)
    elif args.action == "full_min_determine":
        machine = mutator.minimize_and_determine(machine)
        machine = mutator.supplement(machine, args.alpha)
    else:
        raise Exception("Unknown action '%s'" % args.action)

    result = encoder.encode(machine, args.output_format)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(result)
    else:
        print(result)
