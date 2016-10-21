import sys
import pandas as pd
sys.path.insert(0, '/Users/kseniya/Documents/Study/NELL/CPL-python/src/classes')
from PatternTemplateWord import PatternTemplateWord
from Pattern import Pattern

class PatternsPool:
    maxID = 1
    def __init__(self, file):
        if file == None:
            self.patterns = list()
            return

        file = pd.read_excel(file)
        for index, row in file.iterrows():
            id = int(row['id'])
            maxID = max(maxID, id)
            patternString = row['pattern']
            arg1 = PatternTemplateWord(row['arg1_case'], row['arg1_num'], row['arg1_pos'])
            arg2 = PatternTemplateWord(row['arg2_case'], row['arg2_num'], row['arg2_pos'])
            self.patterns.append(Pattern(id, patternString, arg1, arg2))

    def saveToFile(self, file):
        pass

    def addPattern(self, pattern):
        self.patterns.append(pattern)