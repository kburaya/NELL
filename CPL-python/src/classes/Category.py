import sys
sys.path.insert(0, '../src/classes')
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

    def check_if_pattern_exists(self, pattern_string, pattern_pool):
        # check if we found existing pattern, then we need to skip it
        for pattern_id in self.extractionPatterns:
            pattern = pattern_pool.getPatternByID(pattern_id)
            if pattern.pattern == pattern_string:
                return True
        return False

    def check_if_promoted_instance_exists(self, promoted_instance):
        if promoted_instance in self.instances:
            return True
        return False