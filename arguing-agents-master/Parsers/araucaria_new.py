#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 19:29:38 2018
"""

import os
import json
import csv
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

        self.input_arr = []
        self.output_label_arr = []

        self.training_datafr = pd.DataFrame(columns=['Input', 'Output'])
        
        self.discourse_markers_list = ['where', 'as a consequence', 'as a result', 'as soon as', 'because', 'certainly', 'consequently', 'correspondingly',
                                       'despite the fact that', 'even', 'first', 'firstly', 'for instance', 'further', 'accordingly', 'admittedly', 'after that', 'as long as',
                                       'but', 'clearly', 'conversely', 'despite that', 'else', 'then', 'eventually', 'except', 'finally', 'for this reason', 'furthermore', 'given that',
                                       'however', 'if ever', 'if only', 'in case', 'in particular', 'not because', 'obviously', 'on condition that', 'hence', 'if', 'in conclusion', 'in any case',
                                       'in fact', 'in short', 'because', 'moreover', 'now that', 'of course', 'or else', 'subsequently', 'supposing that', 'summarise', 'ultimately', 'unless', 'since',
                                       'so that', 'such that', 'therefore', 'thereafter', 'conclude', 'sum up', 'example', 'extent that', 'true', 'undoubtedly', 'until', 'yet']
        
        self.switcher = {
            "0": self.readJsonFileAndConstructDataset,
            "1": self.readTxtFileAndConstructDataset,
            "2": self.readTsvFileAndConstructDataset
        }

    def readJsonFileAndConstructDataset(self, path_to_json):
        json_files = [pos_json for pos_json in os.listdir(
            path_to_json) if pos_json.endswith('.json')]

        json_data = pd.DataFrame(columns=['Input', 'Output'])

        for index, js in enumerate(json_files):
            with open(os.path.join(path_to_json, js)) as json_file:
                json_text = json.load(json_file)
                for arTextNode in json_text['nodes']:
                    if arTextNode['text'] and (arTextNode['text'] != 'RA' and arTextNode['text'] != 'CA') and not(arTextNode['text'].startswith('YA_')):
                        json_data.loc[index] = [arTextNode['text'], '1']

        self.dataset = self.dataset.append(json_data)

        print(self.dataset.size)

    def readTxtFileAndConstructDataset(self, path_to_txt):
        non_arg_list = []

        txt_files = [pos_txt for pos_txt in os.listdir(
            path_to_txt) if pos_txt.endswith('.txt')]

        for index, tx in enumerate(txt_files):
            with open(os.path.join(path_to_txt, tx)) as txt_file:
                if (ntpath.basename(txt_file.name)+"") != "araucaria-concatenated.txt":
                    text_data = txt_file.read()
                    sentences = sent_tokenize(text_data)
                    for sen in sentences:
                        non_arg_list.append(sen)
                        
        self.parseNonArgData(non_arg_list)

    def parseNonArgData(self, non_arg_list):
        arg_list = self.dataset['Input']

        for each_non_arg in non_arg_list:
            max_Match = 0

            for arg in arg_list:
                SM = difflib.SequenceMatcher(None, each_non_arg, arg)

                match = SM.find_longest_match(
                    0, len(each_non_arg), 0, len(arg))

                if match.size > max_Match:
                    max_match_sent = arg
                    
                max_Match = max(match.size, max_Match)

            if (len(each_non_arg)-max_Match > 20):
                eachNonArgDf = pd.DataFrame(columns=['Input', 'Output'])
                eachNonArgDf.loc[0] = [each_non_arg, '0']
                self.dataset.append(eachNonArgDf)

        self.dataset.to_csv('dataset.csv')

    def readTsvFileAndConstructDataset(self, path_to_tsv):
        tsv_files = [pos_tsv for pos_tsv in os.listdir(
            path_to_tsv) if pos_tsv.endswith('.tsv')]

        word_lem = WordNetLemmatizer()

        datafr_index = 0

        for index, tsv_each_path in enumerate(tsv_files):
            print("Reading file "+tsv_each_path)

            train_file = pd.read_csv(os.path.join(
                path_to_tsv, tsv_each_path), delimiter='	', encoding='utf-8', quoting=csv.QUOTE_NONE)

            for row_index, each_train in train_file.iterrows():
                regex_sen = (
                    re.sub('[^a-zA-z0-9\s]', '', each_train[4])).lower()

                word_splits = word_tokenize(regex_sen)
                word_splits = [word_lem.lemmatize(
                    i, pos='v') for i in word_splits]
                word_splits = [word_lem.lemmatize(i) for i in word_splits]

                recon_sen = ' '.join(word for word in word_splits)

                if each_train[5] == 'NoArgument':
                    if len(word_splits) > 3:
                        self.training_datafr.loc[datafr_index] = [
                            recon_sen, '0']
                elif each_train[5] == 'Argument_for':
                    if len(word_splits) > 3:
                        self.training_datafr.loc[datafr_index] = [
                            recon_sen, '1']
                elif each_train[5] == 'Argument_against':
                    if len(word_splits) > 3:
                        self.training_datafr.loc[datafr_index] = [
                            recon_sen, '2']

                datafr_index += 1

        print(self.training_datafr.head(2))

        # shuffle the data
        self.training_datafr = self.training_datafr.sample(
            frac=1).reset_index(drop=True)

        print("--------------------")
        print(
            len(self.training_datafr.loc[self.training_datafr['Output'] == '2']))
        print(
            len(self.training_datafr.loc[self.training_datafr['Output'] == '1']))
        print(
            len(self.training_datafr.loc[self.training_datafr['Output'] == '0']))
        print("--------------------")
        print(self.training_datafr.head(2))

    def extractFeatures(self):
        # put the training input (training has input and labels) in sentence_rows
        sentence_rows = self.training_datafr['Input']

        # construction of unigrmas till trigrams the next three steps
        n_gram_range = CountVectorizer(ngram_range=(1, 3), max_features=1000)

        uni_bi_tri_vector = n_gram_range.fit_transform(sentence_rows).toarray()
        tfidf_vector = TfidfTransformer().fit_transform(uni_bi_tri_vector).toarray()

        print("size of vector ", tfidf_vector[0].size)

        for index, row in self.training_datafr.iterrows():
            sen_tok = nltk.word_tokenize(row['Input'])

            sen_tags = nltk.pos_tag(sen_tok)
            tag_counts = Counter(tag for word, tag in sen_tags)
            total_tag_count = sum(tag_counts.values())
            avg_tag_counts = dict((word, float(count)/total_tag_count)
                                  for word, count in tag_counts.items())

            VB_count = avg_tag_counts.get('VB', 0)
            Adv_count = avg_tag_counts.get('RB', 0)
            Mod_count = avg_tag_counts.get('MD', 0)

            Aux_val = 0
            
            if any(word in row['Input'] for word in self.discourse_markers_list):
                Aux_val = 1

            words = row['Input'].split()
            avg_word_len = sum(len(word) for word in words) / len(words)
            sen_len = len(row['Input'])

            self.input_arr.append(np.append(tfidf_vector[index], [
                                  VB_count, Adv_count, Mod_count, Aux_val, avg_word_len, sen_len]))
            self.output_label_arr.append(row['Output'])

    def buildSvm(self):
        svm_model = svm.SVC(gamma='scale')

        X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(
            self.input_arr, self.output_label_arr, test_size=0.20, random_state=42)

        print("--------------")
        print("test length")
        print(len(y_train))
        print(len([x for x in y_test if x == '1']))

        print("Building SVM for Dataset of length ", len(X_train))
        print(self.input_arr[1])

        svm_model.fit(X_train, y_train)

        SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0, decision_function_shape='ovr', degree=3, gamma='scale', kernel='rbf',
            max_iter=-1, probability=False, random_state=None, shrinking=True,
            tol=0.001, verbose=False)

        y_predict = svm_model.predict(X_test)

        print("Predicted Accuracies for Dataset of length ", len(X_test))
        print("The predicted accuracy is ", sklearn.metrics.accuracy_score(
            y_test, y_predict, normalize=True, sample_weight=None))

    def readFile(self, type, path):
        # Get the function from switcher dictionary
        func = self.switcher.get(type)

        # Execute the function
        func(path)
