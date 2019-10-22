from text_processing.text_processing import get_words
from comparison_methods.scoring_methods import compare3

from collections import Counter
from nltk.corpus import wordnet as wn
from nltk.corpus.reader import NOUN

def get_synsets(text):
    words = get_words(text)

    synsets = []

    for word in words:
        #print(word)
        word_synsets = wn.synsets(word, NOUN)

        if word_synsets == []:
            morpied_word = wn.morphy(word, NOUN)

            while morpied_word != None:
                word_synsets += wn.synsets(morphied_word, NOUN)
                morphied_word = wn.morphy(word, NOUN)

        synsets += word_synsets

    return synsets

def match_comment_to_argument(comment_text, argument_counts, scoring_function):
    comment_synsets = get_synsets(comment_text)

    c_synset_counts = Counter(comment_synsets)

    selected_comment_idx = 0
    selected_comment_score = 0

    for i in range(len(argument_counts)):
        a_c = argument_counts[i]

        shared_synset_counts = a_c & c_synset_counts
        score = scoring_function(shared_synset_counts, c_synset_counts, a_c)

        if score > selected_comment_score:
            selected_comment_idx = i
            selected_comment_score = score

    return selected_comment_idx, score, shared_synset_counts, comment_synsets

def match_comments_and_arguments(pro_texts, con_texts, comment_texts, scoring_function):
    argument_texts = pro_texts + con_texts

    matched_to_arg = {}
    matched_to_arg['pro'] = [[] for pro in pro_texts]
    matched_to_arg['con'] = [[] for con in con_texts]

    matched_to_comment = [[] for comment in comment_texts]

    argument_synset_counts = []

    for argument in argument_texts:
        argument_synset_counts.append(Counter(get_synsets(argument)))

    for comment_idx in range(len(comment_texts)):
        comment = comment_texts[comment_idx]

        matched_argument_idx, score, shared_synset_counts, comment_synset_count = match_comment_to_argument(comment, argument_synset_counts, scoring_function)

        if matched_argument_idx < len(pro_texts):
            polarity = 'pro'
        else:
            polarity = 'con'
            matched_argument_idx -= len(pro_texts)

        matched_to_arg[polarity][matched_argument_idx].append((comment_idx, score, comment_synset_count, argument_synset_counts[matched_argument_idx], shared_synset_counts))
        matched_to_comment[comment_idx].append((matched_argument_idx, score, comment_synset_count, argument_synset_counts[matched_argument_idx], shared_synset_counts))
    
    return {'matched_to_arg': matched_to_arg, 'matched_to_comment': matched_to_comment}

def match(comment_texts, pro_texts, con_texts, scoring_function = compare3):
    return match_comments_and_arguments(pro_texts, con_texts, comment_texts, scoring_function)