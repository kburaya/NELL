import argparse
from pymystem3 import Mystem
import re
import logging, os, sys
import codecs
import json

mystem = None
simple_logger = None
medium_logger = None
hard_logger = None

def find_lexema(word, strLex):
    try:
        grStr = word[0]['analysis'][0]['gr']
        if(strLex in grStr):
            return True
        else:
            return False
    except Exception:
        return False


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


def find_part_of_speech_before(text_corpus, position, parts_of_speech, strict = False):
    word = ''

    counter = 0
    while counter <= 100:
        counter += 1

        word = get_prev_word(text_corpus, position)
        position = position - len(word) - 1
        word_stem = mystem.analyze(word)
        flag = False
        for part_of_speech in parts_of_speech:
            if find_lexema(word_stem, part_of_speech) == 0:
                flag = True
        if not flag:
            if strict and (find_lexema(word_stem, '|')):
                logging.info("Found ambiguity in word %s", word)
            return word

    return word


def find_first_part_of_speech_next(text_corpus, position, parts_of_speech, strict = False):

    counter = 0
    while counter <= 100:
        counter += 1
        word = get_next_word(text_corpus, position)
        position += len(word) + 1
        word_stem = mystem.analyze(word)
        flag = False
        for part_of_speech in parts_of_speech:
            if find_lexema(word_stem, part_of_speech) == 0:
                flag = True
        if not flag:
            if strict and (find_lexema(word_stem, '|')):
                logging.info("Found ambiguity in word %s", word)
            return word
    return

def set_mystem():
    global mystem
    mystem = Mystem()


def define_words(text_corpus, result, parts_of_speech_1, parts_of_speech_2, logger, strict = False):

    word_1 = find_part_of_speech_before(text_corpus, result.start(), parts_of_speech_1)
    word_2 = find_first_part_of_speech_next(text_corpus, result.end(), parts_of_speech_2)
    word_1_stem = mystem.analyze(word_1)
    word_2_stem = mystem.analyze(word_2)
    try:
        word_1 = word_1_stem[0]['analysis'][0]['lex']
    except Exception:
        word_1 = word_1
    try:
        word_2 = word_2_stem[0]['analysis'][0]['lex']
    except Exception:
        word_2 = word_2
    logger.info('Found SUBCATEGORY: [%s], RELATION: [%s], CATEGORY: [%s]', word_1, result.group(), word_2)
    logger.info('CONTEXT: [%s] \n', text_corpus[result.start() - 80:result.start() + 80])

    return


def find_patterns(text_corpus):
    patterns_lib = []
    patterns_lib.append(re.compile(u'\s((относ[ия]тся)\s(к)\s)', re.UNICODE))
    patterns_lib.append(re.compile(u'\s(явля[ею]тся\s)', re.UNICODE))
    patterns_lib.append(re.compile(u'\s(счита[ею]тся\s)', re.UNICODE))
    patterns_lib.append(re.compile(u'\s(-)\s(это\s)', re.UNICODE))
    patterns_lib.append(re.compile(u'\s(-)\s', re.UNICODE))

    #categories = dict()
    #categories_file = open('results/categories.txt', 'w')
    #categories_dict = open('results/categories-dict.json', 'w')

    for pattern in patterns_lib:
        for result in re.finditer(pattern, text_corpus):
            #find noun - relation - noun
            define_words(text_corpus, result, ['S'], ['S'], simple_logger)
            define_words(text_corpus, result, ['S'], ['S', 'род'], medium_logger)
            define_words(text_corpus, result, ['S', 'им'], ['S', 'род'], hard_logger, strict = True)

            # try:
            #     categories[word_2].append(word_1)
            # except Exception:
            #     categories[word_2] = [word_1]

    #categories_file.close()
    #categories_dict.write(json.dumps(categories, ensure_ascii=False))
    return


def chunked(file, chunk_size):
    return iter(lambda: file.read(chunk_size), '')


def setup_logger(logger_name, log_file, level=logging.INFO):
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s : %(message)s')
    fileHandler = logging.FileHandler(log_file, mode='w')
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)

    l.setLevel(level)
    l.addHandler(fileHandler)
    l.addHandler(streamHandler)


def main():
    parser = argparse.ArgumentParser(description =' Text corpus file')
    parser.add_argument("-file", type = str, help = 'Path to json with pagenames')

    args = parser.parse_args()

    # logging.basicConfig(format='%(asctime)s.%(msecs)d %(levelname)s in \'%(module)s\' at line %(lineno)d: %(message)s',
    #                 datefmt='%Y-%m-%d %H:%M:%S',
    #                 level=logging.INFO,
    #                 filename='results/parser.log',
    #                 filemode='a')

    global simple_logger
    setup_logger('simple', 'results/nom-nom.log')
    simple_logger = logging.getLogger('simple')

    global medium_logger
    setup_logger('medium', 'results/any-gen.log')
    medium_logger = logging.getLogger('medium')

    global hard_logger
    setup_logger('hard', 'results/nom-gen-strict.log')
    hard_logger = logging.getLogger('hard')

    corpus = open(args.file, errors='ignore')
    text_corpus = corpus.read()
    set_mystem()

    find_patterns(text_corpus)
    return

if __name__ == "__main__":
    main()