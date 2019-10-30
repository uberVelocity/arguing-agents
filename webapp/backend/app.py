from __future__ import print_function
from flask_cors import CORS

import json
import sys

from flask import Flask
from flask import jsonify
from flask import request

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

        # TODO: Compile Procon List of topic

        # TODO: Compile Reddit List of topic



        # TODO: Run the script of the program

        # TODO: Compile JSON object with: pro{procon, reddit}, con{procon, reddit}
        
        pProcon = 'proListProcon'
        cProcon = 'conListProcon'
        pReddit = 'proListReddit'
        cReddit = 'conListReddit'

        response = {
            'prosProcon': pProcon,
            'consProcon': cProcon,
            'prosReddit': pReddit,
            'consReddit': cReddit
        }

        return jsonify(response)