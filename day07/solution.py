import os, argparse

parser = argparse.ArgumentParser(description='')
parser.add_argument('input', help='Input file to read from.')
parser.add_argument('mode', help='')

class Node:
    def __init__(self, name, parent=None, weight=0): 
        self.name = name
        self.weight = weight
        self.parent = parent
        self.children = []

    def get_name(self):
        return self.name

    def get_weight(self):
        return self.weight

    def get_parent(self):
        return self.parent

    def get_children(self):
        return self.children

    def is_folder(self):
        return self.is_folder

    def set_parent(self, parent):
        self.parent = parent

    def set_children(self, children):
        self.children = children

    def add_child(self, child):
        self.children.append(child)

class DirectoryTree:
    def __init__(self):
        self.root = '/'
        self.current_folder = '/'
        self.nodes = {}
        self.edges = {}

    def add_node(self, name, weight=0):
        if name == self.root:
            node_name = self.root
            # print(f'Adding node {node_name} with weight {weight}')
            self.nodes[node_name] = Node(name)
            return

        parent = self.current_folder
        node_name = parent + name
        # if weight == 0:
            # node_name += '/'
        # print(f'Adding node {node_name} with weight {weight}')
        self.nodes[node_name] = Node(name, parent, weight)
        # self.nodes[name].set_parent(self.current_folder)

    def cd(self, name):
        if name == '..':
            self.current_folder = self.nodes[self.current_folder].get_parent()
        else:
            if name != self.root:
                name = self.current_folder + name + '/'
                # print(f'Changing directory to {name}')
            if name not in self.nodes:
                # print(f'Node {name} does not exist.')
                self.add_node(name, 0)
            self.current_folder = name

    # def setFolderWeight(self, folder, weight):
    #     self.nodes[folder].set_weight(weight)

    def get_current_folder(self):
        return self.current_folder

    def get_folder_weight(self, folder):
        folder_weight = 0
        # print(f'Getting weight of {folder}')
        # print(f'Children of {folder}: {self.nodes[folder].get_children()}')
        for node_name in self.nodes[folder].get_children():
            node = self.nodes[node_name]
            node_weight = node.get_weight()
            if node.get_weight() == 0:
                # print(f'Node {node_name} has no weight, getting weight of children.')
                node_weight = self.get_folder_weight(node_name)
                # print(f'Folder {node_name} has weight {node_weight}')
            folder_weight += node_weight
        return folder_weight

    def represent_tree(self):
        print(f'Directory tree:')
        node_id = self.root
        self.represent_node(node_id, 0)

    def represent_node(self, node_id, indent):
        node = self.nodes[node_id]
        node_name = node.get_name()
        node_weight = node.get_weight()
        if node_weight == 0:
            if node_name == self.root:
                node_string = f'(root){node_name}'
                # print(f'{node_name} (root)')
            else:
                node_string = f'{node_name}'
                # print(f'{node_name}')
                # print(' '*indent + f'{node_name}/')
            node_weight = self.get_folder_weight(node_id)
            print(' '*indent + node_string + ' '*20 + f' [content: {node_weight}]')
        else:
            print(' '*indent + f'{node_name} ({node_weight})')
        # print(f'Node children: {node.get_children()}')
        for child_id in node.get_children():
            # child_name = node_name + child_name
            self.represent_node(child_id, indent+2)
        return 

    # def processCommand(self, line):

def addFolderContent(tree, folder):
    
    # print(f'Processing folder {folder}')

    folder_weight = 0

    for entry in folder:
        entry = entry.strip()
        if entry == '':
            continue
        entry = entry.split(' ')
        node_name = entry[1]
        if entry[0] == 'dir':
            node_name += '/'
            tree.add_node(node_name)
        else:
            file_weight = int(entry[0])
            tree.add_node(node_name, file_weight)
        node_name = tree.current_folder + node_name
        tree.nodes[tree.current_folder].add_child(node_name)
            # folder_weight += file_weight
            # folder_weight += file_weight

    # tree.setFolderWeight(tree.getCurrentFolder(), folder_weight)


if __name__ == '__main__':
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print('Input file does not exist.')
        exit(1)

    directory_tree = DirectoryTree()
    folder_content = [] 
    fill_content = False

    with open(args.input, 'r') as f:
        for line in f:
            if line == '\n':
                continue
            line = line.strip()
            if line.startswith('$'):
                if fill_content:
                    addFolderContent(directory_tree, folder_content)
                    folder_content = []
                    fill_content = False
                command = line.split(' ')[1:]
                # print(command)
                if command[0] == 'cd':
                    directory_tree.cd(command[1])
                if command[0] == 'ls':
                    folder_content = []
                    fill_content = True
                    continue
            if fill_content:
                folder_content.append(line)
        # If the file ends with a folder, add it to the tree
        if fill_content:
            addFolderContent(directory_tree, folder_content)
            folder_content = []
            fill_content = False

    directory_tree.represent_tree()

    # mode 1
    max_weight = 100000
    max_target_weight = 0  
    # mode 2
    total_disk_space = 70000000
    update_size = 30000000 
    used_space = directory_tree.get_folder_weight(directory_tree.root)
    free_space = total_disk_space - used_space
    min_weight = update_size - free_space
    print(f'Used space: {used_space}')
    print(f'Free space: {free_space}')
    print(f'Minimum weight: {min_weight}')
    min_target_weight = used_space

    if args.mode == '1':
        print(f'Looking for target folders [max weight={max_weight}]')
    if args.mode == '2':
        print(f'Looking for target folders [min weight={min_weight}]')
    for node_name in directory_tree.nodes:
        node = directory_tree.nodes[node_name]
        if node.get_weight() == 0:
            folder_weight = directory_tree.get_folder_weight(node_name)
            if args.mode == '1':
                if folder_weight <= max_weight:
                    print(f'Folder {node_name} has weight {folder_weight}')
                    max_target_weight += folder_weight
            if args.mode == '2':
                if folder_weight >= min_weight:
                    print(f'Folder {node_name} has weight {folder_weight}')
                    if folder_weight < min_target_weight:
                        min_target_weight = folder_weight
                 

    if args.mode == '1':
        print('Solution 1')
        print(f'Total weight of target folders: {max_target_weight}')
    elif args.mode == '2':
        print('Solution 2')
        print(f'Minimun weight target folder: {min_target_weight}')
        print(f'New free space: {total_disk_space - used_space + min_target_weight}')
    else:
        print('Unknown mode.')
        exit(1)

