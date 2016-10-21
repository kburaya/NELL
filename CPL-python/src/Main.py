import sys
sys.path.insert(0, '/Users/kseniya/Documents/Study/NELL/CPL-python/src/classes')
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
ontologyPath = '/Users/kseniya/Documents/Study/NELL/CPL-python/resources/xlsx/categories_animals_ru.xls'
patternsPoolPath = '/Users/kseniya/Documents/Study/NELL/CPL-python/resources/xlsx/patterns.xlsx'
logPath = '/Users/kseniya/Documents/Study/NELL/CPL-python/src/log/cpl.log'
textsPath = '/Users/kseniya/Documents/Study/NELL/CPL-python/resources/texts'
processedTextsPath = '/Users/kseniya/Documents/Study/NELL/CPL-python/resources/processed'
# FIXME end of path section


def inizialize():
    logging.basicConfig(filename=logPath, filemode='w', level=logging.DEBUG, format='%(asctime)s %(message)s')
    patternsPool = PatternsPool(patternsPoolPath)
    logging.info("Patterns pool inizializated")
    ontology = Ontology(ontologyPath)
    logging.info("Ontology inizializated")
    return patternsPool, ontology


def main():
    patternsPool, ontology = inizialize()
    # print (Reading step begin\n")
    # files = [f for f in os.listdir(textsPath) if os.path.isfile(os.path.join(textsPath, f))]
    # for file in tqdm(files):
    #     originalTextFile = textsPath + '/' + file
    #     processedTextFile = processedTextsPath + '/' + file + '.json'
    #     if not os.path.exists(processedTextFile):
    #         processedText = ProcessedText(originalTextFile, morph)
    #         processedText.toJSON(processedTextFile)
    #         logging.info("Found new file %s. Proccessed successfully from %s to %s" % (file, textsPath, processedTextsPath))

    instanceExtractor = InstanceExtractor()
    patternExtractor = PatternExtractor()
    print ("Learning step begin\n")
    ontology = instanceExtractor.learn(patternsPool, ontology, processedTextsPath)
    print ("Evaluationg step begin\n")
    ontology = instanceExtractor.evaluate(ontology, processedTextsPath)
    promotedPatternsPool, promotedPatternDict = patternExtractor.learn(ontology, processedTextsPath)
    ontology = patternExtractor.evaluate(ontology, promotedPatternsPool, promotedPatternDict)


if __name__ == "__main__":
    main()