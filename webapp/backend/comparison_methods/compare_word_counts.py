import re
from collections import Counter
from comparison_methods.scoring_methods import compare3

def match(comment_texts, pro_texts, con_texts, scoring_function = compare3):
    similarity_matrix_pro = []
    similarity_matrix_con = []

    pro_word_counts = []
    con_word_counts = []
    comment_word_counts = []

    for pro_text in pro_texts:
        words = pro_text.split(' ')
        pro_word_count = Counter(words)
        pro_word_counts.append(pro_word_count)

    for con_text in con_texts:
        words = con_text.split(' ')
        con_word_count = Counter(words)
        con_word_counts.append(con_word_count)

    for comment_text in comment_texts:
        text = comment_text.replace("\t", " ").replace("\n", " ")
        sentences = re.split(r'[\.\?\!] \s*(?![^()]*\))', text)
        words = []

        for sentence in sentences:
            words += sentence.split(" ")

        comment_word_count = Counter(words)
        comment_word_counts.append(comment_word_count)

    for pro_word_count in pro_word_counts:
        score_index_tuples = []
        for i in range(len(comment_word_counts)):
            comment_word_count = comment_word_counts[i]
            matching_word_count = pro_word_count & comment_word_count
            similarity_score = scoring_function(matching_word_count, comment_word_count, pro_word_count)
            score_index_tuples.append((similarity_score, i))
        similarity_matrix_pro.append(score_index_tuples.copy())

    for con_word_count in con_word_counts:
        score_index_tuples = []
        for i in range(len(comment_word_counts)):
            comment_word_count = comment_word_counts[i]
            matching_word_count = con_word_count & comment_word_count
            similarity_score = scoring_function(matching_word_count, comment_word_count, con_word_count)
            score_index_tuples.append((similarity_score, i))
        similarity_matrix_con.append(score_index_tuples.copy())

    return similarity_matrix_pro, similarity_matrix_con
            
    




    matched_to_arg = {}
    matched_to_arg['pro'] = [[] for pro in pro_texts]
    matched_to_arg['con'] = [[] for con in con_texts]

    matched_to_comment = [[] for comment in comment_texts]
    
    arg_word_counts = []

    for i in range(len(pro_texts)):
        arg = pro_texts[i]
        awc_tuple = ('pro', i, Counter(arg.split(' ')))
        arg_word_counts.append(awc_tuple)

    for i in range(len(con_texts)):
        arg = con_texts[i]
        awc_tuple = ('con', i, Counter(arg.split(' ')))
        arg_word_counts.append(awc_tuple)

    for comment_idx in range(len(comment_texts)):
        text = comment_texts[comment_idx]
        text = text.replace("\t", " ").replace("\n", " ")
        
        m = re.split(r'[\.\?\!] \s*(?![^()]*\))', text)

        words = []

        for sentence in m:
            words += sentence.split(" ")

        comment_word_count = Counter(words)

        #maxScore1 = [0, "", "", ""]
        #maxScore2 = [0, "", "", ""]

        # score = -1
        # best_tuple = ()

        for i in arg_word_counts:
            arg_polarity, arg_idx, awc = awc_tuple

            matched_w_c = comment_word_count & awc

            score = scoring_function(matched_w_c, comment_word_count, awc)

            # if max_score < score:
            #     max_score = score
            #     best_tuple = (arg_polarity, arg_idx, awc, matched_w_c, score)

        arg_polarity, arg_idx, awc, matched_w_c, score = best_tuple

        matched_to_arg[arg_polarity][arg_idx].append((comment_idx, score, comment_word_count, awc, matched_w_c))
        matched_to_comment[comment_word_count].append((arg_polarity, arg_idx, score, comment_word_count, awc, matched_w_c))

    return matched_to_arg, matched_to_comment
                
        
            #score1 = sum(matched_w_c.values()) / len(arg.split(" "))
            #score2 = sum(matched_w_c.values()) / len(words)

            #if maxScore1[0] < score1:
            #    maxScore1 = [score1, text, arg, matched_w_c]
            #if maxScore2[0] < score2:
            #    maxScore2 = [score2, text, arg, matched_w_c]

        #threshold = 0.5

        #if maxScore1[0] > threshold or maxScore2[0] > threshold:
        #    print("___")
        #     print(text)
        # if maxScore1[0] > threshold:
        #     print("Max Score 1:", maxScore1[0])
        #     print(maxScore1[2])
        #     print(maxScore1[3])

        # if maxScore2[0] > threshold:
        #     print("Max Score 2:", maxScore2[0])
        #     print(maxScore2[2])
        #     print(maxScore2[3])
