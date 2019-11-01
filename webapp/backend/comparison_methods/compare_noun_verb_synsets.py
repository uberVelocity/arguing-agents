import spacy

from text_processing.text_processing import get_words
from comparison_methods.scoring_methods import compare3

from collections import Counter
from nltk.corpus import wordnet as wn
from nltk.corpus.reader import NOUN, VERB, ADJ, ADV

nlp = spacy.load("en_core_web_sm")

pos_spacy2nltk = {'NOUN': NOUN, 'PROPN': NOUN, 'VERB': VERB, 'ADV': ADV, 'ADJ': ADJ}

def get_synsets(text):
    tokens = nlp(text)

    synsets = []

    for t in tokens:
        if t.pos_ in pos_spacy2nltk:
            nltk_pos = pos_spacy2nltk[t.pos_]
            word = t.text
            word_synsets = wn.synsets(word, nltk_pos)

            if word_synsets == []:
                morpied_word = wn.morphy(word, nltk_pos)

                while morpied_word != None:
                    word_synsets += wn.synsets(morphied_word, nltk_pos)
                    morphied_word = wn.morphy(word, nltk_pos)

            synsets += word_synsets

    return synsets
    
def match(comment_texts, pro_texts, con_texts, scoring_function = compare3):
    pro_texts_wc, con_texts_wc, comment_texts_wc = [], [], []

    for pro_text in pro_texts:
        synsets = get_synsets(pro_text)
        pro_texts_wc.append(Counter(synsets))

    for con_text in con_texts:
        synsets = get_synsets(con_text)
        con_texts_wc.append(Counter(synsets))

    for comment_text in comment_texts:
        synsets = get_synsets(comment_text)
        comment_texts_wc.append(Counter(synsets))

    comment_rank_pro_args = []
    comment_rank_con_args = []

    for pro_text_wc in pro_texts_wc:
        score_comment_tuples = []

        for i in range(len(comment_texts_wc)):
            comment_text_wc = comment_texts_wc[i]
            score = scoring_function(pro_text_wc & comment_text_wc, comment_text_wc, pro_text_wc)
            score_comment_tuples.append((score, i))

        comment_rank_pro_args.append(sorted(score_comment_tuples, key = lambda tup: tup[0], reverse = True))

    for con_text_wc in con_texts_wc:
        score_comment_tuples = []

        for i in range(len(comment_texts_wc)):
            comment_text_wc = comment_texts_wc[i]
            score = scoring_function(con_text_wc & comment_text_wc, comment_text_wc, con_text_wc)
            score_comment_tuples.append((score, i))

        comment_rank_con_args.append(sorted(score_comment_tuples, key = lambda tup: tup[0], reverse = True))

    return comment_rank_pro_args, comment_rank_con_args
    