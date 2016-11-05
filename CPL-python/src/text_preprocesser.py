import nltk
import os
import pickle

text_dictionary = dict()
path = '../resources/texts'
files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

def process_text(files):
    for file in files:
        f = open(path + '/' + file).read()
        sentences = nltk.sent_tokenize(f)
        for sentence in sentences:
            words = nltk.word_tokenize(sentence)
            for i in range(1, 6):
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

process_text(files)

