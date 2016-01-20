class UnigramModel(object):

    """Docstring for UnigramModel. """

    def __init__(self, fd=None, alphabet=None, probabilities=None):
        """TODO: to be defined1.

        :fd: TODO
        :alphabet: TODO

        """
        self._fd = fd
        self.alphabet = alphabet
        self.probabilities = probabilities
        
    def load_fd(self, fd, alphabet=None):
        self._fd = fd
        if alphabet:
            self.alphabet = alphabet
        if not self.alphabet:
            raise RuntimeError("need an alphabet")
        self.probabilities = self.calculate_probabilities()
        return
    
    def calculate_probabilities(self, lmda=0.0001):
        """TODO: Docstring for calculate_probabilities.

        :returns: TODO

        """
        probabilities = {}
        counts = self._fd
        denom = counts.N() + ( lmda * len(self.alphabet) )
        running_sum = 0
        for i in xrange(len(self.alphabet)):
            char = self.alphabet[i]
            observed = counts[char]
            if i < len(self.alphabet)-1:
                p_i = (float(observed) + lmda) / denom
                p_i = 1.0 - (1.0 - p_i)
                running_sum += p_i
            else:
                p_i = 1 - running_sum
            probabilities[char] = p_i
        return probabilities
