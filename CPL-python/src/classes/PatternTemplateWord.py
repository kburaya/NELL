'''
Init function for Patterns
'''


class PatternTemplateWord:
    # One word of Pattern (arg1 and arg2)

    def __init__(self, case, number, pos):
        """
        Constructor.
        @type case: String
        @type number: String
        @type pos: String
        """
        self.case = case.lower() #: @type: String
        self.number = number.lower() #: @type: String
        self.pos = pos.lower() #: @type: String
