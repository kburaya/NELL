import nltk
from SimpleWord import SimpleWord


class Sentence:
    words = list()
    string = ''
    def __init__(self, sentence, morph):
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
        self.words = list()
        self.string = ''
        for i in range(0, len(sentenceJSON) - 1):
            _word = SimpleWord(None, None)
            _word = _word.fromJSON(sentenceJSON[str(i)])
            self.words.append(_word)


        self.string = sentenceJSON['string']
        return self


    def findWordsInSentence(self, word1, word2):
        pos1, pos2 = None, None

        for i in range(0, len(self.words)):
            if word1 == self.words[i].lexem:
                pos1 = i
            if word2 == self.words[i].lexem:
                pos2 = i

        return (pos1, pos2)

