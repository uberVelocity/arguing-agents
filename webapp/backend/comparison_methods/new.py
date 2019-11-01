

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
    for t in token: 
        if t in dic.keys(): 
            prob += dic[t] 
        else: 
            prob +=0
        
    print("prob=" , prob)
    return prob

def match(argument_texts, pro_texts, con_texts):

    return comment_rank_pro_args, comment_rank_con_args