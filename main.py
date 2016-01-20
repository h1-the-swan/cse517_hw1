import sys, argparse, math, time
import numpy as np
from get_bmp_alphabet import get_bmp_alphabet
from load_freqdist_pickle import load_cfd
from interpolatedModel import InterpolatedModel
# from myLanguageModel import MyLanguageModel
# from unigramModel import UnigramModel
try:
    import cPickle as pickle
except ImportError:
    import pickle

parser = argparse.ArgumentParser(description='CSE517 HW1')
parser.add_argument('random_seed', type=int, help='Seed for the random number generator')
parser.add_argument('-n', '--ngram', type=int, choices=xrange(2,9), help='n (int) to use for the ngram (default 2: bigram)')
parser.add_argument('-v', '--verbose', help='verbose output for debugging', action='store_true')
args = parser.parse_args()
np.random.seed(args.random_seed)
ngram_n = 2
if args.ngram:
    ngram_n = args.ngram
verbose = args.verbose

alphabet = get_bmp_alphabet()

# help from http://farmdev.com/talks/unicode/
def to_unicode(obj, encoding='utf-8'):
    if isinstance(obj, basestring):
        if not isinstance(obj, unicode):
            obj = unicode(obj, encoding)
    return obj

def output(out_str):
    if not isinstance(out_str, basestring):
        out_str = str(out_str)
    sys.stdout.write(out_str.encode('utf-8'))
    sys.stdout.flush()

def load_interpolated_model(num_models=3, model_weights=None):
    alphabet = get_bmp_alphabet()
    model = InterpolatedModel(alphabet=alphabet, highest_order=num_models, model_weights=model_weights)
    return model

# def load_model(ngram_n=ngram_n):
#     """TODO: Docstring for function.
#
#     :returns: TODO
#
#     """
#     alphabet = get_bmp_alphabet()
#     model = MyLanguageModel(alphabet=alphabet)
#     # with open('freq_dist_4gram.pickle', 'rb') as f:
#     #     cfd = pickle.load(f)
#     cfd = load_cfd('freq_dist_%dgram.pickle' %(ngram_n))
#     model.load_cfd(cfd)
#     return model
#
# def load_unigram_model():
#     alphabet = get_bmp_alphabet()
#     unigram = UnigramModel(alphabet=alphabet)
#     with open('freq_dist_1gram.pickle', 'rb') as f:
#         fd = pickle.load(fd)
#     unigram.load_fd(fd)
#     return unigram
#
# def load_multiple_models(highest_order=3):
#     with open('freq_dist_1gram.pickle', 'rb') as f:
#         unigram_fd = pickle.load(f)
#     unigram = load_unigram_model()
#     models = [unigram]
#     for i in range(2, highest_order+1):
#         model = load_model(i)
#         models.append(model)
#     return models

# def interpolate_models(models, history, model_weights=None, character=None):
#     # returns logprob of character if character is specified
#     # else returns a dictionary of the probability distribution for all characters
#     #
#     # model_weights is a list of len(models) numbers that sum to one
#     # one weight for [1-gram, 2-gram, ..., highest_order_gram]
#     # defaults to equal weights for all:
#     if not model_weights:
#         num_models = len(models)
#         model_weights = [1.0 / num_models for i in range(num_models)]
#
#     if character:
#         # unigram first
#         p = models[0].probabilities[character] * model_weights[0]
#         # now all the others
#         for model in models:
#             probs = model.calculate_probabilities(history)
#             p += probs[character] * model_weights[0]
#         logprob = math.log(p, 2)
#         return logprob

        

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
    probabilities = model.calculate_probability(history=history, character=None)
    if probabilities:
        p = []
        for char in alphabet:
            p.append(probabilities[char])
        gen = np.random.choice(alphabet, p=p)
        # sys.stdout.write(gen)
        # sys.stdout.write(u'\n')
        # sys.stdout.flush()
        # history = history + gen
        # history.append(gen)
        out_str = gen
        if verbose:
            out_str = out_str + "// generated unicode character %d" %(ord(gen))
        out_str = out_str + u'\n'
        output(out_str)
        history = observe_character(history, gen, model)
    else:
        print('history is too short, and this is unhandled. TODO: fix this')
    return history

def observe_character(history, character, model):
    """TODO: Docstring for observe_character.

    :character: TODO
    :returns: TODO

    """
    if character == u'\u0003':
        if verbose:
            output(u'// Clearing history')
        history = []
    else:
        # probabilities = model.calculate_probabilities(history)
        # if probabilities:
        #     prob = probabilities[character]
        #     logprob = math.log(prob, 2 )
        #     if verbose:
        #         out_str = "// added character %s to history (logprob %.3f)" %(character, logprob)
        #         output(out_str)
        #     # sys.stdout.write('log probability for %s: %.6f' %(character, logprob))
        # history.append(character)
        if verbose:
            logprob = model.calculate_probability(history=history, character=character)
            out_str = "// added character %s to history (logprob %.3f)" %(character, logprob)
            output(out_str)
        history.append(character)

    output(u'\n')
    return history

def query_character(history, character, model):
    """TODO: Docstring for query_character.

    :character: TODO
    :returns: TODO

    """
    # probabilities = model.calculate_probabilities(history)
    # if probabilities:
    #     prob = probabilities[character]
    #     logprob = math.log(prob, 2)
    #     # sys.stdout.write('log probability for %s: %.6f' %(character, logprob))
    #     output(str(logprob))
    # output(u'\n')
    logprob = model.calculate_probability(history=history, character=character)
    output(logprob)
    output(u'\n')
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
            if verbose:
                if isinstance(history, list):
                    output(''.join(history))
                else:
                    output(history)
                end = time.time()
                if verbose:
                    output('total time %.2f seconds' %(end-start))
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


def print_time_from_start(start):
    print('%.2f seconds from start' %(time.time()-start))

if __name__ == "__main__":
    history = []
    # model_weights = [0.1, 0.2, 0.3, 0.4]
    # model_weights = [0.1, 0.1, 0.2, 0.3, 0.3]
    model_weights = None
    # model = load_model()
    start = time.time()
    model = load_interpolated_model(num_models=5, model_weights=model_weights)
    if verbose:
        print_time_from_start(start)
    # command_line(history)
    # test()
    commands = sys.stdin.read()
    commands = to_unicode(commands)

    process_commands(model, commands, history)
