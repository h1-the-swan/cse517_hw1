from nltk import MaxentClassifier
import cPickle as pickle
import codecs, time, sys
from datetime import datetime
from get_bmp_alphabet import get_bmp_alphabet

print(datetime.now())
sys.stdout.flush()

alphabet = get_bmp_alphabet()

def get_feature_dict(chars):
    fd = {}
    numchars = len(chars)
    for i in range(numchars):
        k = 'char-' + str(numchars-i)
        fd[k] = chars[i]
    return fd

def get_training_data(sent_list):
    train = []
    numchars = 4
    for sent in sent_list:
        for i in range(len(sent)):
            if i >= numchars - 1:
                char = sent[i]
                prevchars = sent[i-(numchars-1):i]
                fd = get_feature_dict(prevchars)
                tup = (fd, char)
                train.append(tup)
    return train

start = time.time()
with codecs.open('data/tatoeba/tatoeba_training.txt', 'r', 'utf-8') as f:
    text = f.read()

stop_char = u'\u0003'
text = text.split(stop_char)
print('%d sentences before cleanup' %(len(text)))
sentences = []
for sent in text:
    if sent:
        check = True
        for char in sent:
            if char not in alphabet:
                check = False
        if check:
            sent = sent + stop_char
            sentences.append(sent)
                
print('%d sentences after cleanup' %(len(sentences)))
print("")

print('getting data...')
sys.stdout.flush()
train_data = get_training_data(sentences)
print('done.')
print('training model...')
sys.stdout.flush()
model = MaxentClassifier.train(train_data, labels=alphabet)
print('done.')
print('pickling...')
sys.stdout.flush()
with open('maxentmodel.pickle', 'wb') as f:
    pickle.dump(model, f)
print('done')
sys.stdout.flush()

end = time.time()
print('%.2f seconds' %(end-start))
sys.stdout.flush()
