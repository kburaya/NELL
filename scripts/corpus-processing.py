import argparse
from pymystem3 import Mystem
import re
import logging, os, sys
import codecs
import json

def find_lexema(word, strLex):
    try:
        grStr = word[0]['analysis'][0]['gr']
        if(strLex in grStr):
            return 1
        else:
            return 0
    except Exception:
        return 0

def get_prev_word(text_corpus, position):
    word = ''
    if(text_corpus[position] == ' '):
       position -= 1
    for letter in reversed(range(position + 1)):
        if(text_corpus[letter] == ' '):
            break
        word = word + text_corpus[letter]
    word = word[::-1]
    return word

def get_next_word(text_corpus, position):
    word = ''
    if(text_corpus[position] == ' '):
        position += 1
    for letter in range(position, len(text_corpus)):
        if(text_corpus[letter] == ' '):
            break
        word = word + text_corpus[letter]
    return word

def find_part_of_speech_before(text_corpus, position, part_of_speech):
    mystem = Mystem()
    word = ''

    counter = 0
    while counter <= 100:
        counter += 1

        word = get_prev_word(text_corpus, position)
        position = position - len(word) - 1
        word_stem = mystem.analyze(word)
        if find_lexema(word_stem, part_of_speech) != 0:
            return word

    return word

def find_first_part_of_speech_next(text_corpus, position, part_of_speech):
    mystem = Mystem()
    word = ''
    counter = 0
    while counter <= 100:
        counter += 1

        word = get_next_word(text_corpus, position)
        position += len(word) + 1
        word_stem = mystem.analyze(word)
        if find_lexema(word_stem, part_of_speech) != 0:
            return word



def find_patterns(text_corpus):
    #Don't know how to read it from file
    patterns_lib = []
    patterns_lib.append(re.compile(u'\s((относ[ия]тся)\s(к))', re.UNICODE))
    patterns_lib.append(re.compile(u'\s(явля[ею]тся)', re.UNICODE))
    patterns_lib.append(re.compile(u'\s(счита[ею]тся)', re.UNICODE))
    patterns_lib.append(re.compile(u'\s(-)\s(это)', re.UNICODE))
    patterns_lib.append(re.compile(u'\s(-)\s', re.UNICODE))

    mystem = Mystem()
    categories = dict()
    categories_file = open('results/categories.txt', 'w')
    categories_dict = open('results/categories-dict.json', 'w')

    for pattern in patterns_lib:
        for result in re.finditer(pattern, text_corpus):
            #find noun - relation - noun
            word_1 = find_part_of_speech_before(text_corpus, result.start(), 'S')
            word_2 = find_first_part_of_speech_next(text_corpus, result.end(), 'S')

            word_1_stem = mystem.analyze(word_1)
            word_2_stem = mystem.analyze(word_2)

            try:
                word_1 = word_1_stem[0]['text']
            except Exception:
                word_1 = word_1
            try:
                word_2 = word_2_stem[0]['text']
            except Exception:
                word_2 = word_2

            logging.debug('Found SUBCATEGORY: %s, CATEGORY: %s, RELATION: %s', word_1, word_2, result.group())
            logging.debug('Found CONTEXT: [%s]', text_corpus[result.start()-50:result.start()+50])
            categories_file.write('Subcategory: ' + word_1 + ' Category: ' + word_2 + '\n')
            categories_file.write('Relation: ' + result.group() + '\n\n')

            try:
                categories[word_2].append(word_1)
            except Exception:
                categories[word_2] = [word_1]

    categories_file.close()
    categories_dict.write(json.dumps(categories, ensure_ascii=False))
    return


def main():
    parser = argparse.ArgumentParser(description='Text corpus file')
    parser.add_argument("-file", type = str, help='Path to json with pagenames')

    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)s.%(msecs)d %(levelname)s in \'%(module)s\' at line %(lineno)d: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.DEBUG,
                    filename='results/parser.log')

    text_corpus = codecs.open(args.file).read()
    find_patterns(text_corpus)
    return

if __name__ == "__main__":
    main()