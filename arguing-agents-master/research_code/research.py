import json

class Research:
    def __init__(self, json_file):
        f = open(json_file)
        json_str = f.read()
        settings = json.loads(json_str)

        load_comments()

    def load_comments():
        self.comments = []

        if self.mode == "search":