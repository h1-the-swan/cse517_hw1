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

    def calculate_probabilities(self, history):
        """TODO: Docstring for calculate_probabilities.

        :history: TODO
        :returns: TODO

        """
        context_len = self._ngram_seq_count -1

        if len(history) < context_len:
            raise RuntimeError("history is too short for the %d-gram model" % (self._ngram_seq_count))

        if isinstance(history, list):
            history = ''.join(history)
        context = history[-context_len:]
        counts = self._cfd[context]  # A NLTK FreqDist object
        counts = self.do_smoothing(counts)
        probabilities = {}
        denom = counts.N()
        for char, count in counts.iteritems():
            probabilities[char] = float(count) / denom
        return probabilities

    def do_smoothing(self, counts):
        """TODO: Docstring for do_smoothing.

        :counts: TODO
        :returns: TODO

        """
        for char in self.alphabet:
            counts[char] += 1
        return counts
