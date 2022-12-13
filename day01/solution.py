import os, argparse

parser = argparse.ArgumentParser(description='Day 1: Calorie Counting')
parser.add_argument('input', help='Input file to read from.')
parser.add_argument('mode', help='"top1" or "top3"')

if __name__ == '__main__':
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print('Input file does not exist.')
        exit(1)

    elves=[]
    with open(args.input, 'r') as f:
        calories = 0
        for line in f:
            if line == '\n':
                elves.append(calories)
                calories = 0
                continue
            calories += int(line)

    if args.mode == 'top1':
        print('The elf carriying most Calories is index:',elves.index(max(elves)))
        print('He is carriying',max(elves),'Calories.')
    elif args.mode == 'top3':
        elves.sort(reverse=True)
        print('Top3 Elves calories are:')
        print(elves[:3])
        print('Total calories:',sum(elves[:3]))
    else:
        print('Unknown mode.')
        exit(1)

