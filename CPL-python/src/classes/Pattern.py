"""
Pattern
"""
class Pattern:
    id = 0 #: @type: Integer
    pattern = '' #: @type: PatternTemplateWord
    arg1, arg2 = '', '' #: @type: PatterTemplateWord

    def __init__(self, id, patternString, arg1, arg2):
        """
        Constructor.
        @type id: Integer
        @type patternString: String
        @type arg1: PatternTemplateWord
        @type arg2: PatternTemplateWord
        """
        self.pattern = patternString
        self.arg1 = arg1
        self.arg2 = arg2
        self.id = id