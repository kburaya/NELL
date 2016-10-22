import sys
sys.path.insert(0, '/Users/kseniya/Documents/Study/NELL/CPL-python/src/classes')
import pandas as pd
from pymystem3 import Mystem

mystem = Mystem()


class Category:
    categoryName = ''
    instances = list()
    extractionPatterns = list() # ids of patterns from PatternsPool
    promotedInstances = dict()

    def __init__(self, categoryName, instances, extractionPatterns):
        self.categoryName = categoryName
        self.instances = instances
        self.extractionPatterns = extractionPatterns
        self.promotedInstances = dict()

    def addPromotedInstance(self, instance):
        for _instance in self.instances:
            if _instance == instance:
                return False
        self.instances.append(instance)
        return True

    def addPromotedPattern(self, pattern, patternPoolFrom, patternPool):
        # check if the same pattern from promoted pattern pool exists in actual pattern pool or in extraction patterns for category
        # check by string values of pattern

        for _patternID in self.extractionPatterns:
            if patternPool.getPatternByID(_patternID).pattern == patternPoolFrom.getPatternByID(pattern.id).pattern:
                return False
        self.extractionPatterns.append(pattern.id)
        return True