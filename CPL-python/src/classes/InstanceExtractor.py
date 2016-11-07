import os
import pickle
import nltk
import logging
from tqdm import tqdm
from ProcessedText import ProcessedText
from SimpleWord import SimpleWord
from PatternsPool import PatternsPool
import string
from sortedcontainers import SortedDict


class InstanceExtractor:
    def __init__(self):
        return


    def learn(self, patternsPool, ontology, processedTextsPath):
        print('\nInstance Extractor. Learning step')
        files = [f for f in os.listdir(processedTextsPath) if os.path.isfile(os.path.join(processedTextsPath, f))]
        for file in tqdm(files):
            logging.info("Processing file %s" % file)
            #file = open(processedTextsPath + '/' + file, 'rb')
            text = ProcessedText.fromJSON(processedTextsPath + '/' + file)
            for sentence in text.sentences:
                for pattern in patternsPool.patterns:
                    ontology = self.findPatternInSentence(pattern, sentence, ontology)

        return ontology


    def findPatternInSentence(self, pattern, sentence, ontology):
        patternString = nltk.word_tokenize(pattern.pattern)
        for i in range(0, len(sentence.words) - len(patternString) + 1):
            arg1Pos, arg2Pos = self.checkIfPatternExists(sentence.words[i:(len(patternString))], pattern)
            if (arg1Pos != None) and (arg2Pos != None):
                arg1Pos = i + arg1Pos
                arg2Pos = i + arg2Pos

                arg1 = sentence.words[arg1Pos]
                arg2 = sentence.words[arg2Pos]
                for category in ontology.instances:
                    if (arg1.lexem == category.categoryName):
                        if category.check_if_promoted_instance_exists(arg2.lexem):
                            logging.info("Found existing promoted instance [%s] for category [%s]" % (arg2.lexem, category.categoryName))
                            continue
                        if self.checkWordForPattern(arg1, pattern.arg1):
                            if self.checkWordForPattern(arg2, pattern.arg2):
                                logging.info("Found new promoted instance [%s] in sentence [%s] with pattern '%s'" %
                                             (arg2.lexem, sentence.string, pattern.pattern))
                                try:
                                    category.promotedInstances[arg2.lexem] += 1
                                except:
                                    category.promotedInstances[arg2.lexem] = 1

        return ontology


    def checkIfPatternExists(self, sentencePart, pattern):
        flag, arg1Pos, arg2Pos = True, None, None
        _pattern = nltk.word_tokenize(pattern.pattern)
        for i in range(0, len(sentencePart)):
            if _pattern[i] == 'arg1':
                arg1Pos = i
                continue
            elif _pattern[i] == 'arg2':
                arg2Pos = i
                continue
            elif _pattern[i] != sentencePart[i].original:
                return (None, None)

        return (arg1Pos, arg2Pos)


    def checkWordForPattern(self, word, patternWord):
        try:
            if (word.case.lower() == patternWord.case.lower()) and (word.pos.lower() == patternWord.pos.lower()):
                if ((word.number.lower()) == patternWord.number.lower()) or (patternWord.number == 'all'):
                    return True
        except:
            return False
        return False


    def evaluate(self, ontology, processedTextsPath, treshold = 3):
        print('\nInstance Extractor. Evaluating step.')
        ngrams_dictionary = load_dictionary('ngrams_dictionary.pkl')
        for instance in ontology.instances:
            _treshold = treshold
            precision = dict()
            for promotedInstance in instance.promotedInstances:
                numOfCoOccurence = instance.promotedInstances[promotedInstance]
                numInText = ngrams_dictionary[promotedInstance]
                precision[promotedInstance] = numOfCoOccurence / numInText
            precision = SortedDict(precision)

            instance.promotedInstances = dict()
            for promotedInstance in precision:
                if _treshold == 0:
                    break
                if instance.addPromotedInstance(promotedInstance):
                    logging.info("Adding new instance [%s] to Category [%s] with precision value [%s]" %
                                (promotedInstance, instance.categoryName, str(precision[promotedInstance])))
                    _treshold -= 1

        return ontology

def findNumberOfInstanceInText(instance, processedTextsPath):
    count = 0
    files = [f for f in os.listdir(processedTextsPath) if os.path.isfile(os.path.join(processedTextsPath, f))]
    for file in tqdm(files):
        # file = open(processedTextsPath + '/' + file, 'rb')
        text = ProcessedText.fromJSON(processedTextsPath + '/' + file)
        for sentence in text.sentences:
            for word in sentence.words:
                if word.isPunctuation:
                    continue
                if word.lexem == instance:
                    count += 1
    return count


def load_dictionary(file):
    with open(file, 'rb') as f:
        obj = pickle.load(f)
    return obj