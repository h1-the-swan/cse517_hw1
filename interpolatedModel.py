import math
from myLanguageModel import MyLanguageModel
from unigramModel import UnigramModel
from load_freqdist_pickle import load_cfd
try:
    import cPickle as pickle
except ImportError:
    import pickle

class InterpolatedModel(object):

    """Docstring for InterpolatedModel. """

    def __init__(self, models=None, highest_order=3, alphabet=None, model_weights=None):
        """TODO: to be defined1. """
        self.highest_order = highest_order
        self.alphabet = alphabet
        self.models = models
        self.model_weights = model_weights

        if not self.alphabet:
            raise RuntimeError("need an alphabet")

        if not models:
            self.models = self._load_multiple_models()

    def _load_multiple_models(self):
        with open('freq_dist_1gram.pickle', 'rb') as f:
            unigram_fd = pickle.load(f)
        unigram = self._load_unigram_model()
        models = [unigram]
        for i in range(2, self.highest_order+1):
            model = self._load_model(i)
            models.append(model)
        return models

    def _load_unigram_model(self):
        alphabet = self.alphabet
        unigram = UnigramModel(alphabet=self.alphabet)
        with open('freq_dist_1gram.pickle', 'rb') as f:
            fd = pickle.load(f)
        unigram.load_fd(fd)
        return unigram

    def _load_model(self, ngram_n=None):
        alphabet = self.alphabet
        model = MyLanguageModel(alphabet=alphabet)
        # with open('freq_dist_4gram.pickle', 'rb') as f:
        #     cfd = pickle.load(f)
        cfd = load_cfd('freq_dist_%dgram.pickle' %(ngram_n))
        model.load_cfd(cfd)
        return model

    def calculate_probability(self, history=None, model_weights=None, character=None):
        # returns logprob of character if character is specified
        # else returns a dictionary of the probability distribution for all characters
        #
        # model_weights is a list of len(models) numbers that sum to one
        # one weight for [1-gram, 2-gram, ..., highest_order_gram]
        # defaults to equal weights for all:

        # special case for empty history
        if not history:
            return self._calculate_prob_empty_history(character=character)

        models = self.models
        if not model_weights:
            model_weights = self.model_weights
            if not model_weights:
                num_models = len(models)
                model_weights = [1.0 / num_models for i in range(num_models)]

        # if the history is too short to use all the models
        if len(history) < len(models)-1:
            cutoff = len(history)+1
            models = models[:cutoff]
            # transfer the weights of the unused models to the highest order model
            unused_model_weights = sum(model_weights[cutoff:])
            model_weights = model_weights[:cutoff]
            model_weights[-1] += unused_model_weights

        if character:
            # unigram first
            p = models[0].probabilities[character] * model_weights[0]
            # now all the others
            for i in range(1, len(models)):
                model = models[i]
                probs = model.calculate_probabilities(history)
                if not probs:
                    # TODO
                    return 0
                p += probs[character] * model_weights[i]
            logprob = math.log(p, 2)
            return logprob
        else:
            all_probabilities = [models[0].probabilities]
            for i in range(1, len(models)):
                model = models[i]
                probs = model.calculate_probabilities(history)
                if not probs:
                    # TODO
                    return {}
                all_probabilities.append(probs)
            probabilities = {}
            for char in self.alphabet:
                p_char = 0
                for i in range(len(all_probabilities)):
                    p_dist = all_probabilities[i]
                    p_char += p_dist[char] * model_weights[i]
                probabilities[char] = p_char
            return probabilities

    def _calculate_prob_empty_history(self, character=None, lmda=0.000001):
        """TODO: Docstring for calculate_probabilities.

        :returns: TODO

        """
        with open('freq_dist_empty_history.pickle', 'rb') as f:
            counts = pickle.load(f)
        probabilities = {}
        denom = counts.N() + ( lmda * len(self.alphabet) )
        running_sum = 0
        for i in xrange(len(self.alphabet)):
            char = self.alphabet[i]
            observed = counts[char]
            probabilities[char] = (float(observed) + lmda) / denom
            # if i < len(self.alphabet)-1:
            #     p_i = (float(observed) + lmda) / denom
            #     p_i = 1.0 - (1.0 - p_i)
            #     running_sum += p_i
            # else:
            #     p_i = 1 - running_sum
            # probabilities[char] = p_i
        if character:
            logprob = math.log(probabilities[character], 2)
            return logprob
        else:
            return probabilities
        
