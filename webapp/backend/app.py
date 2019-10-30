from __future__ import print_function
from flask_cors import CORS

import json
import sys

from flask import Flask
from flask import jsonify
from flask import request

from research import Research

f = open("settings.json")
json_str = f.read()
settings = json.loads(json_str)
f.close()

research = Research(settings)

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return 'Hello world!'

@app.route('/process', methods = ['POST'])
def processTopic():
    if request.method == 'POST':
        # Get topic from frontend
        data = request.get_json()

        print('the data:', data)
        # print('the topic:', data.topic, file = sys.stdout)
        
        settings = {}
        settings["topics"] = [{
            "topic-name": data["topic"].lower(),
            "procon": {
                "mode": "find"
            },
            "reddit": {
                "mode": "find"
            }
        }]

        #research = Research(settings)
        # TODO: Compile Procon List of topic

        # TODO: Compile Reddit List of topic



        # TODO: Run the script of the program

        # TODO: Compile JSON object with: pro{procon, reddit}, con{procon, reddit}
        topic = None
        for t in research.topics:
            if t.topic_name == data["topic"]:
                topic = t
                break

        if topic == None:
            print("Tried to parse an unknown topic", data["topic"])

        pProcon = topic.getPros()#'proListProcon'
        cProcon = topic.getCons()#'conListProcon'
        pReddit = [comment.text for comment in topic.getAllComments()][0:2:]#'proListReddit'
        cReddit = [comment.text for comment in topic.getAllComments()][1:2:]#'conListReddit'
        
        # pProcon = research.topics[0].getPros()#'proListProcon'
        # cProcon = research.topics[0].getCons()#'conListProcon'
        # pReddit = [comment.text for comment in research.topics[0].getAllComments()][0:2:]#'proListReddit'
        # cReddit = [comment.text for comment in research.topics[0].getAllComments()][1:2:]#'conListReddit'

        response = {
            'prosProcon': pProcon,
            'consProcon': cProcon,
            'prosReddit': pReddit,
            'consReddit': cReddit
        }

        return jsonify(response)