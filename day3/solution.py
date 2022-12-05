import os, argparse

parser = argparse.ArgumentParser(description='Rucksack reorganization')
parser.add_argument('input', help='Input file to read from.')
parser.add_argument('mode', help='')


def getValue(item):
    a_value = ord('a')
    A_value = ord('A')

    if i.islower():
        ref_value = a_value - 1
    else:
        ref_value = A_value - 27

    item_value = ord(i) - ref_value

    return item_value


if __name__ == '__main__':
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print('Input file does not exist.')
        exit(1)
   
    priorities = 0

    if args.mode == '1':
        with open(args.input, 'r') as f:
            for line in f:
                if line == '\n':
                    continue
                line = line.strip()
                line_lenth = len(line)
                set0 = set(line[0:line_lenth//2])
                set1 = set(line[line_lenth//2:])
                item = set0.intersection(set1)
                print(item)
                for i in item:
                    item_value = getValue(i)
                    print(item_value)
                    priorities += item_value
    if args.mode == '2':
        with open(args.input, 'r') as f:
            group= []
            for line in f:
                if len(group) < 3:
                    group.append(set(line.strip()))
                if len(group) == 3:
                    item = set.intersection(*group)
                    print(item)
                    for i in item:
                        item_value = getValue(i)
                        print(item_value)
                        priorities += item_value
                    group = []

    if args.mode == '1':
        print('Solution 1')
        print(f'Sum of priorities: {priorities}')
    elif args.mode == '2':
        print('Solution 2')
        print(f'Sum of priorities: {priorities}')
    else:
        print('Unknown mode.')
        exit(1)

