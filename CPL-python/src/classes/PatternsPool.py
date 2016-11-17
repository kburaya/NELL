"""
Pool of Patterns
"""
import sys
import pandas as pd
sys.path.insert(0, '../src/classes')
from PatternTemplateWord import PatternTemplateWord
from Pattern import Pattern
import json


class PatternsPool:

    maxID = 1
    """
    id of last added Pattern
    @type: Integer
    """

    def __init__(self, file):
        """
        Constructor.
        @type file: String
        """
        self.patterns = list() #: @type: List<Pattern>
        if file == None:
            return

        file = pd.read_excel(file)
        for index, row in file.iterrows():
            id = int(row['id'])
            PatternsPool.maxID = max(PatternsPool.maxID, id)
            patternString = row['pattern']
            arg1 = PatternTemplateWord(row['arg1_case'], row['arg1_num'], row['arg1_pos'])
            arg2 = PatternTemplateWord(row['arg2_case'], row['arg2_num'], row['arg2_pos'])
            self.patterns.append(Pattern(id, patternString, arg1, arg2))

    def saveToFile(self, file):
        pass


    def getPatternByID(self, id):
        """
        Get pattern by id.

        @type id: Integer
        @param id: id of a pattern to get

        @rtype: Pattern | None
        @return: Pattern with given id if exists
        """
        for pattern in self.patterns:
            if pattern.id == id:
                return pattern
        return None

    def addPattern(self, pattern):
        """
        Add Pattern to PatternPool

        @type pattern: Pattern
        @param pattern: Pattern to add
        """
        self.patterns.append(pattern)


    def toJSON(self, file):
        """
        Save PatternPool to json.

        @type file: String
        @param file: Full path of file to save into
        """
        patternsJSON = dict()
        for i in range(0, len(self.patterns)):
            patternsJSON[i] = dict()
            patternsJSON[i]['pattern'] = self.patterns[i].pattern
            patternsJSON[i]['id'] = self.patterns[i].id
            patternsJSON[i]['arg1_case'] = self.patterns[i].arg1.case
            patternsJSON[i]['arg1_num'] = self.patterns[i].arg1.number
            patternsJSON[i]['arg1_pos'] = self.patterns[i].arg1.pos
            patternsJSON[i]['arg2_case'] = self.patterns[i].arg2.case
            patternsJSON[i]['arg2_num'] = self.patterns[i].arg2.number
            patternsJSON[i]['arg2_pos'] = self.patterns[i].arg2.pos

        with open(file, 'w') as data:
            json.dump(patternsJSON, data, ensure_ascii=False)
        return


    def clear(self):
        """
        Delete all Patterns from PatternPool.
        """
        self.patterns = list()


    def get_pattern_by_string(self, pattern_string):
        """
        Get Pattern by string.

        @type pattern_string: String
        @param pattern_string: string of a Pattern to get

        @rtype: Pattern | None
        @return: Pattern represented by the pattern_string if exists
        """
        for pattern in self.patterns:
            if pattern.pattern == pattern_string:
                return pattern
