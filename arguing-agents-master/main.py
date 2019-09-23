import os
from Parsers import lstm_new
from Parsers import araucaria_new


path_to_corpus = os.getcwd() + '/complete'


arConstObj = araucaria_new.ConstDataSet()

arConstObj.readFile("2",  path_to_corpus)
arConstObj.extractFeatures()
##arConstObj.extractVerbs()
arConstObj.buildSvm()
#print(len(data))
#print(data[0].plain)


word2vec = lstm_new.ConstWord2Vec()
word2vec.readTsvFileAndConstructDatasetNew2(path_to_corpus)
word2vec.load_model_new(["becauseUS Supreme Court majority opinion, Justice Antonin Scalia, LLB, wrote, Like most rights, the right secured by the Second Amendment is not unlimited… nothing in our opinion should be taken to cast doubt on longstanding prohibitions on the possession of firearms by felons and the mentally ill, or laws forbidding the carrying of firearms in sensitive places such as schools and government buildings, or laws imposing conditions and qualifications on the commercial sale of arms."],[['0','1','2']])
