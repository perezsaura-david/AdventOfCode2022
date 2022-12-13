import os, argparse

parser = argparse.ArgumentParser(description='Day 2: Rock Paper Scissors')
parser.add_argument('input', help='Input file to read from.')
parser.add_argument('mode', help='1 or 2.')

plays = ['R', 'P', 'S']
results = ['Lose','Draw','Win']

opp_code = ['A','B','C']
pick_code = ['X','Y','Z']
res_code = ['X','Y','Z']
res_counter = [2,0,1]

def getRoundScore(opponent, pick):

    opp_play = plays[opp_code.index(opponent)]
    print('opp:',opp_play)
    if opp_play == None:
        print('Invalid opponent pick: {}'.format(opponent))
        return None

    play = plays[pick_code.index(pick)]
    print('play:',play)
    if play == None:
        print('Invalid pick: {}'.format(pick))
        return None

    for i in range(0,3):
        if plays[(plays.index(opp_play)+i)%3] == play:
            result_index = res_counter.index(i)
            break

    print('Result:',res_code[result_index])
    result_score = 3*result_index
    pick_score = pick_code.index(pick)+1

    return pick_score+result_score

def getPick(opponent, result):
    
    opp_pick = plays[opp_code.index(opponent)]
    print('opp:',opp_pick)
    if opp_pick == None:
        print('Invalid opponent pick: {}'.format(opponent))
        return None

    result_counter = res_counter[res_code.index(result)]
    if result_counter == None:
        print('Invalid result: {}'.format(result))
        return None

    play = plays[(plays.index(opp_pick)+result_counter)%3]
    print('play:',play)
    pick = pick_code[plays.index(play)]
    return pick



if __name__ == '__main__':
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print('Input file does not exist.')
        exit(1)

    with open(args.input, 'r') as f:
        score = 0
        opp, pick = None, None
        for line in f:
            if args.mode == '1':
                opp, pick = line.split()
            if args.mode == '2':
                opp, result = line.split()
                print(opp, result)
                pick = getPick(opp, result)
                print(pick)

            if opp is not None and pick is not None:
                round_score = getRoundScore(opp, pick)
                if round_score is None:
                    exit(1)
            else:
                print('Invalid input.')
                exit(1)
            score += round_score

    if args.mode == '1':
        print('Solution 1')
        print('Score: {}'.format(score))

    elif args.mode == '2':
        print('Solution 2')
        print('Score: {}'.format(score))
    else:
        print('Unknown mode.')
        exit(1)

