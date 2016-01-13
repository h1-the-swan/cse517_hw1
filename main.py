import sys, argparse, pickle
import numpy as np
from get_bmp_alphabet import get_bmp_alphabet
from myLanguageModel import MyLanguageModel

parser = argparse.ArgumentParser(description='CSE517 HW1')
parser.add_argument('random_seed', type=int, help='Seed for the random number generator')
args = parser.parse_args()
np.random.seed(args.random_seed)

alphabet = get_bmp_alphabet()

# help from http://farmdev.com/talks/unicode/
def to_unicode(obj, encoding='utf-8'):
    if isinstance(obj, basestring):
        if not isinstance(obj, unicode):
            obj = unicode(obj, encoding)
    return obj

def get_user_input(history):
    error = 'Invalid input'
    command = raw_input(':')
    command = to_unicode(command)
    if len(command) == 1:
        if command == u'g':
            history = generate_character(history)
        elif command == u'x':
            sys.exit(0)
        else:
            print(error)
    elif len(command) == 2:
        if command[0] == u'o':
            history = observe_character(history, command[1])
        elif command[0] == u'q':
            query_character(history, command[1])
        else:
            print(error)
    elif command == u'history':
        print(history)
    else:
        print(error)
    return history

def generate_character(history):
    """TODO: Docstring for generate_character.
    :returns: TODO

    """
    ###
    return history

def observe_character(history, character):
    """TODO: Docstring for observe_character.

    :character: TODO
    :returns: TODO

    """
    if character == u'\u0003':
        history = []
    else:
        history.append(character)
    sys.stdout.write(u'\n')
    return history

def query_character(history, character):
    """TODO: Docstring for query_character.

    :character: TODO
    :returns: TODO

    """
    pass

def command_line(history):
    """TODO: Docstring for command_line.
    :returns: TODO

    """
    while True:
        get_user_input(history)

def process_commands(commands, history=[]):
    """TODO: Docstring for process_commands.

    :commands: TODO
    :history: TODO
    :returns: TODO

    """
    i = 0
    while i < len(commands):
        command = commands[i]
        print(command)
        if command == u'g':
            history = generate_character(history)
        elif command == u'x':
            print(history)
            sys.exit(0)
        elif command == u'o':
            i += 1
            character = commands[i]
            history = observe_character(history, character)
        elif command == u'q':
            i += 1
            character = commands[i]
            query_character(history, character)
        i += 1

def test():
    history = 'It was the best of times'
    alphabet = get_bmp_alphabet()
    model = MyLanguageModel(alphabet=alphabet)
    with open('freq_dist_4gram.pickle', 'rb') as f:
        cfd = pickle.load(f)
    model.load_cfd(cfd)
    print('loaded model')
    probabilities = model.calculate_probabilities(history)
    print('got probabilities, len %d' %(len(probabilities)))
    sum = 0
    for k, v in probabilities.iteritems():
        sum += v
    if sum > 0.999999:
        print('sums to one')
    sys.exit()


if __name__ == "__main__":
    history = []
    # command_line(history)
    test()
    commands = sys.stdin.read()
    commands = to_unicode(commands)

    process_commands(commands, history)
