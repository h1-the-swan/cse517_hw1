from interpolatedModel import InterpolatedModel
from get_bmp_alphabet import get_bmp_alphabet
alphabet = get_bmp_alphabet()
models = InterpolatedModel(highest_order=3, alphabet=alphabet)
# models = models.models
print(models.calculate_probability(history=u'hell', character=u'o'))
