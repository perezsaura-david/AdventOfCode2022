import os, argparse
import numpy as np

parser = argparse.ArgumentParser(description='Camp Cleanup')
parser.add_argument('input', help='Input file to read from.')
parser.add_argument('mode', help='1 or 2')

if __name__ == '__main__':
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print('Input file does not exist.')
        exit(1)

    assigment_pairs_found = 0
    with open(args.input, 'r') as f:
        for line in f:
            if line == '\n':
                continue
            line = line.strip()
            pairs = line.split(',')
            elf_0 = np.array(pairs[0].split('-'), int)
            elf_1 = np.array(pairs[1].split('-'), int)

            if args.mode == '1':

                if (elf_0[0] <= elf_1[0]) and (elf_0[1] >= elf_1[1]):
                    print(f'Elf 0: {elf_0} contains Elf 1: {elf_1}')
                    assigment_pairs_found += 1
                elif (elf_1[0] <= elf_0[0]) and (elf_1[1] >= elf_0[1]):
                    print(f'Elf 1: {elf_1} contains Elf 0: {elf_0}')
                    assigment_pairs_found += 1

            if args.mode == '2':

                elf_set_0 = set(range(elf_0[0], elf_0[1] + 1))
                elf_set_1 = set(range(elf_1[0], elf_1[1] + 1))

                if elf_set_0.intersection(elf_set_1):
                    print(f'Elf 0: {elf_0} intersects Elf 1: {elf_1}')
                    assigment_pairs_found += 1

    if args.mode == '1':
        print('Solution 1')
        print(f'Pairs fully contained: {assigment_pairs_found}')
    elif args.mode == '2':
        print('Solution 2')
        print(f'Assignment pairs found: {assigment_pairs_found}')
    else:
        print('Unknown mode.')
        exit(1)

