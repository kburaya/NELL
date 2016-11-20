"""
Ontology.
Contains a list of categories to work with.
"""
import sys
sys.path.insert(0, '../src/classes')
from Category import Category
import pandas as pd
from pymystem3 import Mystem
import json
mystem = Mystem()


class Ontology:

    instances = list() #: @type: List<Category>

    def __init__(self, file):
        """
        Constructor.
        @type file: String
        """
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


    def toJSON(self, file):
        """
        Save Ontology to json.

        @type file: String
        @param file: Full path of file to save into
        """
        ontologyJSON = dict()
        for i in range(0, len(self.instances)):
            ontologyJSON[i] = dict()
            ontologyJSON[i]['categoryName'] = self.instances[i].categoryName
            try:
                if self.instances[i].instances.__len__() > 0:
                    ontologyJSON[i]['seedInstances'] = self.instances[i].instances
            except:
                ontologyJSON[i]['seedInstances'] = []

            try:
                if self.instances[i].extractionPatterns.__len__() > 0:
                    ontologyJSON[i]['seedExtractionPatterns'] = self.instances[i].extractionPatterns
            except:
                ontologyJSON[i]['seedExtractionPatterns'] = []

        with open(file, 'w') as data:
            json.dump(ontologyJSON, data, ensure_ascii=False)
        return