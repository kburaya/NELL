class Pattern:
    id = 0
    pattern = ''
    arg1, arg2 = '', ''

    def __init__(self, id, patternString, arg1, arg2):
        self.pattern = patternString
        self.arg1 = arg1
        self.arg2 = arg2
        self.id = id