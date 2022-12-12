import os, argparse
import numpy as np
import cv2
import imageio

parser = argparse.ArgumentParser(description='Day 9: Rope Bridge')
parser.add_argument('input', help='Input file to read from.')
parser.add_argument('mode', help='1 or 2')
parser.add_argument('--show', dest='show', action='store_true', help='Show the movements.')
parser.add_argument('--gif', dest='gif', action='store_true', help='Create a gif of the movements.')

def generateSteps(move):
    direction = move[0]
    number_of_moves = int(move[1])
    steps = []
    # R +x, L -x
    if direction == 'R':
        step = [1, 0]
    elif direction == 'L':
        step = [-1, 0]
    # U +y, D -y
    elif direction == 'U':
        step = [0, 1]
    elif direction == 'D':
        step = [0, -1]

    for i in range(number_of_moves):
        steps.append(step)

    return steps

def calculatePositions(steps, head_positions, tail_positions):

    print(f'head_positions: {head_positions}')
    print(f'tail_positions: {tail_positions}')

    current_head = head_positions[-1]
    current_tail = tail_positions[-1]

    for step in steps:
        next_head = [current_head[0] + step[0], current_head[1] + step[1]]

        distance = np.array((abs(next_head[0] - current_tail[0]),abs(next_head[1] - current_tail[1])))
        if max(distance) > 1:
            current_tail = current_head

        current_head = next_head

        head_positions.append(current_head)
        tail_positions.append(current_tail)
        first_step = False

    return

def showMovements(head_positions, tail_positions):

    frames = []

    # max_x = max([abs(x[0]) for x in head_positions])
    # max_y = max([abs(x[1]) for x in head_positions])
    max_x = max([x[0] for x in head_positions + tail_positions])
    max_y = max([x[1] for x in head_positions + tail_positions])
    min_x = min([x[0] for x in head_positions + tail_positions])
    min_y = min([x[1] for x in head_positions + tail_positions])

    # print(f'Max x: {max_x}, Max y: {max_y}')
    # print(f'Min x: {min_x}, Min y: {min_y}')

    # image_size = (max_y * 2 + 1, max_x * 2 + 1, 3)
    image_size = (max_y - min_y + 1, max_x - min_x + 1, 3)

    image = np.zeros(image_size, dtype=np.uint8)

    if range(len(head_positions)) != range(len(tail_positions)):
        print('Error: head and tail positions do not match.')
        return

    for i in range(len(head_positions)):
        head = head_positions[i]
        tail = tail_positions[i]

        # h_y = max_y - head[1]
        # h_x = max_x + head[0]
        # t_y = max_y - tail[1]
        # t_x = max_x + tail[0]

        h_y = head[1] - min_y
        h_x = head[0] - min_x
        t_y = tail[1] - min_y
        t_x = tail[0] - min_x

        tail_color = (0,255,0)
        head_color = (255,0,0)

        if i == 0:
            head_color = (0,0,255)

        image[t_y, t_x] = tail_color
        image[h_y, h_x] = head_color

        cv2.namedWindow('image', cv2.WINDOW_KEEPRATIO)
        
        cv2.imshow('image', image)
        key = cv2.waitKey(100)
        if key == 27 or key == ord('q'):
            break

        if args.gif:
            # Sometimes crashes
            frame = cv2.resize(image, (0,0), fx=50, fy=50, interpolation=cv2.INTER_NEAREST)
            frames.append(frame)

        image = image * 0

    return frames

