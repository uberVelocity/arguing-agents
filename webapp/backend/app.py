from __future__ import print_function
from flask_cors import CORS

import json
import sys

from flask import Flask
from flask import jsonify
from flask import request

import atexit

from research import Research
from topic import Topic

import re

f = open("settings.json")
json_str = f.read()
settings = json.loads(json_str)
f.close()

research = Research(settings)

app = Flask(__name__)
CORS(app)

counter = 0

def htmlify(string):
    return re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', string)

def htmlifyList(list_of_strings):
    return [htmlify(string) for string in list_of_strings]

@atexit.register
def save_research():
    print('Saving research...')
    research.save('research_autosave')

@app.route('/')
def hello():
    return 'Hello world!'

@app.route('/process', methods = ['POST'])
def processTopic():
    if request.method == 'POST':
        # Get topic from frontend
        request_json = request.get_json()

        print('the data:', request_json)
        # print('the topic:', data.topic, file = sys.stdout)

        if 'topic' not in request_json:
            print("App: processTopic: Invalid request. No topic specified. Received json:", request_json)

        topic_name = request_json['topic']

        topic = research.get_topic(topic_name)

        if topic == None:
            print("App: processTopic: Tried to parse an unknown topic", topic_name)
            print("\tCreating a new Topic to match request.")

            topic = Topic({'topic-name': topic_name})
            research.add_topic(topic)

        response_json = {'pros': [], 'cons': []}

        comment_rankings_text_pro = topic.get_comment_rankings_text('new', 'pro')

        for i in range(len(topic.get_pros())):
            pro_text = topic.get_pros()[i]
            comment_ranking = comment_rankings_text_pro[i]

            arg_element = {'arg_text': pro_text, 'best_comments': []}

            for j in range(3):
                comment_score, comment_text = comment_ranking[j]
                comment_element = {'score': comment_score, 'text': comment_text}
                arg_element['best_comments'].append(comment_element)

            response_json['pros'].append(arg_element.copy())

        for i in range(len(topic.get_cons())):
            con_text = topic.get_cons()[i]
            comment_ranking = comment_rankings_text_con[i]

            arg_element = {'arg_text': con_text, 'best_comments': []}

            for j in range(3):
                comment_score, comment_text = comment_ranking[j]
                comment_element = {'score': comment_score, 'text': comment_text}
                arg_element['best_comments'].append(comment_element)

            response_json['cons'].append(arg_element.copy())

        return jsonify(response_json)

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