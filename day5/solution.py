import os, argparse

parser = argparse.ArgumentParser(description='')
parser.add_argument('input', help='Input file to read from.')
parser.add_argument('mode', help='')

def getStorageInfo(file_line):
    row = []
    space_counter = 0
    for c in file_line:
        if c == ' ':
            space_counter += 1
            if space_counter == 4:
                row.append(None)
                space_counter = 0
        elif c == '[' or c == ']' or c == '\n':
            space_counter = 0
            continue
        else:
            row.append(c)
            space_counter = 0
    return row

def makeStructure(structure_info):
    columns_id = structure_info[0]
    
    columns = []
    for i in range(len(columns_id)):
        column = []
        for row in reversed(structure_info[:-1]):
            print(row)
            if row[i] != None:
                column.append(row[i])
        columns.append(column)

    print(columns)
    return


if __name__ == '__main__':
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print('Input file does not exist.')
        exit(1)

    structure = []
    reconstruction = True
    with open(args.input, 'r') as f:
        for line in f:
            if line == '\n':
                reconstruction = False
                # print(structure)
                makeStructure(structure)
            if reconstruction:
                structure.append(getStorageInfo(line))

    if args.mode == '1':
        print('Solution 1')
    elif args.mode == '2':
        print('Solution 2')
    else:
        print('Unknown mode.')
        exit(1)

