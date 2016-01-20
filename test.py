from interpolatedModel import InterpolatedModel
from get_bmp_alphabet import get_bmp_alphabet
import math
alphabet = get_bmp_alphabet()
models = InterpolatedModel(highest_order=5, alphabet=alphabet, model_weights = [0.1, 0.1, 0.2, 0.3, 0.3])
# models = models.models
probs = models.calculate_probability(history=u'hello worl', character=None)
for char in [u'z', u'd', u'$', unichr(36179)]:
    print(char, models.calculate_probability(history=u'hello worl', character=char))
    # print(char, math.log(probs[char], 2))
# p = models.calculate_probability(history=u'', character=None)
