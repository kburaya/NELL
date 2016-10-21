import sys
sys.path.insert(0, '/Users/kseniya/Documents/Study/NELL/CPL-python/src/classes')
from Category import Category
import pandas as pd
from pymystem3 import Mystem
mystem = Mystem()


class Ontology:
    instances = list()

    def __init__(self, file):
        file = pd.read_excel(file)
        self.instances = list()
        for index, row in file.iterrows():
            categoryName = mystem.lemmatize(row['categoryName'])[0]
            if type(row['seedInstances']) is float:
                instances = list()
            else:
                instances = row['seedInstances'].split('"')[1::2]
            if type(row['seedExtractionPatterns']) is float:
                extractionPatterns = list
            else:
                extractionPatterns = [int(s) for s in row['seedExtractionPatterns'].split(' ') if s.isdigit()]

            self.instances.append(Category(categoryName, instances, extractionPatterns))
        return
