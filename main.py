import sys, argparse, pickle, math
import numpy as np
from get_bmp_alphabet import get_bmp_alphabet
from load_freqdist_pickle import load_cfd
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

def load_model():
    """TODO: Docstring for function.

    :returns: TODO

    """
    alphabet = get_bmp_alphabet()
    model = MyLanguageModel(alphabet=alphabet)
    # with open('freq_dist_4gram.pickle', 'rb') as f:
    #     cfd = pickle.load(f)
    cfd = load_cfd('freq_dist_4gram.pickle')
    model.load_cfd(cfd)
    return model

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

def generate_character(history, model):
    """TODO: Docstring for generate_character.
    :returns: TODO

    """
    ###
    probabilities = model.calculate_probabilities(history)
    if probabilities:
        p = []
        for char in alphabet:
            p.append(probabilities[char])
        gen = np.random.choice(alphabet, p=p)
        sys.stdout.write(gen)
        sys.stdout.write(u'\n')
        sys.stdout.flush()
        # history = history + gen
        history.append(gen)
    else:
        print('history is too short, and this is unhandled. TODO: fix this')
    return history

def observe_character(history, character, model):
    """TODO: Docstring for observe_character.

    :character: TODO
    :returns: TODO

    """
    if character == u'\u0003':
        history = []
    else:
        probabilities = model.calculate_probabilities(history)
        if probabilities:
            prob = probabilities[character]
            logprob = math.log(prob, 2 )
            sys.stdout.write('log probability for %s: %.6f' %(character, logprob))
        history.append(character)
    sys.stdout.write(u'\n')
    sys.stdout.flush()
    return history

def query_character(history, character, model):
    """TODO: Docstring for query_character.

    :character: TODO
    :returns: TODO

    """
    probabilities = model.calculate_probabilities(history)
    if probabilities:
        prob = probabilities[character]
        logprob = math.log(prob, 2)
        sys.stdout.write('log probability for %s: %.6f' %(character, logprob))
    sys.stdout.write(u'\n')
    sys.stdout.flush()
    return

def command_line(history):
    """TODO: Docstring for command_line.
    :returns: TODO

    """
    while True:
        get_user_input(history)

def process_commands(model, commands, history=[]):
    """TODO: Docstring for process_commands.

    :commands: TODO
    :history: TODO
    :returns: TODO

    """
    i = 0
    while i < len(commands):
        command = commands[i]
        # print(command)
        if command == u'g':
            history = generate_character(history, model)
        elif command == u'x':
            if isinstance(history, list):
                print(''.join(history))
            else:
                print(history)
            sys.exit(0)
        elif command == u'o':
            i += 1
            character = commands[i]
            history = observe_character(history, character, model)
        elif command == u'q':
            i += 1
            character = commands[i]
            query_character(history, character, model)
        i += 1

def test():
    history = u'It was the best of timom '
    alphabet = get_bmp_alphabet()
    model = MyLanguageModel(alphabet=alphabet)
    with open('freq_dist_4gram.pickle', 'rb') as f:
        cfd = pickle.load(f)
    model.load_cfd(cfd)
    print('loaded model')
    for i in range(50):
        probabilities = model.calculate_probabilities(history)
        # print('got probabilities, len %d' %(len(probabilities)))
        # sum = 0
        # for k, v in probabilities.iteritems():
        #     sum += v
        # if sum > 0.999999:
        #     print('sums to one')
        p = []
        for char in alphabet:
            p.append(probabilities[char])
        # print(probabilities[u'.'])
        gen = np.random.choice(alphabet, p=p)
        # print(gen)
        # print(ord(gen))
        history = history + gen
        print(history)

    print(history)
    sys.exit()


if __name__ == "__main__":
    history = []
    model = load_model()
    # command_line(history)
    # test()
    commands = sys.stdin.read()
    commands = to_unicode(commands)

    process_commands(model, commands, history)
