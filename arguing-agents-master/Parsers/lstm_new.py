#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 12:46:13 2018
@author: sandy
"""

# imports needed and logging
import pandas as pd
import re
#path_to_corpus = os.getcwd() + '/Corpora/araucaria/'
import gzip
import os,csv
os.environ['KERAS_BACKEND']='tensorflow'
import gensim
import sklearn
import nltk
import pickle
from collections import Counter
from nltk.tokenize import word_tokenize
from keras.preprocessing.text import Tokenizer
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.model_selection import train_test_split
from gensim.models import Word2Vec
from keras.models import Sequential
from keras import optimizers
from keras.preprocessing.text import one_hot
from keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from keras.models import model_from_json
from keras.layers import Activation
from keras.layers import Embedding
from keras.layers import LSTM
from keras.layers import Dense
from keras import utils
import json

import logging
import pandas as pd
import numpy as np

class ConstWord2Vec(object):
    def __init__(self):
        self.training_datafr = pd.DataFrame(columns=['Input', 'Output'])
        self.input_sen = []
        self.output_sen = []
        self.input = []
        self.output = []
        self.word_model = '';
        self.word_lists = []
        self.train_features = []
        self.lexicon = []
        self.new_lexicon = []
        self.output = []
        self.token_index = {}
        
    def readTsvFileAndConstructDatasetNew2(self, path_to_tsv):
        tsv_files = [pos_tsv for pos_tsv in os.listdir(path_to_tsv) if pos_tsv.endswith('.tsv')]
        word_lem = WordNetLemmatizer()
        for index, tsv_each_path in enumerate(tsv_files):
                print("Reading file "+tsv_each_path)
                train_file = pd.read_csv(os.path.join(path_to_tsv, tsv_each_path), delimiter='	',quoting=csv.QUOTE_NONE)
                for row_index, each_train in train_file.iterrows():
                    regex_sen = (re.sub('[^a-zA-z0-9\s]', '', each_train[4])).lower()
                    self.input_sen.append(regex_sen)
                    word_splits = word_tokenize(regex_sen)
                    self.lexicon += list(word_splits)
                    if each_train[5] == 'NoArgument':
                        self.output.append('0')
                    elif each_train[5] == 'Argument_for': 
                        self.output.append('1')
                    elif each_train[5] == 'Argument_against':
                        self.output.append('2')
        
        self.lexicon = [word_lem.lemmatize(i) for i in self.lexicon]
        self.lexicon = [word_lem.lemmatize(i, pos='v') for i in self.lexicon]
        
        w_counts = Counter(self.lexicon)
        for w in w_counts:
            if 1500 > w_counts[w]> 800 and "http" not in w:
                self.new_lexicon.append(w)
                
        for sen in self.input_sen:
            cur_words = word_tokenize(sen)
            cur_words = [word_lem.lemmatize(i) for i in cur_words]
            cur_words = [word_lem.lemmatize(i, pos='v') for i in cur_words]
            features = np.zeros(len(self.new_lexicon),dtype=int)
            for word in cur_words:
                if word in self.new_lexicon and  "http" not in word:
                    index_value = self.new_lexicon.index(word)
                    features[index_value] += 1
            features = list(features)
            self.train_features.append(features)
        
        np.save("dict_list", self.new_lexicon)
        max_length = 150
        batch_size = 32
        padded_sens = pad_sequences(self.train_features, maxlen=len(self.new_lexicon), padding='post')
        sgd = optimizers.SGD(lr=0.01, clipvalue=0.5)
        model = Sequential()
        model.add(Embedding(len(self.new_lexicon)+1, 1, input_length=len(self.new_lexicon)))
        model.add(LSTM(max_length, dropout_U = 0.2, dropout_W = 0.2))
        model.add(Dense(3,activation='softmax'))
        model.compile(loss = 'categorical_crossentropy', optimizer= sgd,metrics = ['accuracy'])
        print(model.summary())
        self.output = pd.get_dummies(self.output).values
        X_train, X_valid, Y_train, Y_valid = train_test_split(padded_sens,self.output, test_size = 0.20, random_state = 36)
        #Here we train the Network.
        model.fit(X_train, Y_train, batch_size =batch_size, nb_epoch = 10,  verbose = 5) # orinal 5 
        
        score,acc = model.evaluate(X_valid, Y_valid, verbose = 2, batch_size = batch_size)
        print("validation accuracy ",acc)
        model_json = model.to_json()
        with open("model.json", "w") as json_file:
            json_file.write(model_json)
        model.save_weights("model.h5")
        print("Saved model to disk")
        np.save("dict_list", self.new_lexicon)
            
    def load_model_new(self, sen_list, output):
        # load json and create model
        word_lem = WordNetLemmatizer()
        max_length = 150
        batch_size = 32
        tokenizer = ''
        json_file = open('model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        # load weights into new model
        loaded_model.load_weights("model.h5")
        print("Loaded model from disk")
        sgd = optimizers.SGD(lr=0.01, clipvalue=0.5)
        loaded_model.compile(loss = 'categorical_crossentropy', optimizer= sgd,metrics = ['accuracy'])
        regex_sen = (re.sub('[^a-zA-z0-9\s]', '', sen_list[0])).lower()
        word_splits = word_tokenize(regex_sen)
        word_splits = [word_lem.lemmatize(i, pos='v') for i in word_splits]
        word_splits = [word_lem.lemmatize(i) for i in word_splits]
        dict_list = np.load("dict_list.npy").tolist()
        features = np.zeros(len(dict_list),dtype=int)
        #print(dict_list.index('because'))
        #num = dict_list.index('because')
        for word in word_splits:
            if word in dict_list:
                print("inside dict_list ")
                index_value = dict_list.index(word)
                features[index_value] += 1
            features = list(features)
        #print(features[num])   
        print("after text to sequence")
        padded_sens = pad_sequences([features], maxlen=len(dict_list), padding='post')
        print("Predicition:")
        print(loaded_model.predict(padded_sens))
        score,acc = loaded_model.evaluate(padded_sens, np.array(output), verbose = 2, batch_size = batch_size)
        print("validation accuracy ",acc)
        