def calculateRopePositions(steps, rope_positions):

    for step in steps:
        for i in range(len(rope_positions)):
            if i == 0:
                next_position = [rope_positions[i][-1][0] + step[0], rope_positions[i][-1][1] + step[1]]
            else: 
                 
                rope_step =  np.zeros((2), np.int32) 
                distance = np.array((rope_positions[i-1][-1][0] - rope_positions[i][-1][0],
                                     rope_positions[i-1][-1][1] - rope_positions[i][-1][1]))
                if np.linalg.norm(distance) < 2:
                    rope_step *= 0
                else:
                    index = np.argwhere(distance == 0)
                    if index != []:
                        rope_step[index] = 0
                    else:
                        rope_step = np.sign(distance)


                # for index in range(len(distance)):
                #     if distance[index] > 1:
                #         rope_step[index] = 1
                
                

                # if np.linalg.norm(distance) == 1:
                #     rope_step *= 0
                # else:
                #     index = np.argwhere(distance == 0) 
                #     if index != []:
                #         rope_step[index] = 0

                # rope_step = rope_step * np.sign(distance)
                    
                # index = np.argwhere(distance > 1)
                # rope_step[index] += 1
                # print(f'index: {index}')
                # print(f'rope_step: {rope_step}')
                next_position = [rope_positions[i][-1][0] + rope_step[0], 
                                 rope_positions[i][-1][1] + rope_step[1]]
                # print(f'next_position: {next_position}')
                # if max(distance) > 1:
                #     next_position = rope_positions[i-1][-2]
                # else:
                #     next_position = rope_positions[i][-1]

            rope_positions[i].append(next_position)

    return


def showRopeMovement(rope_positions):

    frames = []

    max_x = max([x[0] for x in rope_positions[0]])
    max_y = max([x[1] for x in rope_positions[0]])
    min_x = min([x[0] for x in rope_positions[0]])
    min_y = min([x[1] for x in rope_positions[0]])

    image_size = (max_y - min_y + 1, max_x - min_x + 1, 3)

    image = np.zeros(image_size, dtype=np.uint8)

    for i in range(len(rope_positions[0])):
        for j in reversed(range(len(rope_positions))):
            x,y = rope_positions[j][i]

            r_y = max_y - y
            r_x = x - min_x

            rope_color = (0,255,0)

            if j == 0:
                rope_color = (255,0,0)
            if j == len(rope_positions) - 1:
                rope_color = (0,0,255)

            image[r_y, r_x] = rope_color

        cv2.namedWindow('image', cv2.WINDOW_KEEPRATIO)
            
        cv2.imshow('image', image)
        key = cv2.waitKey(100)
        if key == 27 or key == ord('q'):
            break

        if args.gif:
            # Sometimes crashes
            frame = cv2.resize(image, (0,0), fx=50, fy=50, interpolation=cv2.INTER_NEAREST)
            frames.append(frame)

        image = image * 0

    return frames




if __name__ == '__main__':
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print('Input file does not exist.')
        exit(1)

    show_movements = args.show
    make_gif = args.gif

    if args.mode == '1':

        H_positions = [[0,0]]
        T_positions = [[0,0]]
        with open(args.input, 'r') as f:
            for line in f:
                if line == '\n':
                    continue
                line = line.strip()
                move = line.split(' ')
                steps = generateSteps(move)
                calculatePositions(steps, H_positions, T_positions)
        set_tail = set([tuple(x) for x in T_positions])

    if args.mode == '2':

        rope_positions = [np.zeros((10,2), dtype=np.int32)]
        rope_positions = []
        for i in range(10):
            rope_positions.append([[0,0]])
        with open(args.input, 'r') as f:
            for line in f:
                if line == '\n':
                    continue
                line = line.strip()
                move = line.split(' ')
                steps = generateSteps(move)
                calculateRopePositions(steps, rope_positions)
        set_tail = set([tuple(x) for x in rope_positions[-1]])

    number_of_tail_positions = len(set_tail)

    if args.mode == '1':
        print('Solution 1')
        print(f'Number of tail positions: {number_of_tail_positions}')
    elif args.mode == '2':
        print('Solution 2')
        print(f'Number of tail positions: {number_of_tail_positions}')
    else:
        print('Unknown mode.')
        exit(1)

    if show_movements:
        # images = showMovements(H_positions, T_positions)
        images = showRopeMovement(rope_positions)
        if make_gif:
            imageio.mimsave('rope_bridge.gif', images, duration=0.1)
