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
    print ('\ntry to find unprocessed text')
    for file in tqdm(files):
        if db['processed_files'].find({'name':file}).count() != 0:
            logging.info('File [%s] is already in database, skipping' % file)
            continue
        file_path = texts_path + '/' + file
        helper.process_sentences_from_file(file_path, db)
        db['processed_files'].insert_one({'name':file})
        logging.info('File [%s] was sucessfully added to database' % file)

def main():
    connect_to_database()
    inizialize()
    # preprocess_files()
    # helper.build_category_index(db)
    treshold = 50
    for iteration in range(1, 11):
        print ('Iteration [%s] begins' % str(iteration))
        logging.info('=============ITERATION [%s] BEGINS=============' % str(iteration))
        helper.extract_instances(db, iteration)
        helper.evaluate_instances(db, treshold, iteration)
        helper.extract_patterns(db, iteration)
        helper.evaluate_patterns(db, treshold, iteration)
        helper.zero_coocurence_count(db)


if __name__ == "__main__":
    main()