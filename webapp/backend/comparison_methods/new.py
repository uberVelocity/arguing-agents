from nltk.tokenize import word_tokenize
import math



def addWords (word, dic): 
    if len(word) > 5: 
        if word in dic.keys(): 
            # print('found', word) 
            dic[word] += 1 
        else: 
            dic[word] = 1 


def createDictandCounter (string, dic):
    counter =0  
    # print(string)
    tokened = word_tokenize(string)
    for t in tokened:
        counter+=1 
        addWords(t, dic)
    return counter 

def computeProbWord(counter, dic): 
    # print('counter', counter)
    for item in dic: 
        dic[item] /= counter
        dic[item] = math.log2(dic[item])

def createDictMain (string1, dic):
    counter_all = createDictandCounter(string1, dic)
    computeProbWord(counter_all,dic)

def checkRelevance(comment, dic):
    token = word_tokenize(comment) 
    prob = 0 
    if len(comment) > 10:  
        for t in token: 
            if t in dic.keys(): 
                prob += dic[t] 
            else: 
                prob +=0
    else: 
        prob = math.log2(0.00001) 
    
    print("comment", comment) 
    print("prob=" , prob)
    return prob

def match(argument_texts, pro_texts, con_texts):

    comment_rank_pro_args = []
    for pro_text in pro_texts: 
        dic = {}
        score_comment_tuples = []
        createDictMain (pro_text,dic)
        index = 0 
        for comment in argument_texts: 
            score = checkRelevance(comment, dic)
            score_comment_tuples.append(score, index) 

        comment_rank_pro_args.append(sorted(score_comment_tuples, key = lambda tup: tup[0], reverse = True))
        dic.clear() 

    comment_rank_con_args = []

    for con_text in con_text: 
        dic = {} 
        score_comment_tuples = []
        createDictMain(con_text, dic)
        index = 0 
        for comment in argument_texts: 
            score = checkRelevance(comment, dic) 
            score_comment_tuples.append(score, index)

        comment_rank_con_args.append(sorted(score_comment_tuples, key = lambda tup: tup[0], reverse = True))
        dic.clear() 
        
    return comment_rank_pro_args, comment_rank_con_args
