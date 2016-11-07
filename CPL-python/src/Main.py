import sys
sys.path.insert(0, '../src/classes')
from PatternsPool import PatternsPool
from Ontology import Ontology
from ProcessedText import ProcessedText
from InstanceExtractor import InstanceExtractor
from PatternExtractor import PatternExtractor
import logging
import os
from tqdm import tqdm
import pickle
import pymorphy2
morph = pymorphy2.MorphAnalyzer()


# FIXME enter full path for current files on your computer
ontologyPath = '../resources/xlsx/categories_animals_ru.xls'
ontologyJSON = '../resources/json/ontology.json'
patternsPoolPath = '../resources/xlsx/patterns.xlsx'
patternsPoolJSON = '../resources/json/patternsPool.json'
logPath = 'log/cpl.log'
textsPath = '../resources/texts'
processedTextsPath = '../resources/processed'

# FIXME end of path section
ITERATIONS = 100


def inizialize():
    logging.basicConfig(filename=logPath, filemode='w', level=logging.DEBUG, format='%(asctime)s %(message)s')
    patternsPool = PatternsPool(patternsPoolPath)
    logging.info("Patterns pool inizializated")
    ontology = Ontology(ontologyPath)
    logging.info("Ontology inizializated")
    return patternsPool, ontology


def main():
    patternsPool, ontology = inizialize()
    print ("Reading step begin\n")
    files = [f for f in os.listdir(textsPath) if os.path.isfile(os.path.join(textsPath, f))]
    for file in tqdm(files):
        originalTextFile = textsPath + '/' + file
        processedTextFile = processedTextsPath + '/' + file + '.json'
        if not os.path.exists(processedTextFile):
            processedText = ProcessedText(originalTextFile, morph)
            processedText.toJSON(processedTextFile)
            logging.info("Found new file %s. Proccessed successfully from %s to %s" % (file, textsPath, processedTextsPath))
        break

    instanceExtractor = InstanceExtractor()
    patternExtractor = PatternExtractor()
    for iteration in range(1, ITERATIONS):
        logging.info('Iteration %s begin' % (str(iteration)))
        print('\nIteration %s begin' % (str(iteration)))


        print("\nInstance Extractor learning step begin")
        ontology = instanceExtractor.learn(patternsPool, ontology, processedTextsPath)
        print("\nInstance Extractor evaluationg step begin")
        ontology = instanceExtractor.evaluate(ontology, processedTextsPath)
        print("\nPattern Extractor learning step begin")
        promotedPatternsDict, promotedPatternsPool = patternExtractor.learn(patternsPool, ontology, processedTextsPath)
        print("\nPattern Extractor evaluationg step begin")
        patternsPool, ontology = patternExtractor.evaluate(ontology, patternsPool, promotedPatternsPool, promotedPatternsDict, processedTextsPath)

        print("Saving ontology/patternsPool")
        ontology.toJSON(ontologyJSON)
        patternsPool.toJSON(patternsPoolJSON)

        print("Clear promoted pattern pool and dictionary")
        promotedPatternsPool.clear()
        promotedPatternsDict = dict()


if __name__ == "__main__":
    main()