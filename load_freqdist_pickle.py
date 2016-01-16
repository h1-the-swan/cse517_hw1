import cPickle as pickle
from nltk import FreqDist, ConditionalFreqDist

# http://stackoverflow.com/questions/20716812/saving-and-loading-multiple-objects-in-python-pickle-file/28745948
def pkl_load(fname):
    with open(fname, 'rb') as f:
        while True:
            try:
                yield pickle.load(f)
            except EOFError:
                break

def load_cfd(fname):
    items = pkl_load(fname)
    cfd = ConditionalFreqDist()
    for item in items:
        # backward compatibility:
        if isinstance(item, ConditionalFreqDist):
            cfd = item
            return cfd
        k = item[0]
        fd = item[1]
        cfd[k] = fd
    return cfd
