# try:
#     from cdecimal import Decimal
# except ImportError:
#     from decimal import Decimal
class MyLanguageModel(object):

    """Docstring for MyLanguageModel. """

    def __init__(self, cfd=None, ngram_seq_count=None, alphabet=None):
        """TODO: to be defined1.

        :cfd: NLTK ConditionalFreqDist containing n-gram character counts

        """
        self._cfd = cfd
        self._ngram_seq_count = ngram_seq_count
        self.alphabet = alphabet
        
    def load_cfd(self, cfd, ngram_seq_count=None, alphabet=None):
        """TODO: Docstring for load_cfd.

        :cfd: TODO
        :n_gram_seq_count: TODO
        :returns: TODO

        """
        self._cfd = cfd
        if not ngram_seq_count:
            self._ngram_seq_count = len(cfd.keys()[0]) + 1
        if alphabet:
            self.alphabet = alphabet
        if not self.alphabet:
            raise RuntimeError("need an alphabet")
        return str(self._ngram_seq_count) + '-gram'

    def test(self, test_str):
        """TODO: Docstring for test.

        :test_str: TODO
        :returns: TODO

        """
        return self._cfd[test_str]

    def calculate_probabilities(self, history, lmda=0.01):
        """
        calculate the probability distribution across the alphabet with additive smoothing

        :history: TODO
        :lmda: the lambda value to use for additive smoothing
        :returns: TODO

        """
        # lmda = Decimal(lmda)
        context_len = self._ngram_seq_count -1

        if len(history) < context_len:
            # raise RuntimeError("history is too short for the %d-gram model" % (self._ngram_seq_count))
            return {}

        if isinstance(history, list):
            history = ''.join(history)
        context = history[-context_len:]
        counts = self._cfd[context]  # A NLTK FreqDist object
        # print(counts.items())
        probabilities = {}
        # denom = float(counts.N()) + ( lmda * len(self.alphabet) )
        denom = counts.N() + ( lmda * len(self.alphabet) )
        running_sum = 0
        # for char in self.alphabet:
        for i in xrange(len(self.alphabet)):
            char = self.alphabet[i]
            observed = counts[char]
            # probabilities[char] = Decimal((observed + lmda) / denom)
            # probabilities[char] = (float(observed) + lmda) / denom

            # problem with probabilities not summing to one, trying this:
            # http://stackoverflow.com/questions/17641300/rounding-floats-so-that-they-sum-to-precisely-1
            if i < len(self.alphabet):
                p_i = (float(observed) + lmda) / denom
                p_i = 1.0 - (1.0 - p_i)
                running_sum += p_i
            else:
                p_i = 1 - running_sum
            probabilities[char] = p_i
        # for char, count in counts.iteritems():
        #     probabilities[char] = float(count) / denom
        return probabilities

    # def do_smoothing(self, counts):
    #     """TODO: Docstring for do_smoothing.
    #
    #     :counts: TODO
    #     :returns: TODO
    #
    #     """
    #     for char in self.alphabet:
    #         counts[char] += 1
    #     return counts
