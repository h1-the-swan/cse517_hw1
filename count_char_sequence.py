import argparse, sys, codecs, pickle
import nltk

parser = argparse.ArgumentParser(description='count sequences of characters')
parser.add_argument('fname', type=str, help='text file of natural language')
parser.add_argument('seq_length', type=int, help='length of character sequence to count')
args = parser.parse_args()
fname = args.fname
seq_length = args.seq_length

with codecs.open(fname, 'r', 'utf-8') as f:
    text = f.read()

ngrams = nltk.ngrams(text, seq_length)
freq_dist = nltk.ConditionalFreqDist()
for gram in ngrams:
    first_elem = list(gram[:-1])
    first_elem = ''.join(first_elem)
    second_elem = gram[-1]
    freq_dist[first_elem][second_elem] += 1

with open('freq_dist_' + str(seq_length) + 'gram.pickle', 'wb') as outf:
    pickle.dump(freq_dist, outf)
