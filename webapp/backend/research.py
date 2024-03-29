from topic import Topic

from comparison_methods import compare_noun_synsets

import re
import operator
import json

class Research:
    def __init__(self, research_settings = {}):
        if research_settings == {}:
            print("Research: __init__: No settings given. Creating empty object.")
            return

        if 'topics' not in research_settings:
            print("Research: provide topics")
            exit(-1234234)

        topics = research_settings['topics']

        self.topics = []

        for topic_settings in topics:
            topic = Topic(topic_settings)
            self.topics.append(topic)
        
        self.counter = 0
        

        # for topic in self.topics:
        #     print(compare_noun_synsets.match(topic.getAllComments(), topic.getPros(), topic.getCons()))

        #exit(0)
                        
        #f = open("tsv_file.tsv", "w")
        #f.write(self.getTSV())
        #f.close()

    def to_dict(self):
        dic = {}
        dic['topics'] = []
        for topic in self.topics:
            dic['topics'].append(topic.to_dict())
        return dic

    def save(self, file_name):
        dic = self.to_dict()
        
        with open(file_name, 'w') as f:
            f.write(json.dumps(dic))

    def from_dict(self, dic):
        if 'topics' not in dic:
            print("Research: from_dict: 'topics' not in dic. Dic:", dic)
            exit(-1)

        self.topics = []

        for dic_topic in dic['topics']:
            topic = Topic()
            topic.from_dict(dic_topic)
            self.topics.append(topic)

    def load(self, file_name):
        with open(file_name, "r") as f:
            dic = json.loads(f.read())
        
        self.from_dict(dic)

    def get_topic(self, topic_name):
        for topic in self.topics:
            if topic.topic_name == topic_name:
                return topic

        print("App: processTopic: Tried to parse an unknown topic", topic_name)
        print("\tCreating a new Topic to match request.")

        topic = Topic({'topic-name': topic_name})
        self.add_topic(topic)  

        return topic

    def add_topic(self, topic):
        for topic_ in self.topics:
            if topic.topic_name == topic_.topic_name:
                print("Research: add_topic: Topic name already exists:", topic_.topic_name)
        self.topics.append(topic)       
        
    def getTSV(self):
        tsv_string = ""

        for topic in self.topics:
            topic_name = topic.topic_name

            for submission in topic.reddit.submissions:
                for comment in submission.comments:
                    text = comment.text
                    text = text.replace("\t", " ").replace("\n", " ")
                    
                    m = re.split(r'([\.\?\!]) \s*(?![^()]*\))', text)

                    print(m)

                    for i in range(len(m))[::2]:
                        sentence = m[i]

                        if i + 1 < len(m):
                            sentence += m[i + 1]

                        sentence = sentence.strip()

                        if sentence == "":
                            continue

                        tsv_string += topic_name + "\t\t\t\t" + sentence + "\tNoArgument\ttest\n"

        return tsv_string



          