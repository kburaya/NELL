import sys
sys.path.insert(0, '../src/classes')
import pandas as pd
from pymystem3 import Mystem

mystem = Mystem()


class Category:
    categoryName = '' #: @type: String
    instances = list() #: @type: List<String>
    extractionPatterns = list()
    """
    ids of patterns from PatternsPool
    @type: List<Integer>
    """

    promotedInstances = dict() #: @type: Dictionary<String, Double>

    def __init__(self, categoryName, instances, extractionPatterns):
        """
        Constructor.
        @type categoryName: String
        @type instances: List<String>
        @type extractionPatterns: List<Integer>
        """
        self.categoryName = categoryName
        self.instances = instances
        self.extractionPatterns = extractionPatterns
        self.promotedInstances = dict()

    def addPromotedInstance(self, instance):
        """
        Add instance to category.

        @type instance: String
        @param instance: instance to add

        @rtype: Boolean
        @return: True if instance successfully added, False if instance already exists.
        """
        for _instance in self.instances:
            if _instance == instance:
                return False
        self.instances.append(instance)
        return True

    def addPromotedPattern(self, pattern, patternPoolFrom, patternPool):
        """
        Check if the same pattern from promoted pattern pool exists in actual pattern pool or
        in extraction patterns for category.

        @type pattern: String
        @param pattern: pattern to check

        @type patternPoolFrom: PatternPool
        @param patternPoolFrom: promoted PatternPool

        @type patternPool: PatternPool
        @param patternPool: actual PatternPool

        @rtype: Boolean
        @return: False if already exists, True if pattern not exists and will be added to category.
        """
        for _patternID in self.extractionPatterns:
            if patternPool.getPatternByID(_patternID).pattern == patternPoolFrom.getPatternByID(pattern.id).pattern:
                return False
        self.extractionPatterns.append(pattern.id)
        return True

    def check_if_pattern_exists(self, pattern_string, pattern_pool):
        """
        Check if Pattern exists in PatternPool.
        -- # check if we found existing pattern, then we need to skip it

        @type pattern_string: String
        @param pattern_string: pattern_string of Pattern to check

        @type pattern_pool: PatternPool
        @param pattern_pool: PatternPool to check in

        @rtype: Boolean
        @return: if exists
        """
        for pattern_id in self.extractionPatterns:
            pattern = pattern_pool.getPatternByID(pattern_id)
            if pattern.pattern == pattern_string:
                return True
        return False

    def check_if_promoted_instance_exists(self, promoted_instance):
        """
        Check if promoted instance exists in category instances.

        @type promoted_instance: String
        @param promoted_instance: instance to check

        @rtype: Boolean
        @return: if exists
        """
        if promoted_instance in self.instances:
            return True
        return False