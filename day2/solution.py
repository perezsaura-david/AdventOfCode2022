import os, argparse

parser = argparse.ArgumentParser(description='')
parser.add_argument('input', help='Input file to read from.')
parser.add_argument('mode', help='')

if __name__ == '__main__':
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print('Input file does not exist.')
        exit(1)

    elves=[]
    with open(args.input, 'r') as f:
        for line in f:
            if line == '\n':
                continue

    if args.mode == '1':
        print('Solution 1')
    elif args.mode == '2':
        print('Solution 2')
    else:
        print('Unknown mode.')
        exit(1)

