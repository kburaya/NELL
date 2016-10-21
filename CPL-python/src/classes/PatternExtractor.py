from ProcessedText import ProcessedText
from tqdm import tqdm
from PatternTemplateWord import PatternTemplateWord
from PatternPool import PatternPool
from Pattern import Pattern
import os
import logging

class PatternExtractor:
    def __init__(self):
        return


    def learn(self, ontology, processedTextsPath):
        promotedPatternsDict = dict()
        promotedPatternsPool = PatternPool(None)
        files = [f for f in os.listdir(processedTextsPath) if os.path.isfile(os.path.join(processedTextsPath, f))]
        for file in tqdm(files):
            # file = open(processedTextsPath + '/' + file, 'rb')
            text = ProcessedText.fromJSON(processedTextsPath + '/' + file)
            for sentence in text.sentences:
                for instance in ontology.instances:
                    pos1, pos2 = self.findPatternInSentence(sentence, instance)
                    if abs(pos1 - pos2) >= 5:
                        continue
                    if pos1 < pos2:
                        patternString = 'arg1 '
                        for i in range(pos1 + 1, pos2):
                            patternString += sentence.words[i].original
                            patternString += ' '
                        patternString += 'arg2'
                    else:
                        patternString = 'arg2'
                        for i in range(pos2 + 1, pos1):
                            patternString += sentence.words[i].original
                            patternString += ' '
                        patternString += 'arg1'

                    patternWord1 = PatternTemplateWord(sentence.words[pos1].case, sentence.words[pos1].number, sentence.words[pos1].pos)
                    patternWord2 = PatternTemplateWord(sentence.words[pos2].case, sentence.words[pos2].number, sentence.words[pos2].pos)
                    if patternString not in promotedPatternsDict.keys():
                        promotedPatternsDict[patternString] = dict()
                    try:
                        promotedPatternsDict[patternString][instance.categoryName] += 1
                    except:
                        promotedPatternsDict[patternString][instance.categoryName] = 1

                    pattern = Pattern(PatternPool.maxID + 1, patternString, patternWord1, patternWord2)
                    PatternPool.maxID += 1
                    promotedPatternsPool.addPattern(pattern)
                    logging.info("Found new promoted pattern '%s' in sentence '%s'." % (patternString, sentence.string))

        return promotedPatternsDict, promotedPatternsPool



    def evaluate(self, ontology, promotedPatternsPool, promotedPatternDict):
        return

    def findPatternInSentence(self, sentence, instance):
        arg1 = instance.categoryName
        for arg2 in instance.instances():
            arg2 = arg2.lexem
            pos1, pos2 = sentence.findWordsInSentence(arg1, arg2)

        return pos1, pos2
