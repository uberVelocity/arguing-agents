from __future__ import print_function
from flask_cors import CORS

import json
import sys

from flask import Flask
from flask import jsonify
from flask import request

import atexit

from operator import itemgetter

from research import Research
from topic import Topic

import re

f = open("settings.json")
json_str = f.read()
settings = json.loads(json_str)
f.close()

try:
    research = Research()
    research.load('research_autosave')
except:
    research = Research(settings)

# research = Research()
# research.load('research_autosave')

app = Flask(__name__)
CORS(app)

counter = 0

def htmlify(string):
    return re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', string)

def htmlifyList(list_of_strings):
    return [htmlify(string) for string in list_of_strings]

def parse_request(request):
    request_dict = request.get_json()

    if 'topic_name' not in request_dict:
        print("App: get_data_for_graph: Invalid request. No topic name specified. Received json:", request_dict)

    if 'similarity_measure' not in request_dict:
        print("App: get_data_for_graph: Invalid request. No similarity measure specified. Received json:", request_dict)

    topic_name = request_dict['topic_name']
    similarity_measure = request_dict['similarity_measure']

    return topic_name, similarity_measure

@atexit.register
def save_research():
    print("Autosaving disabled.")
    # print('Saving research...')
    # research.save('research_autosave')

@app.route('/')
def hello():
    return 'Hello world!'

@app.route('/graph', methods = ['POST'])
def get_data_for_graph():
    if request.method != 'POST':
        return

    topic_name, similarity_measure = parse_request(request)

    topic = research.get_topic(topic_name)

    data_points = topic.get_data_points_comment_score_author_delta(similarity_measure)

    response_dict = {'data_points': data_points}

    return jsonify(response_dict)

def get_argument_elements(argument_texts, argument_comment_rankings, n_top_comments = 3):
    argument_elements = []

    if len(argument_texts) != len(argument_comment_rankings):
        print("App: get_argument_elements: Amount of arguments are not the same!")
        print("\tlen(argument_texts):", len(argument_texts))
        print("\tlen(argument_comment_rankings):", len(argument_comment_rankings))

    for i in range(len(argument_texts)):
        argument_text = argument_texts[i]
        comment_ranking = argument_comment_rankings[i]

        print("App: get_argument_elements: Debug")
        print("\tcomment_ranking:", comment_ranking)

        arg_element = {'arg_text': argument_text, 'best_comments': []}

        for j in range(n_top_comments):
            comment_score, comment_text = comment_ranking[j]
            comment_element = {'score': comment_score, 'text': comment_text}
            arg_element['best_comments'].append(comment_element)

        argument_elements.append(arg_element.copy())

    return argument_elements

@app.route('/process', methods = ['POST'])
def processTopic():
    if request.method != 'POST':
        return

    topic_name, similarity_measure = parse_request(request)

    topic = research.get_topic(topic_name)

    response_json = {'pros': [], 'cons': []}

    pro_texts = topic.get_pros()
    comment_rankings_text_pro = topic.get_comment_rankings_text(similarity_measure, 'pro')

    con_texts = topic.get_cons()
    comment_rankings_text_con = topic.get_comment_rankings_text(similarity_measure, 'con')

    response_json['pros'] = get_argument_elements(pro_texts, comment_rankings_text_pro)
    response_json['cons'] = get_argument_elements(con_texts, comment_rankings_text_con)

    return jsonify(response_json)

@app.route('/best_comments', methods = ['POST'])
def get_best_comments():
    if request.method != 'POST':
        return

    topic_name, similarity_measure = parse_request(request)

    topic = research.get_topic(topic_name)

    aggregated_comment_scores = topic.get_aggregated_scores_comments(similarity_measure)

    sorted_aggregated_comment_scores = sorted(aggregated_comment_scores, key = itemgetter(0), reverse = True)

    response_dict = {}

    response_dict['comment_ranking'] = sorted_aggregated_comment_scores

    return jsonify(response_dict)
    
        # settings = {}
        # settings["topics"] = [{
        #     "topic-name": data["topic"].lower(),
        #     "procon": {
        #         "mode": "find"
        #     },
        #     "reddit": {
        #         "mode": "find"
        #     }
        # }]

        #research = Research(settings)
        # TODO: Compile Procon List of topic

        # TODO: Compile Reddit List of topic



        # TODO: Run the script of the program

        # TODO: Compile JSON object with: pro{procon, reddit}, con{procon, reddit}
        # topic = None
        # for t in research.topics:
        #     if t.topic_name == data["topic"]:
        #         topic = t
        #         break

        # print(t.topic_name)
        # print(topic.topic_name)

        # if topic == None:
        #     print("Tried to parse an unknown topic", data["topic"])

        # pProcon = topic.getPros()#'proListProcon'
        # cProcon = topic.getCons()#'conListProcon'
        # pReddit = [str(score) + " " + topic.getAllComments()[i].text for score, i in topic.getCommentRankings('words', 'pro')[0]][:4]  # [comment.text for comment in topic.getAllComments()][0::2]#'proListReddit'
        # cReddit = [str(score) + " " + topic.getAllComments()[i].text for score, i in topic.getCommentRankings('words', 'con')[0]][:4]  # [comment.text for comment in topic.getAllComments()][1::2]#'conListReddit'

        # for comment in topic.getAllComments()[0:10]:
        #     print(comment.text.replace('\n', ' ').replace('\t', ' ')[:30])
        
        # print("\n")

        # for comment in topic.getCons()[0:10]:
        #     print(comment.replace('\n', ' ').replace('\t', ' ')[:30])
            
        # # pProcon = research.topics[0].getPros()#'proListProcon'
        # # cProcon = research.topics[0].getCons()#'conListProcon'
        # # pReddit = [comment.text for comment in research.topics[0].getAllComments()][0:2:]#'proListReddit'
        # # cReddit = [comment.text for comment in research.topics[0].getAllComments()][1:2:]#'conListReddit'

        # response = {
        #     'prosProcon': pProcon[:10],
        #     'consProcon': cProcon[:10],
        #     'prosReddit': pReddit[:10],
        #     'consReddit': cReddit[:10]
        # }

        # research.counter += 1
        # print('returning ya boi ', research.counter)

        # return jsonify(response)