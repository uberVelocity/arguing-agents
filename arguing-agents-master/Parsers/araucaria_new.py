#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 19:29:38 2018
"""

import os, json, csv
from os.path import basename
import collections
import ntpath
import re
import numpy as np
import difflib
import pandas as pd
import nltk
import sklearn
from sklearn import svm
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.decomposition import SparsePCA
from sklearn.svm import SVC
from nltk.tokenize import sent_tokenize
from scipy import sparse
from collections import Counter
path_to_corpus = os.getcwd() + '/Corpora/araucaria/'


class ConstDataSet(object):
    def __init__(self):
        self.dataset = pd.DataFrame(columns=['Input', 'Output'])
        self.tagDataSet = pd.DataFrame(columns=['Input', 'Output'])
        self.input_arr = [];
        self.output_label_arr = [];
        #self.tagDataSet = pd.DataFrame(columns=['UNI_BIGRAM_TRI', 'VB_C', 'ADV_C', 'AVG_WORD', 'SEN_LEN', 'OUTPUT'])
        self.training_datafr = pd.DataFrame(columns=['Input', 'Output'])
        self.discourse_markers_list = ['where','as a consequence','as a result','as soon as', 'because','certainly','consequently','correspondingly',
                                       'despite the fact that','even','first','firstly','for instance','further','accordingly','admittedly','after that','as long as',
                                       'but','clearly','conversely','despite that','else','then','eventually','except','finally','for this reason','furthermore','given that',
                                       'however','if ever','if only','in case','in particular','not because','obviously','on condition that','hence','if','in conclusion','in any case',
                                       'in fact','in short','because','moreover','now that','of course','or else','subsequently','supposing that','summarise','ultimately','unless','since',
                                       'so that','such that','therefore','thereafter','conclude','sum up','example','extent that','true','undoubtedly','until','yet']
        self.switcher = {
                "0": self.readJsonFileAndConstructDataset,
                "1": self.readTxtFileAndConstructDataset,
                "2": self.readTsvFileAndConstructDataset
        }
    def readJsonFileAndConstructDataset(self,path_to_json):
        json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
        json_data = pd.DataFrame(columns=['Input', 'Output'])
        for index, js in enumerate(json_files):
            with open(os.path.join(path_to_json, js)) as json_file:
                json_text = json.load(json_file)
                for arTextNode in json_text['nodes']:
                    if  arTextNode['text'] and (arTextNode['text'] != 'RA' and arTextNode['text'] != 'CA') and not(arTextNode['text'].startswith('YA_')):
                        json_data.loc[index] = [arTextNode['text'], '1']
        
        self.dataset = self.dataset.append(json_data)
        print(self.dataset.size)
        
        
    def readTxtFileAndConstructDataset(self,path_to_txt):
        non_arg_list = [];
        txt_files = [pos_txt for pos_txt in os.listdir(path_to_txt) if pos_txt.endswith('.txt')]
        jsons_data = pd.DataFrame(columns=['Input', 'Output'])
        for index, tx in enumerate(txt_files):
            with open(os.path.join(path_to_txt, tx)) as txt_file:
                if (ntpath.basename(txt_file.name)+"") != "araucaria-concatenated.txt":
                    text_data = txt_file.read()
                    sentences = sent_tokenize(text_data)
                    for sen in sentences:
                        non_arg_list.append(sen)
        self.parseNonArgData(non_arg_list)
                
    def parseNonArgData(self,non_arg_list):
        arg_list = self.dataset['Input']
        for each_non_arg in non_arg_list:
            max_match_sent = ""
            max_Match = 0;
            
            for arg in arg_list:
                SM = difflib.SequenceMatcher(None, each_non_arg, arg)
                match  = SM.find_longest_match(0, len(each_non_arg), 0, len(arg))
                if match.size > max_Match:
                    max_match_sent = arg;
                max_Match = max(match.size, max_Match)
            
            #if (len(each_non_arg)-max_Match <20):
                
            if (len(each_non_arg)-max_Match >20):
                eachNonArgDf = pd.DataFrame(columns=['Input', 'Output'])
                eachNonArgDf.loc[0] = [each_non_arg, '0']
                self.dataset.append(eachNonArgDf)
        
        self.dataset.to_csv('dataset.csv')
                
    def readTsvFileAndConstructDataset(self, path_to_tsv):
        tsv_files = [pos_tsv for pos_tsv in os.listdir(path_to_tsv) if pos_tsv.endswith('.tsv')]
        word_lem = WordNetLemmatizer()
        datafr_index=0;
        for index, tsv_each_path in enumerate(tsv_files):
                print("Reading file "+tsv_each_path)
                train_file = pd.read_csv(os.path.join(path_to_tsv, tsv_each_path), delimiter='	', encoding='utf-8',quoting=csv.QUOTE_NONE)

                for row_index, each_train in train_file.iterrows():
                    regex_sen = (re.sub('[^a-zA-z0-9\s]', '', each_train[4])).lower()
                    word_splits = word_tokenize(regex_sen)
                    word_splits = [word_lem.lemmatize(i, pos='v') for i in word_splits]
                    word_splits = [word_lem.lemmatize(i) for i in word_splits]
                    recon_sen = ' '.join(word for word in word_splits)
                    if each_train[5] == 'NoArgument':
                        if len(word_splits) > 3:
                            self.training_datafr.loc[datafr_index] = [recon_sen, '0']
                    else :
                        if len(word_splits) > 3:
                            self.training_datafr.loc[datafr_index] = [recon_sen, '1']
                    datafr_index+=1
        print(self.training_datafr.head(2))
        #shuffle the data
        self.training_datafr = self.training_datafr.sample(frac=1).reset_index(drop=True)
        print("--------------------")
        print(len(self.training_datafr.loc[self.training_datafr['Output'] == '1']))
        print(len(self.training_datafr.loc[self.training_datafr['Output'] == '0']))
        print("--------------------")
        print(self.training_datafr.head(2))
                
    def extractVerbs(self):
        #old method of extracting features(contains only verb count, adv count, avg .....)
        for index, row in self.training_datafr.iterrows():
            
            sen_tok = nltk.word_tokenize(row['Input'])
            sen_tags = nltk.pos_tag(sen_tok, tagset='universal')
            tag_counts = Counter(tag for word,tag in sen_tags)
            total_tag_count = sum(tag_counts.values())
            avg_tag_counts = dict((word, float(count)/total_tag_count) for word,count in tag_counts.items())
            VB_count = avg_tag_counts.get('VERB', 0)
            Adv_count = avg_tag_counts.get('ADV', 0)
            punct_count = avg_tag_counts.get('.', 0)
            words = row['Input'].split()
            avg_word_len = sum(len(word) for word in words) / len(words)
            sen_len = len(row['Input'])
            #self.tagDataSet.loc[index] = [[VB_count, Adv_count, avg_word_len, punct_count, sen_len], row['Output']]
            self.input_arr.append([VB_count, Adv_count, avg_word_len, punct_count, sen_len])
            self.output_label_arr.append(row['Output'])
#            tag_fd = nltk.FreqDist(tag for (word, tag) in sen_tags)
#            
#            tag_list = []
#            for word, tag in sen_tags:
#                if tag == 'VB' or tag == 'VBP' or tag == 'RB':
#                    
#                    tag_list.append(word)
    def extractFeatures(self):
        sentence_rows = self.training_datafr['Input']
        #construction of unigrmas till trigrams the next three steps
        n_gram_range = CountVectorizer(ngram_range=(1,3), max_features=1000)
        uni_bi_tri_vector = n_gram_range.fit_transform(sentence_rows).toarray()
        tfidf_vector = TfidfTransformer().fit_transform(uni_bi_tri_vector).toarray()
        print("size of vector ",tfidf_vector[0].size)
        for index, row in self.training_datafr.iterrows():
            sen_tok = nltk.word_tokenize(row['Input'])
            sen_tags = nltk.pos_tag(sen_tok)
            tag_counts = Counter(tag for word,tag in sen_tags)
            total_tag_count = sum(tag_counts.values())
            avg_tag_counts = dict((word, float(count)/total_tag_count) for word,count in tag_counts.items())
            VB_count = avg_tag_counts.get('VB', 0)
            Adv_count = avg_tag_counts.get('RB', 0)
            Mod_count = avg_tag_counts.get('MD', 0)
            Aux_val = 0
            if any(word in row['Input'] for word in self.discourse_markers_list):
                Aux_val = 1
            #punct_count = avg_tag_counts.get('.', 0)
            words = row['Input'].split()
            avg_word_len = sum(len(word) for word in words) / len(words)
            sen_len = len(row['Input'])
            #self.tagDataSet.loc[index] = [[VB_count, Adv_count, avg_word_len, punct_count, sen_len], row['Output']]
            #self.input_arr.append([uni_bi_tri_vector[index].tolist(),VB_count, Adv_count, avg_word_len, sen_len])
            #self.input_arr.append([['a'],VB_count, Adv_count, avg_word_len, sen_len])
#            self.input_arr.append([VB_count, Adv_count, Mod_count, avg_word_len, sen_len])
            self.input_arr.append(np.append(tfidf_vector[index],[VB_count, Adv_count, Mod_count, Aux_val, avg_word_len, sen_len]))
            self.output_label_arr.append(row['Output'])
            
                
    def buildSvm(self):
        svm_model = svm.SVC(gamma='scale')
        #Reducing the dimensions
#        X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split( self.tagDataSet['Input'], self.tagDataSet['Output'], test_size=0.33, random_state=42)
#        print("started reducing the dimensions")
#        transformer = SparsePCA(n_components=100,normalize_components=True,random_state=0)
#        input_arr_transform =  transformer.fit_transform(self.input_arr)
#        print("Reduced dimensions ",input_arr_transform.shape)
        X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(self.input_arr, self.output_label_arr, test_size=0.20, random_state=42)
        print("--------------")
        print("test length")
        print(len(y_train))
        print(y_test)
        print(len([x for x in y_test if x=='1']))
#        X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(input_arr_transform, self.output_label_arr, test_size=0.33, random_state=42)
        print("Building SVM for Dataset of length ",len(X_train))
        print(self.input_arr[1])
        #train_sparse = sparse.csr_matrix(np.asarray(self.input_arr))
        svm_model.fit(X_train, y_train)
        SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0, decision_function_shape='ovr', degree=3, gamma='scale', kernel='rbf',
            max_iter=-1, probability=False, random_state=None, shrinking=True,
            tol=0.001, verbose=False)
        y_predict = svm_model.predict(X_test)
        print("Predicted Accuracies for Dataset of length ",len(X_test))
        print("The predicted accuracy is ",sklearn.metrics.accuracy_score(y_test, y_predict, normalize=True, sample_weight=None))

    def readFile(self, type, path):
        # Get the function from switcher dictionary
        func = self.switcher.get(type)
        # Execute the function
        func(path)
        
    def readTsvFileAndConstructDataset_old(self, path_to_tsv):
        tsv_files = [pos_tsv for pos_tsv in os.listdir(path_to_tsv) if pos_tsv.endswith('.tsv')]
        csv_files = [pos_tsv for pos_tsv in os.listdir(path_to_tsv) if pos_tsv.endswith('.csv')]
        for index, tsv_each_path in enumerate(tsv_files):
            if tsv_each_path != "school_uniforms.tsv":
                print("Reading file "+tsv_each_path)
                train_file = pd.read_csv(os.path.join(path_to_tsv, tsv_each_path), delimiter='	',encoding='utf-8', equoting=csv.QUOTE_NONE)
                for row_index, each_train in train_file.iterrows():
                    regex_sen = re.sub('[^a-zA-z0-9\s]', '', each_train[4])
                    word_splits = regex_sen.split()
                    #considering only sentences having word length > 3
                    if len(word_splits) > 3:
                        self.word_lists.append(regex_sen)
                        if each_train[5] == 'NoArgument':
                            self.output.append('0')
                        else:
                            self.output.append('1') 
                    
        for index, csv_each_path in enumerate(csv_files):
            print(csv_files)
            train_file = pd.read_csv(os.path.join(path_to_tsv, csv_each_path), delimiter=',',encoding='utf-8', error_bad_lines=False)
            print("reading file "+csv_each_path)
            for row_index, each_train in train_file.iterrows():
                regex_sen = re.sub('[^a-zA-z0-9\s]', '', each_train[4])
                word_splits = regex_sen.split()
                #considering only sentences having word length > 3
                if len(word_splits) > 3:
                    self.word_lists.append(regex_sen)
                    if each_train[5] == 'NoArgument':
                        self.output.append('0')
                    else:
                        self.output.append('1') 

#        vocab_size = 10000
#        max_length = 150
#        batch_size = 32
#        encoded_sens = [one_hot(d, vocab_size) for d in self.word_lists]
#        print(encoded_sens)
#        word_hot_dic = {}
#        ind=0
#        print("encc ")
##        print(encoded_sens)
#        for sen in self.word_lists:
#            words = sen.split()
#            print(sen)
#            print(encoded_sens[ind])
#            for i in range(len(words)):
##                print(words[i])
#                if not words[i] in word_hot_dic:
##                    print(i,ind)
#                    word_hot_dic[words[i]+''] = encoded_sens[ind][i]
#            ind+=1
#        padded_sens = pad_sequences(encoded_sens, maxlen=max_length, padding='post')
#        model = Sequential()
#        model.add(Embedding(vocab_size, 100, input_length=max_length))
#        model.add(LSTM(max_length, dropout_U = 0.2, dropout_W = 0.2))
#        model.add(Dense(2,activation='softmax'))
#        model.compile(loss = 'categorical_crossentropy', optimizer='adam',metrics = ['accuracy'])
#        print(model.summary())
#        self.output = pd.get_dummies(self.output).values
#        X_train, X_valid, Y_train, Y_valid = train_test_split(padded_sens,self.output, test_size = 0.20, random_state = 36)
#        #Here we train the Network.
#        model.fit(X_train, Y_train, batch_size =batch_size, nb_epoch = 1,  verbose = 5)
#        score,acc = model.evaluate(X_valid, Y_valid, verbose = 2, batch_size = batch_size)
#        print("validation accuracy ",acc)
#        model_json = model.to_json()
#        with open("model.json", "w") as json_file:
#            json_file.write(model_json)
#        model.save_weights("model.h5")
#        print("Saved model to disk")
#        json_new = json.dumps(word_hot_dic)
#        f = open("dict.json","w")
#        f.write(json_new)
#        f.close()
        
    
        
        
        
        
        

