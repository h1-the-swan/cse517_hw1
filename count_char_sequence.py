import argparse, sys, codecs, time
import cPickle as pickle
from nltk import ConditionalFreqDist, FreqDist
from datetime import datetime

start = time.time()

parser = argparse.ArgumentParser(description='count sequences of characters')
parser.add_argument('fname', type=str, help='text file of natural language')
parser.add_argument('seq_length', type=int, help='length of character sequence to count')
parser.add_argument('-v', '--verbose', help='verbose output', action='store_true')
args = parser.parse_args()
fname = args.fname
seq_length = args.seq_length
verbose = args.verbose

def progressbar_init(maxval=None):
    try:
        from progressbar import ProgressBar, Bar, ETA, Percentage, Timer
        if maxval:
            widgets = ['Progress: ', Percentage(), ' ', Bar(), ' ' , Timer()]
        else:
            widgets = ['Progress: ', Bar(), ' ', Timer()]
        pbar = ProgressBar(widgets=widgets, maxval=maxval)
        return pbar
    except ImportError:
        return None

with codecs.open(fname, 'r', 'utf-8') as f:
    text = f.read()

if seq_length > 1:
    if verbose:
        print(datetime.now())
        print("Reading n-grams (seq_length %d) from file: %s" %(seq_length, fname))
        sys.stdout.flush()
    ngrams = nltk.ngrams(text, seq_length)
    if verbose:
        print("done")
        sys.stdout.flush()
    freq_dist = ConditionalFreqDist()
    # c = 0
    # pbar = progressbar_init()
    if verbose:
        print("storing in FreqDist")
        sys.stdout.flush()
    c = 0
    for gram in ngrams:
        first_elem = list(gram[:-1])
        # exclude ngrams with stop character (unless it's in the final position)
        if u'\u0003' not in first_elem:
            first_elem = ''.join(first_elem)
            second_elem = gram[-1]
            freq_dist[first_elem][second_elem] += 1
        c += 1
        if verbose:
            if ( c in [20, 100, 1000, 10000, 100000, 1000000] ) or ( c % 10000000 == 0 ):
                print("%d ngrams processed" %(c))
                sys.stdout.flush()

    fname = 'freq_dist_' + str(seq_length) + 'gram.pickle'
    # with open(fname, 'wb') as outf:
    #     if verbose:
    #         print("pickling to %s" %(fname))
    #     sys.stdout.flush()
    #     pickle.dump(freq_dist, outf)
    #
    # The above is giving memory errors
    # Trying instead to iterate and save multiple pickles
    # http://stackoverflow.com/questions/20716812/saving-and-loading-multiple-objects-in-python-pickle-file/28745948
    with open(fname, 'wb') as outf:
        if verbose:
            print("pickling to %s" %(fname))
            sys.stdout.flush()
        num_conditions = len(freq_dist)
        if verbose:
            print("%d items to pickle" %(num_conditions))
        c = 1
        for k in freq_dist:
            # fd = {k: freq_dist[k]}
            fd = (k, freq_dist[k])
            pickle.dump(fd, outf)
            c+=1
            if verbose:
                if ( c in [20, 100, 1000, 10000] ) or ( c % 100000 == 0 ):
                    print("%d items pickled" % (c))
                    sys.stdout.flush()
elif seq_length == 1:
    # unigram case
    if verbose:
        print(datetime.now())
        print("Reading unigrams from file: %s" %(fname))
        sys.stdout.flush()
    fd = FreqDist()
    c = 0
    for char in text:
        c += 1
        fd[char] += 1
        if verbose:
            if ( c in [20, 100, 1000, 10000, 100000, 1000000] ) or ( c % 10000000 == 0 ):
                print("%d ngrams processed" %(c))
                sys.stdout.flush()
    fname = 'freq_dist_' + str(seq_length) + 'gram.pickle'
    with open(fname, 'wb') as outf:
        if verbose:
            print("pickling to %s" %(fname))
        sys.stdout.flush()
        pickle.dump(fd, outf)

end = time.time()
if verbose:
    print("total time: %.2f seconds" %(end-start))
    sys.stdout.flush()
