import os, argparse
from PIL import Image, ImageDraw
import numpy as np
import cv2
import time

parser = argparse.ArgumentParser(description='Day 12: Hill Climbing Algorithm')
parser.add_argument('input', help='Input file to read from.')
parser.add_argument('mode', help='1 or 2')

class HillClimbing():

    def __init__(self, h_map):
        self.graph = {}
        self.costs = {}
        self.nodes = set()
        self.parents = {}
        self.map = h_map
        self.start = None
        self.goal = None
        self.make_graph()
        self.init_costs()
        self.init_parents()

        # print("Graph: ", self.graph)
        # print("Costs: ", self.costs)
        # print("Nodes: ", self.nodes)
        # print("Parents: ", self.parents)
        print("Start: ", self.start)
        print("Goal: ", self.goal)

        print("Number of nodes: ", len(self.nodes))
        print("Number of edges: ", len(self.graph))
        print("Number of parents: ", len(self.parents))

        # Measure execution time
        start = time.time()
        self.dijkstra_algorithm()
        end = time.time()
        print("Execution time in seconds: ", end - start)

        # print("Costs: ", self.costs)
        # print("Nodes: ", self.nodes)
        # print("Parents: ", self.parents)


    def make_graph(self):
        print("Making graph...")
        # row_len = self.map.shape[0]
        for i in range(self.map.shape[0]):
            for j in range(self.map.shape[1]):
                # node_id = i * row_len + j
                # print(node_id)
                node_id = (i, j)
                self.nodes.add(node_id)
                self.graph[node_id] = {}
                self.costs[node_id] = float('inf')
                self.parents[node_id] = None
                node_value = self.map[i, j]
                # print("Node id: ", node_id, "Node value: ", node_value)
                if node_value == 0:
                    self.start = node_id
                if node_value == 27:
                    self.goal = node_id
                # Add the left cell
                if j > 0:
                    # print("Left node")
                    candidate_value = self.map[i, j-1]
                    candidate_id = (i, j-1)
                    # candidate_id = i * row_len + j - 1
                    diff = candidate_value - node_value
                    # print("Node id: ", node_id, "Candidate id: ", candidate_id, "Diff: ", diff)
                    if diff <= 1: 
                        self.graph[node_id][candidate_id] = 1
                # Add the right cell
                if j < self.map.shape[1] - 1:
                    # print("Right node")
                    candidate_value = self.map[i, j+1]
                    candidate_id = (i, j+1)
                    # candidate_id = i * row_len + j + 1
                    diff = candidate_value - node_value
                    # print("Node id: ", node_id, "Candidate id: ", candidate_id, "Diff: ", diff)
                    if diff <= 1:
                        self.graph[node_id][candidate_id] = 1
                # Add the top cell
                if i > 0:
                    # print("Top node")
                    candidate_value = self.map[i-1, j]
                    candidate_id = (i-1, j)
                    # candidate_id = (i-1) * row_len + j
                    diff = candidate_value - node_value
                    # print("Node id: ", node_id, "Candidate id: ", candidate_id, "Diff: ", diff)
                    if diff <= 1:
                        self.graph[node_id][candidate_id] = 1
                # Add the bottom cell
                if i < self.map.shape[0] - 1:
                    # print("Bottom node")
                    candidate_value = self.map[i+1, j]
                    candidate_id = (i+1, j)
                    # candidate_id = (i+1) * row_len + j
                    diff = candidate_value - node_value
                    # print("Node id: ", node_id, "Candidate id: ", candidate_id, "Diff: ", diff)
                    if diff <= 1:
                        self.graph[node_id][candidate_id] = 1

    def init_costs(self):
        self.costs[self.start] = 0
        for node in self.graph[self.start]:
            self.costs[node] = 1

    def init_parents(self):
        for node in self.graph[self.start]:
            self.parents[node] = self.start
            
    def dijkstra_algorithm(self):
        print("Dijkstra algorithm...")
        visited=[]

        node=self.find_cheaper_node(visited)
        while node is not None:
            print("Visiting node: ", node)
            node_cost = self.costs[node]
            neighbors = self.graph[node]
            for n in neighbors.keys():
                print("Neighbor: ", n)
                new_cost = node_cost+neighbors[n]
                if self.costs[n] > new_cost:
                    self.costs[n] = new_cost
                    self.parents[n] = node
            visited.append(node)
            node = self.find_cheaper_node(visited)
            print("Visited: ", len(visited))

    def find_cheaper_node(self, visited):
        minimum_cost = float("inf")
        minimun_cost_node = None
        for node in self.costs:
            if node in visited:
                # print("Node already visited: ", node)
                continue
            node_cost = self.costs[node]
            if node_cost < minimum_cost: 
                minimum_cost = node_cost
                minimun_cost_node = node
        
        return minimun_cost_node
    
    def find_best_path(self): 
        print("Finding best path...")
      
        path = []
        node = self.goal 
        
        while node != self.start:
            parent = self.parents[node]
            path.append(node)
            node = parent
        
        path.append(self.start)
        
        return path[::-1]

    def get_path_steps(self):
        return self.costs[self.goal]

