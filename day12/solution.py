import os, argparse
from PIL import Image, ImageDraw
import numpy as np
import cv2

parser = argparse.ArgumentParser(description='Day 12: Hill Climbing Algorithm')
parser.add_argument('input', help='Input file to read from.')
parser.add_argument('mode', help='1 or 2')

class Map():
    
    def __init__(self, width, height, path):
        self.path = path
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
        for i in range(self.path.shape[0]):
            for j in range(self.path.shape[1]):
                # print((i,j), self.path[i,j])
                self.draw_height((i,j), self.path[i,j])

    def draw_height(self, cell, height):
        y = cell[0]
        x = cell[1]
        
        height = int(height) * 9

        x_limits = [(self.cell_size + 1) * x + 1, (self.cell_size + 1) * (x + 1) - 1]
        y_limits = [(self.cell_size + 1) * y + 1, (self.cell_size + 1) * (y + 1) - 1]
        
        self.draw.rectangle((x_limits[0], y_limits[0], x_limits[1], y_limits[1]), fill=(height, height, height))

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

    if "path" in args.input:
        translatePathMap(input_map)
        path_shape = input_map.shape
        # path_shape = path.shape
        # print(f'path_shape {path_shape}')
        path_map = Map(path_shape[1], path_shape[0], input_map)
        path_map.draw_step_map()
        path_map.show_map()

    else:
        # map = translateMap(input_map)
        # print(input_map)
        h_map = translateMap(input_map)
        # print(h_map)
        map_shape = h_map.shape
        # print(f'map_shape {map_shape}')
        height_map = Map(map_shape[1], map_shape[0], h_map)
        height_map.draw_height_map()
        height_map.show_map()
        # map_shape = input_map.shape
        # print(f'map_shape {map_shape}')



    # climbing = HillClimbing()
    # climbing.show_map()

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

