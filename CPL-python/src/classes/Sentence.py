"""
One sentence of ProcessedText
Contains a list of words in sentence and a string representing the sentence.
"""
import nltk
from SimpleWord import SimpleWord


class Sentence:

    words = list() #: @type: List<SimpleWord>
    string = '' #: @type: String

    def __init__(self, sentence, morph):
        """
        Constructor.
        @type sentence: String
        @type morph: MorphAnalyzer
        """
        if sentence == None:
            return

        self.string = sentence
        words = nltk.word_tokenize(sentence)
        self.words = list()
        for word in words:
            _word = SimpleWord(word, morph)
            self.words.append(_word)
        return

    def fromJSON(self, sentenceJSON):
        """
        Get Sentence from json.

        @type  sentenceJSON: jsonObject
        @param sentenceJSON: sentence json

        @rtype: Sentence
        @return: self
        """
        self.words = list()
        self.string = ''
        for i in range(0, len(sentenceJSON) - 1):
            _word = SimpleWord(None, None)
            _word = _word.fromJSON(sentenceJSON[str(i)])
            self.words.append(_word)

        self.string = sentenceJSON['string']
        return self

    def findWordsInSentence(self, word1, word2):
        """
        Find words positions in Sentence.

        @type  word1: SimpleWord
        @param word1: first word to find

        @type  word2: SimpleWord
        @param word2: second word to find

        @rtype: tuple(Integer|None, Integer|None)
        @return: positions of first letters of given words in sentence (if exist)
        """
        pos1, pos2 = None, None

        for i in range(0, len(self.words)):
            if word1 == self.words[i].lexem:
                pos1 = i
            if word2 == self.words[i].lexem:
                pos2 = i

        return (pos1, pos2)
