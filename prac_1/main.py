"""This module is responsible for cli interface"""
import argparse
from state_machine_utils import *


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', metavar='<path>', dest='input', help='Path to input file')
    parser.add_argument('--input-format', '-if', metavar='<format>', dest='input_format',
                        choices=['doa'], default='doa', help='input file format')
    parser.add_argument('--output', '-o', metavar='<path>', dest='output', help='Path to input file')
    parser.add_argument('--output-format', '-of', metavar='<format>', dest='output_format',
                        choices=['doa'], default='doa', help='input file format')
    args = parser.parse_args()

    data = ""
    if args.input:
        with open(args.input, 'r') as f:
            data = f.read()
    else:
        data = '\n'.join(iter(input, ''))

    if args.input_format == "doa":
        machine = build_nfa_from_doa(data)
    else:
        raise Exception("Unknown format '%s'" % args.input_format)

    if args.output_format == "doa":
        result = convert_nfa_to_doa(machine)
    else:
        raise Exception("Unknown format '%s'" % args.output_format)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(result)
    else:
        print(result)
