import nltk
import pymorphy2
import pickle
import string
from tqdm import tqdm
from Sentence import Sentence
import json


class ProcessedText:
    """
    Makes ProcessedText structure from each file
    """
    sentences = list() #: @type: List<Sentence>

    def __init__(self, file, morph):
        """
        Constructor.
        @type file: String
        @type morph: MorphAnalyzer
        """
        if file == None:
            return
        text = open(file, 'r').read()
        sentences = nltk.sent_tokenize(text)
        self.sentences = list()
        for sentence in sentences:
            _sentence = Sentence(sentence, morph)
            self.sentences.append(_sentence)
            del _sentence
        return


    def toJSON(self, file):
        """
        Save ProcessedText to json.

        @type file: String
        @param file: full path of file to save into
        """

        _json = dict()
        for i in range(0, len(self.sentences)):
            _json[i] = dict()
            for j in range(0, len(self.sentences[i].words)):
                _json[i][j] = dict()
                _json[i][j]['original'] = self.sentences[i].words[j].original
                _json[i][j]['isPunctuation'] = self.sentences[i].words[j].isPunctuation
                if self.sentences[i].words[j].isPunctuation:
                    continue
                _json[i][j]['pos'] = self.sentences[i].words[j].pos
                _json[i][j]['case'] = self.sentences[i].words[j].case
                _json[i][j]['lexem'] = self.sentences[i].words[j].lexem
                _json[i][j]['number'] = self.sentences[i].words[j].number
            _json[i]['string'] = self.sentences[i].string

        with open(file, 'w') as data:
            json.dump(_json, data, ensure_ascii=False)
        return

    @classmethod
    def fromJSON(self, file):
        """
        Constructor.
        Get ProcessedText from json.

        @type  file: String
        @param file: full path to file

        @rtype: ProcessedText
        @return: self
        """
        with open(file, 'r') as data:
            _json = json.load(data)
        self.sentences = list()
        for sentence in _json:
            _sentence = Sentence(None, None)
            _sentence = _sentence.fromJSON(_json[sentence])
            self.sentences.append(_sentence)
        return self

