'''
Init function for Patterns
'''


class PatternTemplateWord:
    def __init__(self, case, number, pos):
        self.case = case.lower()
        self.number = number.lower()
        self.pos = pos.lower()
