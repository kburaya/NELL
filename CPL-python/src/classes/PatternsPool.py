import sys
import pandas as pd
sys.path.insert(0, '../src/classes')
from PatternTemplateWord import PatternTemplateWord
from Pattern import Pattern
import json


class PatternsPool:
    maxID = 1

    def __init__(self, file):
        self.patterns = list()
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
        for pattern in self.patterns:
            if pattern.id == id:
                return pattern
        return None

    def addPattern(self, pattern):
        self.patterns.append(pattern)


    def toJSON(self, file):
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
        self.patterns = list()


    def get_pattern_by_string(self, pattern_string):
        for pattern in self.patterns:
            if pattern.pattern == pattern_string:
                return pattern
