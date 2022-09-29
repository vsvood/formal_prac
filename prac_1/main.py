"""This module is responsible for cli interface"""
import argparse
import fileinput

from automaton_lib import encoder, mutator

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', metavar='<path>', dest='input', help='Path to input file')
    parser.add_argument('--input-format', '-if', metavar='<format>', dest='input_format',
                        choices=['doa'], default='doa', help='input file format')
    parser.add_argument('--action', '-A', metavar='<action>', dest='action',
                        choices=['determine', 'full_determine', 'min_determine', 'full_min_determine'],
                        default='full_min_determine', help='action to do with imported automaton')
    parser.add_argument('--alphabet', '-a', metavar='<alpha>', dest='alpha', nargs='+',
                        default=['a', 'b'], help='action to do with imported automaton')
    parser.add_argument('--output', '-o', metavar='<path>', dest='output',
                        help='Path to input file')
    parser.add_argument('--output-format', '-of', metavar='<format>', dest='output_format',
                        choices=['doa'], default='doa', help='input file format')
    args = parser.parse_args()

    if args.input:
        with open(args.input, 'r') as f:
            data = f.read()
    else:
        data = ''.join(fileinput.input())

    if args.input_format == "doa":
        machine = encoder.decode(data)
    else:
        raise Exception("Unknown format '%s'" % args.input_format)

    if args.action == "determine":
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

    if args.output_format == "doa":
        result = encoder.encode(machine)
    else:
        raise Exception("Unknown format '%s'" % args.output_format)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(result)
    else:
        print(result)
