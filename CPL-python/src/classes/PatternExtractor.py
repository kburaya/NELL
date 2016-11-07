from ProcessedText import ProcessedText
from tqdm import tqdm
from PatternTemplateWord import PatternTemplateWord
from PatternsPool import PatternsPool
from Pattern import Pattern
import os
import logging
import nltk
from sortedcontainers import SortedDict
import pickle
import traceback


class PatternExtractor:
    def __init__(self):
        return


    def learn(self, patternsPool, ontology, processedTextsPath):
        print ('\n Pattern Extractor. Learning step. ')
        logging.info('\n Pattern Extractor. Learning step. ')
        promotedPatternsDict = dict()
        promotedPatternsPool = PatternsPool(None)
        files = [f for f in os.listdir(processedTextsPath) if os.path.isfile(os.path.join(processedTextsPath, f))]
        for file in tqdm(files):
            logging.info("Processing file %s" % file)
            # file = open(processedTextsPath + '/' + file, 'rb')
            text = ProcessedText.fromJSON(processedTextsPath + '/' + file)
            for sentence in text.sentences:
                for instance in ontology.instances:
                    pos1, pos2 = self.findPatternInSentence(sentence, instance)
                    if pos1 == None or pos2 == None:
                        continue

                    if abs(pos1 - pos2) >= 5:
                        continue

                    if pos1 < pos2:
                        patternString = 'arg1 '
                        for i in range(pos1 + 1, pos2):
                            patternString += sentence.words[i].original
                            patternString += ' '
                        patternString += 'arg2'
                    else:
                        patternString = 'arg2 '
                        for i in range(pos2 + 1, pos1):
                            patternString += sentence.words[i].original
                            patternString += ' '
                        patternString += 'arg1'

                    if instance.check_if_pattern_exists(patternString, patternsPool):
                        logging.info("Pattern [%s] for category [%s] already exists, skip" % (patternString, instance.categoryName))
                        continue

                    patternWord1 = PatternTemplateWord(sentence.words[pos1].case, sentence.words[pos1].number, sentence.words[pos1].pos)
                    patternWord2 = PatternTemplateWord(sentence.words[pos2].case, sentence.words[pos2].number, sentence.words[pos2].pos)
                    if patternString not in promotedPatternsDict.keys():
                        promotedPatternsDict[patternString] = dict()
                    try:
                        promotedPatternsDict[patternString][instance.categoryName] += 1
                    except:
                        promotedPatternsDict[patternString][instance.categoryName] = 1

                    pattern = Pattern(PatternsPool.maxID + 1, patternString, patternWord1, patternWord2)
                    PatternsPool.maxID += 1
                    promotedPatternsPool.addPattern(pattern)
                    logging.info("Found new promoted pattern [%s] in sentence [%s]." % (patternString, sentence.string))

        return promotedPatternsDict, promotedPatternsPool



    def evaluate(self, ontology, patternsPool, promotedPatternsPool, promotedPatternsDict, processedTextsPath, treshold = 3):
        # TODO think how to rewrite this part
        print('Pattern Extractor. Evaluating step.')
        logging.info('Pattern Extractor. Evaluating step.')
        ngrams_dictionary = load_dictionary('ngrams_dictionary.pkl')
        for instance in ontology.instances:
            _treshold = treshold
            precision = dict()
            for pattern in promotedPatternsPool.patterns:
                try:
                    numOfCoOccurence = promotedPatternsDict[pattern.pattern][instance.categoryName]
                except:
                    continue

                s_pattern = ''
                pattern_tokenize = nltk.word_tokenize(pattern.pattern)
                try:
                    pattern_tokenize.remove('arg2')
                    pattern_tokenize.remove('arg1')
                except:
                    logging.error("Can't remove arg1/2 arguments from pattern string, passing")
                    continue
                for word in pattern_tokenize:
                    s_pattern += word
                    s_pattern += ' '
                s_pattern = s_pattern[:-1].lower()
                try:
                    numOfCoOccurence = promotedPatternsDict[pattern.pattern][instance.categoryName]
                    numInText = ngrams_dictionary[s_pattern]
                    precision[pattern.pattern] = numOfCoOccurence / numInText
                except:
                    continue

            if precision.__len__() == 0:
                continue

            precision = SortedDict(precision)


            for pattern_string in precision:
                if _treshold == 0:
                    break
                try:
                    pattern = promotedPatternsPool.get_pattern_by_string(pattern_string)
                    precision_score = precision[pattern.pattern]
                except:
                    continue
                if instance.addPromotedPattern(pattern, promotedPatternsPool, patternsPool):
                    patternsPool.addPattern(pattern)
                    logging.info("Add pattern [%s] for category [%s] with precision score [%s]" % (pattern.pattern, instance.categoryName, str(precision_score)))
                    _treshold -= 1

        return patternsPool, ontology


    def findPatternInSentence(self, sentence, instance):
        pos1, pos2 = None, None
        arg1 = instance.categoryName
        for arg2 in instance.instances:
            pos1, pos2 = sentence.findWordsInSentence(arg1, arg2)
            if pos1 != None and pos2 != None:
                return pos1, pos2

        return pos1, pos2


def load_dictionary(file):
    with open(file, 'rb') as f:
        obj = pickle.load(f)
    return obj



