import nltk, pickle, argparse, random

parser = argparse.ArgumentParser(description='test conditional prob dist')
parser.add_argument('fname', type=str, help='pickle file of conditional freq dist')
parser.add_argument('numchars', type=int, help='number of characters to output')
args = parser.parse_args()
fname = args.fname
numchars = args.numchars

with open(fname, 'rb') as f:
    cfd = pickle.load(f)
cpd = nltk.ConditionalProbDist(cfd, nltk.MLEProbDist)

hist = random.choice(cpd.keys())
output = hist
for i in range(numchars):
    next_char = cpd[hist].generate()
    hist = hist[1:] + next_char
    output = output + next_char
print(output)
