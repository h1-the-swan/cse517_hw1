class MyLanguageModel(object):

    """Docstring for MyLanguageModel. """

    def __init__(self, cfd=None, ngram_seq_count=None):
        """TODO: to be defined1.

        :cfd: NLTK ConditionalFreqDist containing n-gram character counts

        """
        self._cfd = cfd
        self._ngram_seq_count = ngram_seq_count
        
    def load_cfd(self, cfd, ngram_seq_count=None):
        """TODO: Docstring for load_cfd.

        :cfd: TODO
        :n_gram_seq_count: TODO
        :returns: TODO

        """
        self._cfd = cfd
        if not ngram_seq_count:
            self._ngram_seq_count = len(cfd.keys()[0]) + 1
        return str(self._ngram_seq_count) + '-gram'

    def test(self, test_str):
        """TODO: Docstring for test.

        :test_str: TODO
        :returns: TODO

        """
        return self._cfd[test_str]
