import argparse, sys, codecs, time
import cPickle as pickle
import nltk

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

if verbose:
    print("Reading n-grams (seq_length %d)" %(seq_length))
    sys.stdout.flush()
ngrams = nltk.ngrams(text, seq_length)
if verbose:
    print("done")
    sys.stdout.flush()
freq_dist = nltk.ConditionalFreqDist()
c = 0
pbar = progressbar_init()
if verbose:
    print("storing in FreqDist")
    sys.stdout.flush()
c = 0
for gram in ngrams:
    first_elem = list(gram[:-1])
    first_elem = ''.join(first_elem)
    second_elem = gram[-1]
    freq_dist[first_elem][second_elem] += 1
    c += 1
    if verbose:
        if ( c in [20, 100, 1000, 10000, 100000, 1000000] ) or ( c % 100000000 == 0 ):
            print("%d ngrams processed" %(c))
            sys.stdout.flush()

fname = 'freq_dist_' + str(seq_length) + 'gram.pickle'
with open(fname, 'wb') as outf:
    if verbose:
        print("pickling to %s" %(fname))
    sys.stdout.flush()
    pickle.dump(freq_dist, outf)

end = time.time()
if verbose:
    print("total time: %.2f seconds" %(end-start))
    sys.stdout.flush()
