import requests
import atexit
import json

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

    #tokens = {'f96d3b84d2e541b1bc61ecfbefcf0fa5': 1, '12a4556df49845b6a6eb6cfe431c0789':1000, '08bc47bd7b824b8a8411bae30a82176a': 1000}

def match(comment_texts, pro_texts, con_texts):
    global tokens

    comment_rank_pro_args = []
    
    j = 0

    for pro_text in con_texts:
        score_comment_tuples = []

        for i in range(len(comment_texts)):
            comment_text = comment_texts[i]

            token = get_token()
            
            r = requests.post("https://api.dandelion.eu/datatxt/sim/v1/", data = {'text1': pro_text, 'text2': comment_text, 'lang': 'en', 'token': token})

            tokens[token] -= 3

            if 'error' in r.json():
                print('Error in Dandelion response.')
                print('Returned json:')
                print(r.json())

            score = r.json()['similarity']

            score_comment_tuples.append((score, i))

        comment_rank_pro_args.append(sorted(score_comment_tuples, key = lambda tup: tup[0], reverse = True))

        print(pro_text)

        for score, i in comment_rank_pro_args[j][:5]:
            print("______")
            print(score, comment_texts[i])

        j += 1
