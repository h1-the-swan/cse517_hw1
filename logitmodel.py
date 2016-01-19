from sklearn import linear_model
from sklearn.feature_extraction import DictVectorizer
from sklearn.externals import joblib
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
    feature_dict_list = []
    y = []
    numchars = 4
    for sent in sent_list:
        for i in range(len(sent)):
            if i >= numchars - 1:
                char = sent[i]
                prevchars = sent[i-(numchars-1):i]
                fd = get_feature_dict(prevchars)
                if fd:
                    y.append(char)
                    feature_dict_list.append(fd)
    return (feature_dict_list, y)

def get_y_again(sent_list):
    y = []
    numchars = 4
    for sent in sent_list:
        for i in range(len(sent)):
            if i >= numchars - 1:
                char = sent[i]
                prevchars = sent[i-(numchars-1):i]
                fd = get_feature_dict(prevchars)
                if fd:
                    y.append(char)
    return y

start = time.time()
with codecs.open('data/tatoeba/tatoeba_training.txt', 'r', 'utf-8') as f:
    text = f.read()

stop_char = u'\u0003'
text = text.split(stop_char)
print('%d sentences before cleanup' %(len(text)))
sys.stdout.flush()
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
# sys.stdout.flush()
# train_data = get_training_data(sentences)
# train_data_X_fd = train_data[0]
# train_data_y = train_data[1]
train_data_y = get_y_again(sentences)

# deal with out of vocab problem:
for char in alphabet:
    train_data_y.append(char)
#     train_data_X_fd.append({})
#
# vec = DictVectorizer()
# train_data_X = vec.fit_transform(train_data_X_fd)
# pickle.dump(vec, open('logit_vectorizer.pickle', 'wb'))
# print('done.')
#
# # http://stackoverflow.com/questions/11195395/scikit-learn-logistic-regression-memory-error
# joblib.dump(train_data_X.tocsr(), 'train_data_X.joblib')
#

print('loading data...')
sys.stdout.flush()
train_data_X = joblib.load('train_data_X.joblib', mmap_mode='c')
print('training model...')
sys.stdout.flush()
model = linear_model.LogisticRegression(multi_class='multinomial', solver='lbfgs')
model.fit_transform(train_data_X, train_data_y)
print('done.')
print('pickling...')
sys.stdout.flush()
with open('logitmodel.pickle', 'wb') as f:
    pickle.dump(model, f)
print('done')
sys.stdout.flush()

end = time.time()
print('%.2f seconds' %(end-start))
sys.stdout.flush()

