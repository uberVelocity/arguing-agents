import requests
import atexit
import json
from nltk.tokenize import word_tokenize
import math

units_per_request = 3

with open("comparison_methods/dandelion.json") as dandelion_json_file:
    tokens = json.loads(dandelion_json_file.read())
    print(tokens)

@atexit.register
def write_tokens_to_disk():
    with open("comparison_methods/dandelion.json", "w") as dandelion_json_file:
        dandelion_json_file.write(json.dumps(tokens))

def get_token():
    print(tokens)
    for token, left_units in tokens.items():
        if left_units >= 3:
            return token
    
    print("Ran out of units")
    exit(-1)

def calculate_similarity_matrix(text_list_1, text_list_2):
    global tokens

    similarity_matrix = []

    for text_1 in text_list_1:
        score_comment_tuples = []

        for i in range(len(text_list_2)):
            text_2 = text_list_2[i]

            token = get_token()
            
            r = requests.post("https://api.dandelion.eu/datatxt/sim/v1/", data = {'text1': text_1, 'text2': text_2, 'lang': 'en', 'token': token})

            tokens[token] -= 3

            if 'error' in r.json():
                print('Error in Dandelion response.')
                print('Returned json:')
                print(r.json())
            

            score = r.json()['similarity']

            score_comment_tuples.append((score, i))

        similarity_matrix.append(score_comment_tuples.copy())  # sorted(score_comment_tuples, key = lambda tup: tup[0], reverse = True))

    return similarity_matrix

    #tokens = {'f96d3b84d2e541b1bc61ecfbefcf0fa5': 1, '12a4556df49845b6a6eb6cfe431c0789':1000, '08bc47bd7b824b8a8411bae30a82176a': 1000}


def match(comment_texts, pro_texts, con_texts):
    similarity_matrix_pro = calculate_similarity_matrix(pro_texts, comment_texts)
    similarity_matrix_con = calculate_similarity_matrix(con_texts, comment_texts)

    return similarity_matrix_pro, similarity_matrix_con