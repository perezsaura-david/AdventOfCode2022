import os, argparse
import numpy as np

parser = argparse.ArgumentParser(description='Day 8: Treetop Tree House')
parser.add_argument('input', help='Input file to read from.')
parser.add_argument('mode', help='1 or 2')

def checkTreeVisibility(grid, i, j):
    height = grid[i][j]
    
    visibility = np.ones(4, int)
    # check if it visible from the left
    v_i = 0
    for k in range(j):
        if grid[i][k] >= height:
            visibility[v_i] = 0
            break
    # check if it visible from the right
    v_i += 1
    for k in range(j+1, len(grid[i])):
        if grid[i][k] >= height:
            visibility[v_i] = 0
            break
    # check if it visible from the top
    v_i += 1
    for k in range(i):
        if grid[k][j] >= height:
            visibility[v_i] = 0
            break
    # check if it visible from the bottom
    v_i += 1
    length = len(grid)
    for k in range(i+1, len(grid)):
        if grid[k][j] >= height:
            visibility[v_i] = 0
            break
    
    return visibility

def findVisibleTrees(grid):
    
    visible_trees = []

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            tree_visibility = checkTreeVisibility(grid, i, j)
            if np.sum(tree_visibility) > 0: 
                visible_trees.append((i, j))

    return visible_trees


def countTreeVisibility(grid, i, j):
    height = grid[i][j]
    
    visibility = np.zeros(4, int)
    # check if it visible from the left
    v_i = 0
    for k in reversed(range(j)):
        visibility[v_i] += 1
        if grid[i][k] >= height:
            break
    # check if it visible from the right
    v_i += 1
    for k in range(j+1, len(grid[i])):
        visibility[v_i] += 1
        if grid[i][k] >= height:
            break
    # check if it visible from the top
    v_i += 1
    for k in reversed(range(i)):
        visibility[v_i] += 1
        if grid[k][j] >= height:
            break
    # check if it visible from the bottom
    v_i += 1
    length = len(grid)
    for k in range(i+1, len(grid)):
        visibility[v_i] += 1
        if grid[k][j] >= height:
            break

    # print(visibility)

    return visibility


def findHighestScore(grid):

    max_score = 0

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            visibility = countTreeVisibility(grid, i, j)
            score = 1
            for v in visibility:
                score *= v
            if score > max_score:
                max_score = score

    return max_score

if __name__ == '__main__':
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print('Input file does not exist.')
        exit(1)

    with open(args.input, 'r') as f:
        rows = []
        for line in f:
            if line == '\n':
                continue
            line = line.strip()
            row = []
            for c in line:
                row.append(int(c))
            rows.append(row)

        grid = np.array(rows)
        
        print(f'Forest shape: {grid.shape}')
       
        if args.mode == '1':
            visibleTrees = findVisibleTrees(grid)
        if args.mode == '2':
            highest_score = findHighestScore(grid)


    if args.mode == '1':
        print('Solution 1')
        print(f'Number of visible trees: {len(visibleTrees)}')
    elif args.mode == '2':
        print('Solution 2')
        print(f'Highest score: {highest_score}')
    else:
        print('Unknown mode.')
        exit(1)

