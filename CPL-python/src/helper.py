import pandas as pd
from pymystem3 import Mystem
import nltk
import string
import pymorphy2
mystem = Mystem()
punctuation = string.punctuation
morph = pymorphy2.MorphAnalyzer()

def get_patterns_from_file(file, db):
    file = pd.read_excel(file)
    for index, row in file.iterrows():
        if db['patterns'].find({'_id':int(row['id'])}).count() != 0:
            continue
        pattern = dict()
        pattern['_id'] = int(row['id'])
        pattern['string'] = row['pattern']

        arg1, arg2 = dict(), dict()
        arg1['case'] = row['arg1_case'].lower()
        arg1['num'] = row['arg1_num'].lower()
        arg1['pos'] = row['arg1_pos'].lower()
        arg2['case'] = row['arg2_case'].lower()
        arg2['num'] = row['arg2_num'].lower()
        arg2['pos'] = row['arg2_pos'].lower()

        pattern['arg1'] = arg1
        pattern['arg2'] = arg2

        pattern['presicion'] = 0
        pattern['true_detective'] = 0
        pattern['false_detective'] = 0
        pattern['categories'] = list()
        pattern['used'] = False

        #FIXME think about this features more deeply later
        pattern['iteration_added'] = list()
        pattern['iteration_deleted'] = list()

        db['patterns'].insert_one(pattern)


def get_ontology_from_file(file, db):
    file = pd.read_excel(file)
    for index, row in file.iterrows():
        ontology_category = dict()
        category_name = mystem.lemmatize(row['categoryName'])[0]

        if db['ontology'].find({'category_name': category_name}).count() != 0:
            continue
        ontology_category['category_name'] = category_name
        ontology_category['_id'] = db['ontology'].find().count() + 1
        if type(row['seedInstances']) is float:
            ontology_category['instances'] = list()
        else:
            ontology_category['instances'] = row['seedInstances'].split('"')[1::2]

        if type(row['seedExtractionPatterns']) is float:
            ontology_category['extraction_patterns'] = list()
        else:
            ontology_category['extraction_patterns'] = [int(s) for s in row['seedExtractionPatterns'].split(' ') if s.isdigit()]

        ontology_category['promoted_patterns'] = list()

        db['ontology'].insert_one(ontology_category)


def process_sentences_from_file(file, db):
    text = open(file, 'r').read()
    sentences = nltk.sent_tokenize(text)
    for s in sentences:
        sentence = dict()
        sentence['_id'] = db['sentences'].find().count() + 1
        sentence['string'] = s
        sentence['words'] = list()

        words = nltk.word_tokenize(s)
        for word in words:
            word_dict = dict()
            word_dict['original'] = word
            if word in punctuation:
                word_dict['punctuation'] = True
                word_dict['lexem'] = word
                sentence['words'].append(word_dict)
                continue

            p = morph.parse(word)
            word_dict['pos'] = p[0].tag.POS
            word_dict['case'] = p[0].tag.case
            word_dict['lexem'] = p[0].normal_form
            word_dict['number'] = p[0].tag.number
            word_dict['punctuation'] = False
            sentence['words'].append(word_dict)

        db['sentences'].insert_one(sentence)
    return