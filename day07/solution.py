import os, argparse

parser = argparse.ArgumentParser(description='')
parser.add_argument('input', help='Input file to read from.')
parser.add_argument('mode', help='')

class Node:
    def __init__(self, name):
        self.name = name
        self.weight = 0
        self.parent = None
        self.children = None

    def get_name(self):
        return self.name

    def get_weight(self):
        return self.weight

    def get_parent(self):
        return self.parent

    def get_children(self):
        return self.children

    def set_weight(self, weight):
        self.weight = weight

    def set_parent(self, parent):
        self.parent = parent

    def set_children(self, children):
        self.children = children

class DirectoryTree:
    def __init__(self):
        self.root = '/'
        self.nodes = {}
        self.edges = {}

    def add_node(self, node):
        self.nodes[name] = Node(name)

    def represent(self):
        return self.name


if __name__ == '__main__':
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print('Input file does not exist.')
        exit(1)

    with open(args.input, 'r') as f:
        for line in f:
            if line == '\n':
                continue
            if line.startswith('$'):
                processCommand(line)

    if args.mode == '1':
        print('Solution 1')
    elif args.mode == '2':
        print('Solution 2')
    else:
        print('Unknown mode.')
        exit(1)

