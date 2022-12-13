import os, argparse

parser = argparse.ArgumentParser(description='Day 6: Tuning Trouble')
parser.add_argument('input', help='Input file to read from.')
parser.add_argument('mode', help='1 or 2')

if __name__ == '__main__':
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print('Input file does not exist.')
        exit(1)

    if args.mode == '1':
        start_of_packet = 4
    if args.mode == '2':
        start_of_packet = 14

    characters=[]
    with open(args.input, 'r') as f:
        for line in f:
            print('new line')
            characters = []
            if line == '\n':
                continue
            for i in range(len(line)):
                characters.append(line[i])
                if len(characters) < start_of_packet:
                    continue
                set_characters = set(characters)
                characters = characters[-start_of_packet+1:]
                if len(set_characters) == start_of_packet:
                    print('Last start packet character is number: {}'.format(i))
                    break
                    



    if args.mode == '1':
        print('Solution 1')
        print(f'First marker after character: {i+1}')
    elif args.mode == '2':
        print('Solution 2')
        print(f'First marker after character: {i+1}')
    else:
        print('Unknown mode.')
        exit(1)

