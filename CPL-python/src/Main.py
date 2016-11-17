import sys
sys.path.insert(0, '../src/')
import helper
import logging
import os
from tqdm import tqdm
import pymorphy2
from pymongo import MongoClient
morph = pymorphy2.MorphAnalyzer()


# FIXME enter full path for current files on your computer
ontology_path = '../resources/xlsx/categories_animals_ru.xls'
patterns_pool_path = '../resources/xlsx/patterns.xlsx'
log_path = 'log/cpl.log'
texts_path = '../resources/texts'
# FIXME end of path section
ITERATIONS = 100
db = None


def connect_to_database():
    client = MongoClient('localhost', 27017)
    global db
    db = client.nell


def inizialize():
    # Read initial ontology and patterns
    logging.basicConfig(filename=log_path, filemode='w', level=logging.DEBUG, format='%(asctime)s %(message)s')
    helper.get_patterns_from_file(patterns_pool_path, db)
    logging.info("patterns pool inizializated")
    helper.get_ontology_from_file(ontology_path, db)
    logging.info("ontology inizializated")


def preprocess_files():
    files = [f for f in os.listdir(texts_path) if os.path.isfile(os.path.join(texts_path, f))]
    print ('try to find unprocessed text')
    for file in tqdm(files):
        if db['processed_files'].find({'name':file}).count() != 0:
            continue
        file_path = texts_path + '/' + file
        helper.process_sentences_from_file(file_path, db)
        break

def main():
    connect_to_database()
    inizialize()
    preprocess_files()


    # instanceExtractor = InstanceExtractor()
    # patternExtractor = PatternExtractor()
    # for iteration in range(1, ITERATIONS):
    #     logging.info('Iteration %s begin' % (str(iteration)))
    #     print('\nIteration %s begin' % (str(iteration)))
    #
    #
    #     print("\nInstance Extractor learning step begin")
    #     ontology = instanceExtractor.learn(patternsPool, ontology, processedTextsPath)
    #     print("\nInstance Extractor evaluationg step begin")
    #     ontology = instanceExtractor.evaluate(ontology, processedTextsPath)
    #     print("\nPattern Extractor learning step begin")
    #     promotedPatternsDict, promotedPatternsPool = patternExtractor.learn(patternsPool, ontology, processedTextsPath)
    #     print("\nPattern Extractor evaluationg step begin")
    #     patternsPool, ontology = patternExtractor.evaluate(ontology, patternsPool, promotedPatternsPool, promotedPatternsDict, processedTextsPath)
    #
    #     print("Saving ontology/patternsPool")
    #     ontology.toJSON(ontologyJSON)
    #     patternsPool.toJSON(patternsPoolJSON)
    #
    #     print("Clear promoted pattern pool and dictionary")
    #     promotedPatternsPool.clear()
    #     promotedPatternsDict = dict()


if __name__ == "__main__":
    main()