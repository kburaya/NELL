import string

class SimpleWord:
    isPunctuation = False
    def __init__(self, word, morph):
        if word == None:
            return

        self.original = word # FIXME maybe use word.lower() ??
        if word in string.punctuation:
            self.isPunctuation = True
            self.lexem = word
            return

        p = morph.parse(word)
        self.pos = p[0].tag.POS
        self.case = p[0].tag.case
        self.lexem = p[0].normal_form
        self.number = p[0].tag.number


    def fromJSON(self, wordJSON):
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