class Map():
    
    def __init__(self, width, height, hmap):
        self.map = hmap
        self.cell_size = 50
        image_width = width * (self.cell_size + 1) + 1  
        image_height = height * (self.cell_size + 1) + 1
        self.image = Image.new('RGB', (image_width, image_height), color =  'black')
        self.draw = ImageDraw.Draw(self.image)
        self.draw_grid(width, height, self.cell_size)
        # self.draw_step_map()

    def draw_grid(self, width, height, cell_size):
        for x in range(0, width * (cell_size + 1) + 1, cell_size + 1):
            self.draw.line((x, 0, x, height * (cell_size + 1)), fill='white')
        for y in range(0, height * (cell_size + 1) + 1, cell_size + 1):
            self.draw.line((0, y, width * (cell_size + 1), y), fill='white')

    def draw_height_map(self):
        for i in range(self.map.shape[0]):
            for j in range(self.map.shape[1]):
                # print((i,j), self.path[i,j])
                self.draw_height((i,j), self.map[i,j])

    def draw_height(self, cell, height):
        y = cell[0]
        x = cell[1]
        
        height = int(height) * 9

        x_limits = [(self.cell_size + 1) * x + 1, (self.cell_size + 1) * (x + 1) - 1]
        y_limits = [(self.cell_size + 1) * y + 1, (self.cell_size + 1) * (y + 1) - 1]
        
        self.draw.rectangle((x_limits[0], y_limits[0], x_limits[1], y_limits[1]), fill=(height, height, height))

    def draw_step(self, cell):
        y = cell[0]
        x = cell[1]

        # y = cell // self.map.shape[1]
        # x = cell % self.map.shape[1]

        height = int(self.map[y,x]) * 6 + 60

        x_limits = [(self.cell_size + 1) * x + 1, (self.cell_size + 1) * (x + 1) - 1]
        y_limits = [(self.cell_size + 1) * y + 1, (self.cell_size + 1) * (y + 1) - 1]
        
        self.draw.rectangle((x_limits[0], y_limits[0], x_limits[1], y_limits[1]), fill=(height, 0, 0))

    def draw_path(self, path):
        print("Drawing path...")
        for step in path:
            # print("Drawing step: ", step)
            self.draw_step(step)




    def draw_step_map(self):
        for i in range(self.path.shape[0]):
            for j in range(self.path.shape[1]):
                # print((i,j), self.path[i,j])
                self.draw_map_step((i,j), self.path[i,j])


    def draw_map_step(self, cell, step):
        # print(f'Drawing step {step} at {cell}')

        if step == '.':
            return

        y = cell[0]
        x = cell[1]

        offset = 10

        x_limits = [(self.cell_size + 1) * x + offset, (self.cell_size + 1) * (x + 1) - offset]
        y_limits = [(self.cell_size + 1) * y + offset, (self.cell_size + 1) * (y + 1) - offset]

        if cell == (0,0):
            self.draw.rectangle((x_limits[0], y_limits[0], x_limits[1], y_limits[1]), fill='green')

        if step == 'S':
            self.draw.rectangle((x_limits[0], y_limits[0], x_limits[1], y_limits[1]), fill='green')
            return
        elif step == 'E':
            self.draw.rectangle((x_limits[0], y_limits[0], x_limits[1], y_limits[1]), fill='red')
            return
        
        step = int(step)

        if step == 0: # up
            # draw triangle
            left = (x_limits[0], y_limits[1])
            right = (x_limits[1], y_limits[1])
            top = (x_limits[0] + (x_limits[1] - x_limits[0]) // 2, y_limits[0])
            self.draw.polygon([left, right, top], fill='white')
        elif step == 2: # down
            # draw triangle
            left = (x_limits[0], y_limits[0])
            right = (x_limits[1], y_limits[0])
            bottom = (x_limits[0] + (x_limits[1] - x_limits[0]) // 2, y_limits[1])
            self.draw.polygon([left, right, bottom], fill='white')
        elif step == 3: # right
            # draw triangle
            left = (x_limits[0], y_limits[0])
            top = (x_limits[0], y_limits[1])
            right = (x_limits[1], y_limits[0] + (y_limits[1] - y_limits[0]) // 2)
            self.draw.polygon([left, top, right], fill='white')
        elif step == 1: # left
            # draw triangle
            left = (x_limits[0], y_limits[0] + (y_limits[1] - y_limits[0]) // 2)
            top = (x_limits[1], y_limits[0])
            right = (x_limits[1], y_limits[1])
            self.draw.polygon([left, top, right], fill='white')

    def show_map(self):
        # na = np.array(self.image)
        # cv2.imshow('image', na)
        # cv2.waitKey(0)
        self.image.show()

def parseFile(file):
    content = []
    with open(file) as f:
        for line in f:
            row = []
            if line == '\n':
                continue
            line = line.strip()
            for i in line:
                row.append(i)
            content.append(row)
    content_array = np.array(content)
    return content_array

def translatePathMap(path):
    for i in range(path.shape[0]):
        for j in range(path.shape[1]):
            if path[i,j] == '^':
                path[i,j] = 0
            elif path[i,j] == '<':
                path[i,j] = 1
            elif path[i,j] == 'v':
                path[i,j] = 2
            elif path[i,j] == '>':
                path[i,j] = 3
        # elif path[i] == 'S':
            # path[i] = 'S'
    # print(path)
    # return path

def translateMap(input_map):
    output_map = np.zeros(input_map.shape)
    for i in range(input_map.shape[0]):
        for j in range(input_map.shape[1]):
            if  input_map[i,j] == 'S':
                output_map[i,j] = int(0)
            elif input_map[i,j] == 'E':
                output_map[i,j] = int(ord('z') - ord('a')) + 2
            else:
                value = ord(input_map[i,j]) - ord('a') + 1 
                # value = value * 9 
                # print(input_map[i,j], value)
                output_map[i,j] = int(value)
    return output_map
   

if __name__ == '__main__':
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print('Input file does not exist.')
        exit(1)
    
    input_map = parseFile(args.input)
    hill_map = None

    if "path" in args.input:
        # Show path example
        translatePathMap(input_map)
        path_shape = input_map.shape
        path_map = Map(path_shape[1], path_shape[0], input_map)
        path_map.draw_step_map()
        path_map.show_map()
        exit(0)

    h_map = translateMap(input_map)
    map_shape = h_map.shape
    height_map = Map(map_shape[1], map_shape[0], h_map)
    height_map.draw_height_map()
    height_map.show_map()
    print(f'Hill map: {h_map}')

    climbing = HillClimbing(h_map)
    path = climbing.find_best_path()
    print("Path: ", path)
    print("Path steps: ", climbing.get_path_steps())

    height_map.draw_path(path)
    height_map.show_map()



    if args.mode == '1':
        print('Solution 1')
    elif args.mode == '2':
        print('Solution 2')
    else:
        print('Unknown mode.')
        exit(1)

