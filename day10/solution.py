import os, argparse
import numpy as np
import cv2
import imageio

parser = argparse.ArgumentParser(description='Day 0: Template')
parser.add_argument('input', help='Input file to read from.')
parser.add_argument('mode', help='1 or 2')
parser.add_argument('--show', dest='show', action='store_true', help='Show the movements.')
parser.add_argument('--gif', dest='gif', action='store_true', help='Create a gif of the movements.')


class Device:
    def __init__(self, log_cycles):
        self.cycle = 0
        self.x = 1
        self.signal_log = []
        self.log_cycles = log_cycles
        # mode 2
        self.image = np.zeros((6, 40), dtype=np.uint8)
        self.sprite = [self.x -1, self.x, self.x + 1]

    def getCycle(self):
        return self.cycle

    def getX(self):
        return self.x

    def getSignalLog(self):
        return self.signal_log
    
    def calculateSignalStrength(self):
        return self.cycle * self.x

    def incrementCycle(self):
        self.setSprite()
        if self.cycle in self.sprite:
            self.drawPixel(self.image, self.cycle)
        if args.show or args.gif:
            self.showMonitor()
        self.cycle += 1
        if self.cycle in self.log_cycles:
            self.signal_log.append(self.calculateSignalStrength())

    def executeInstruction(self, code):
        instruction = code[0]
        if len(code) > 1:
            value = int(code[1])

        if instruction == 'noop':
            self.noop()
        if instruction == 'addx':
            self.addx(value)
            
    def noop(self):
        instruction_cycles = 1
        for i in range(0, instruction_cycles):
            self.incrementCycle()

    def addx(self, value):
        instruction_cycles = 2 
        for i in range(0, instruction_cycles):
            self.incrementCycle()
        self.x += value

    # mode 2
    def cycle2pixel(self, cycle):
        return [cycle // self.image.shape[1], cycle % self.image.shape[1]]

    def setSprite(self):
        row = self.cycle // self.image.shape[1]
        cycle = self.x + row * self.image.shape[1]
        self.sprite = [cycle-1, cycle, cycle+1]
        print(f'x: {self.x}, sprite: {self.sprite}')
    
    def drawPixel(self, image, cycle):
        pixel = self.cycle2pixel(cycle)
        print(f'drawing pixel: {pixel}')
        image[pixel[0], pixel[1]] = 255

    def drawColorPixel(self, image, cycle, color):
        pixel = self.cycle2pixel(cycle)
        image[pixel[0], pixel[1]] = color 

    # def runCRT(self):
    #     print(f'cycle: {self.cycle}, x: {self.x}')
    def showMonitor(self):
        image = np.zeros((6, 40, 3), dtype=np.uint8)
       
        for sprite in self.sprite:
            color = (0,0,255)
            if sprite < image.shape[1] * image.shape[0]:
                self.drawColorPixel(image, sprite, color)
        color = (0, 255, 0)
        self.drawColorPixel(image, self.cycle, color)
        image[:, :, 0] = self.image

        if args.show:
            cv2.namedWindow('monitor', cv2.WINDOW_KEEPRATIO)
            cv2.imshow('monitor', image)
            cv2.waitKey(0)
        
        if args.gif:
            frame = cv2.resize(image, (0,0), fx=50, fy=50, interpolation=cv2.INTER_NEAREST)
            frames.append(frame)
        
    def getCRT (self):
        cv2.namedWindow('CRT', cv2.WINDOW_KEEPRATIO)
        cv2.imshow('CRT', self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == '__main__':
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print('Input file does not exist.')
        exit(1)

    frames = []

    # if args.mode == '1':
    log_cycles = (20, 60, 100, 140, 180, 220)

    with open(args.input, 'r') as f:
        device = Device(log_cycles)
        for line in f:
            if line == '\n':
                continue
            line = line.strip()
            code = line.split(' ')
            device.executeInstruction(code)
    
    if args.mode == '1':
        print('Solution 1')
        signal_log = device.getSignalLog()
        print(f'Signal log: {signal_log}')
        signal_log_sum = sum(signal_log)
        print(f'Signal log sum: {signal_log_sum}')

    elif args.mode == '2':
        print('Solution 2')
        device.getCRT()
    else:
        print('Unknown mode.')
        exit(1)

    if args.gif:
        print('Creating gif...')
        # convert frames from BGR to RGB
        frames = [cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) for frame in frames]
        imageio.mimsave('CRT.gif', frames, duration=0.1)
