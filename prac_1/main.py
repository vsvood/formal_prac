"""This module is responsible for cli interface"""
import argparse
import encoder
import mutator

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', metavar='<path>', dest='input', help='Path to input file')
    parser.add_argument('--input-format', '-if', metavar='<format>', dest='input_format',
                        choices=['doa'], default='doa', help='input file format')
    parser.add_argument('--output', '-o', metavar='<path>', dest='output',
                        help='Path to input file')
    parser.add_argument('--output-format', '-of', metavar='<format>', dest='output_format',
                        choices=['doa'], default='doa', help='input file format')
    args = parser.parse_args()

    if args.input:
        with open(args.input, 'r') as f:
            data = f.read()
    else:
        data = '\n'.join(iter(input, ''))

    if args.input_format == "doa":
        machine = encoder.decode(data)
    else:
        raise Exception("Unknown format '%s'" % args.input_format)

    machine = mutator.minimize_and_determine(machine, {'a', 'b'})

    if args.output_format == "doa":
        result = encoder.encode(machine)
    else:
        raise Exception("Unknown format '%s'" % args.output_format)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(result)
    else:
        print(result)
