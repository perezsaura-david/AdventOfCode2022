import os, argparse
import numpy as np
from visualizer import Visualizer

parser = argparse.ArgumentParser(description='Day 5: Supply Stacks')
parser.add_argument('input', help='Input file to read from.')
parser.add_argument('mode', help=' 1: single block move, 2: multiple block move')

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

def getMoveInfo(file_line):

    file_line = file_line.strip()
    info = file_line.split(' ')
    move = np.array(info[1::2], int) 

    return move

def makeStructure(structure):
    columns_id = structure[0]
    
    columns = []
    for i in range(len(columns_id)):
        column = []
        for row in reversed(structure[:-1]):
            if row[i] != None:
                column.append(row[i])
        columns.append(column)

    return columns

def moveBlocks(structure, move, mode):

    quantity = move[0]
    column_start = move[1] - 1
    column_end = move[2] - 1

    # print("Quantity: ", quantity)
    # print("Column start: ", column_start)
    # print("Column end: ", column_end)

    if mode == 1:
        for i in range(quantity):
            block = structure[column_start][-1]
            # print(f'block: {block}')
            structure[column_start].pop()
            structure[column_end].append(block)
            # print(f'structure after block moved: {structure}')
    if mode == 2:
        blocks = structure[column_start][-quantity:]
        # print(f'blocks: {blocks}')
        structure[column_start] = structure[column_start][:-quantity]
        structure[column_end] += blocks
        # print(f'structure after blocks moved: {structure}')

    return

def visualizeStorage(storage, visualizer, time):
    visualizer.setStorage(cargo_structure)
    visualizer.drawStorage()
    visualizer.show(time)

def getMaxRows(structure):
    max_rows = 0
    for column in structure:
        if len(column) > max_rows:
            max_rows = len(column)
    return max_rows

if __name__ == '__main__':
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print('Input file does not exist.')
        exit(1)

    visualize_moves = True

    structure_info = []
    reconstruction = True
    with open(args.input, 'r') as f:
        for line in f:
            if line == '\n':
                reconstruction = False
                cargo_structure = makeStructure(structure_info)
                
                if visualize_moves: 
                    max_rows = getMaxRows(cargo_structure)
                    visualizer = Visualizer(len(cargo_structure), max_rows ,int(args.mode))
                continue

            if reconstruction:
                structure_info.append(getStorageInfo(line))
            else:
                move = getMoveInfo(line)
                moveBlocks(cargo_structure, move, int(args.mode))
                if visualize_moves:
                    visualizeStorage(cargo_structure, visualizer, 500)


    if args.mode == '1':
        print('Solution 1')
        print(f'Final structure: {cargo_structure}')
        # for column in cargo_structure:
            # print(f'Column {column} last block: {column[-1]}')
        last_blocks = ''
        for column in cargo_structure:
            last_blocks += column[-1]
        print(f'Last blocks: {last_blocks}')
    elif args.mode == '2':
        print('Solution 2')
        print(f'Final structure: {cargo_structure}')
        last_blocks = ''
        for column in cargo_structure:
            last_blocks += column[-1]
        print(f'Last blocks: {last_blocks}')
    else:
        print('Unknown mode.')
        exit(1)

    max_rows = 0
    for column in cargo_structure:
        if len(column) > max_rows:
            max_rows = len(column)

    visualizer = Visualizer(len(cargo_structure), max_rows ,int(args.mode))
    visualizeStorage(cargo_structure, visualizer, 0)
