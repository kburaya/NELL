"""
One word of a Sentence.
Contains part of speech(noun, adjf, ...), case(nomn, gent, datv ...), lexem(normal form) and number(sing, plur) for specified word.
"""
import string


class SimpleWord:


    isPunctuation = False #: @type: Boolean

    def __init__(self, word, morph):
        """
        Constructor.
        @type word: String
        @type morph: MorphAnalyzer
        """
        if word == None:
            return

        self.original = word # FIXME maybe use word.lower() ??
        if word in string.punctuation:
            self.isPunctuation = True
            self.lexem = word
            return

        p = morph.parse(word)
        self.pos = p[0].tag.POS #: @type: String
        self.case = p[0].tag.case #: @type: String
        self.lexem = p[0].normal_form #: @type: String
        self.number = p[0].tag.number #: @type: String


    def fromJSON(self, wordJSON):
        """
        Get SimlpeWord from json.

        @type  wordJSON: jsonObject
        @param wordJSON: json of a word

        @rtype: SimpleWord
        @return: self
        """
        self.original = wordJSON['original']
        if wordJSON['isPunctuation']:
            self.isPunctuation = True
            self.lexem = self.original
            return self
        self.isPunctuation = False

        self.pos = wordJSON['pos']
        self.case = wordJSON['case']
        self.lexem = wordJSON['lexem']
        self.number = wordJSON['number']
        return self