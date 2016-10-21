import sys
sys.path.insert(0, '/Users/kseniya/Documents/Study/NELL/CPL-python/src/classes')
import pandas as pd
from pymystem3 import Mystem

mystem = Mystem()


class Category:
    categoryName = ''
    instances = list() # list of IWord objects
    extractionPatterns = list() # ids of patterns from PatternsPool
    promotedInstances = dict()

    def __init__(self, categoryName, instances, extractionPatterns):
        self.categoryName = categoryName
        self.instances = instances
        self.extractionPatterns = extractionPatterns
        self.promotedInstances = dict()

    def addPromotedInstance(self, instance):
        self.promotedInstances.append(instance)