import os, argparse
import numpy as np

parser = argparse.ArgumentParser(description='Day 11: Monkey in the Middle')
parser.add_argument('input', help='Input file to read from.')
parser.add_argument('mode', help='1 or 2')

class Operation:
    def __init__(self, op, arg):
        self.operate = None
        self.arg = None 
        if op == '+':
            self.operate = self.sum
            self.arg = int(arg)
        elif op == '*':
            if arg == 'old':
                self.operate = self.square
            else:
                self.operate = self.product
                self.arg = int(arg)
        else:
            raise Exception(f'Invalid operation {op}')


    def sum(self,item):
        # print(f'Summing {item}+{self.arg} = {item+self.arg}')
        return item + self.arg
    def product(self,item):
        # print(f'Multiplying {item}*{self.arg} = {item*self.arg}')
        return item * self.arg
    def square(self,item):
        # print(f'Squaring {item} = {item*item}')
        return item * item

class Monkey():
    def __init__(self, name):
        self.name = name 
        self.items = []
        self.operation = None
        self.test_number = 0
        self.moves = np.array([0,0])
        self.inspections = 0
    
    def setOperation(self, op):
        self.operation = op

    def setTestNumber(self, number):
        self.test_number = number

    def setMove(self, move, index):
        self.moves[index] = move

    def getItemToInspect(self):
        if len(self.items) == 0:
            item = None
        else:
            item = self.items[0]
            self.removeItem(item)
        return item
    
    def getNextMonkey(self, index):
        return self.moves[index]

    def getInspections(self):
        return self.inspections

    def addItem(self, item):
        # print(f'Monkey {self.name} is getting {item}')
        self.items.append(item)

    def removeItem(self, item):
        # print(f'Monkey {self.name} extracting {item}')
        self.items.remove(item)

    def inspection(self, item):
        inspected_item = item 
        self.inspections += 1
        # print(f'Monkey {self.name} is inspecting {inspected_item}')
        return self.operation.operate(inspected_item)

    def testing(self, item):
        # print(f'Monkey {self.name} is testing {item}')
        rest = item % self.test_number
        # print(f'Rest of {item}/{self.test_number} is {rest}')
        if rest == 0:
            return True
        else:
            return False

class KeepAway():
    def __init__(self, name):
        self.monkeys = []

    def addMonkey(self, monkey):
        self.monkeys.append(monkey)

    def getMonkey(self, name):
        for monkey in self.monkeys:
            if monkey.name == name:
                return monkey

    def getMonkeys(self):
        return self.monkeys

    def round(self):
        for monkey in self.monkeys:
            # print(f'\n**** Round for monkey {monkey.name} ****\n')
            while len(monkey.items) > 0:
                items = monkey.items
                # print(f'*** Monkey {monkey.name} has {items} ***')
                next_monkey_index = 0
                item = monkey.getItemToInspect()
                if item is None:
                    continue
                item = monkey.inspection(item)
                # item //= 3
                if not monkey.testing(item):
                    next_monkey_index = 1
                monkey_name = monkey.getNextMonkey(next_monkey_index)
                receiver_monkey = self.getMonkey(monkey_name)
                receiver_monkey.addItem(item)

if __name__ == '__main__':
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print('Input file does not exist.')
        exit(1)

    monkeys = []

    with open(args.input, 'r') as f:
        for line in f:
            if line == '\n':
                continue
            line = line.strip()
            if 'Monkey' in line:
                monkeys.append(Monkey(int(line[-2])))
                continue
            if 'items' in line:
                split_line = line.split(':')
                items = split_line[1].replace(' ', '').split(',')
                for item in items:
                    monkeys[-1].addItem(int(item))
                continue
            if 'Operation' in line:
                split_line = line.split('=')
                operation = split_line[1].split(' ')[-2:]
                op = operation[0]
                arg = operation[1]
                monkeys[-1].setOperation(Operation(op, arg))
                continue
            if 'Test' in line:
                split_line = line.split(' ')
                monkeys[-1].setTestNumber(int(split_line[-1]))
                continue
            if 'true' in line:
                line = line.strip()
                monkeys[-1].setMove(int(line[-1]), 0)
                continue
            if 'false' in line:
                line = line.strip()
                monkeys[-1].setMove(int(line[-1]), 1)
                continue
    
    keepaway = KeepAway('KeepAway')

    for monkey in monkeys:
        keepaway.addMonkey(monkey)
        
        # print(f'Monkey {monkey.name}: {monkey.items}')
        # print(f'Inspection: {monkey.inspection()}')
        # print(f'Testing: {monkey.testing(monkey.inspection())}')
        # print(f'Moves: {monkey.moves}')

    rounds = 10000

    for i in range(rounds):
        # print('***************')
        # print(f'*** Round {i+1} ***')
        # print('***************')
        keepaway.round()
        # if i % 1000 == 999:
        if i % 10 == 9:
            print(f'*** Round {i+1} ***')
            for monkey in keepaway.getMonkeys():
                print(f'Monkey {monkey.name} has {monkey.items}')
                print(f'Monkey {monkey.name} has inspected {monkey.getInspections()} items')

    print('***************')
    print('*** Results ***')
    print('***************')

    inspections = []
    for monkey in keepaway.getMonkeys():
        print(f'Monkey {monkey.name} has inspected {monkey.getInspections()} items')
        inspections.append(monkey.getInspections())

    inspections.sort(reverse=True)
    first_inspector = inspections[0]
    second_inspector = inspections[1]

    print(f'First inspector: {first_inspector}')
    print(f'Second inspector: {second_inspector}')

    monkey_business = first_inspector * second_inspector

    if args.mode == '1':
        print('Solution 1')
        print(f'Monkey business: {monkey_business}')
    elif args.mode == '2':
        print('Solution 2')
    else:
        print('Unknown mode.')
        exit(1)

