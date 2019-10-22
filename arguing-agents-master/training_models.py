import os
from Parsers import lstm_new
from Parsers import araucaria_new


path_to_corpus = os.getcwd() + '/complete'


arConstObj = araucaria_new.ConstDataSet()

arConstObj.readFile("2",  path_to_corpus)
arConstObj.extractFeatures()
arConstObj.buildSvm()
print("Created SVM")

word2vec = lstm_new.ConstWord2Vec()

word2vec.readTsvFileAndConstructDatasetNew2(path_to_corpus)
