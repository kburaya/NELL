import nltk
import os
import pickle
from tqdm import tqdm

text_dictionary = dict()
path = '../resources/texts'
files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

def process_text(files, max_n):
    for file in tqdm(files):
        f = open(path + '/' + file).read()
        sentences = nltk.sent_tokenize(f)
        for sentence in sentences:
            words = nltk.word_tokenize(sentence)
            for i in range(1, max_n + 1):
                ngrams = nltk.ngrams(words, i)
                for ngram in ngrams:
                    s = ''
                    for word in ngram:
                        s += word
                        s += ' '
                    s = s[:-1].lower()
                    try:
                        text_dictionary[s] += 1
                    except:
                        text_dictionary[s] = 1
    with open('ngrams_dictionary.pkl', 'wb') as f:
        pickle.dump(text_dictionary, f)


def load_dictionary(file):
    with open(file, 'rb') as f:
        obj = pickle.load(f)
    return obj

process_text(files, 3)
# load_dictionary('ngrams_dictionary.pkl')
