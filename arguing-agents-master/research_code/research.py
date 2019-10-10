from topic import Topic

import re
from collections import Counter

class Research:
    def __init__(self, research_settings):
        if 'topics' not in research_settings:
            print("Research: provide topics")
            exit(-1234234)

        topics = research_settings['topics']

        self.topics = []

        for topic_settings in topics:
            topic = Topic(topic_settings)
            self.topics.append(topic)

        self.compareWordCounts()
            
        #f = open("tsv_file.tsv", "w")
        #f.write(self.getTSV())
        #f.close()
        
        
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

    def compareWordCounts(self):
        for topic in self.topics:
            arg_word_counts = {}
            i = 0
            for arg in topic.procon.pros + topic.procon.cons:
                print(i)
                i += 1
                print(arg)
                arg_word_counts[arg] = Counter(arg.split(" "))

            for submission in topic.reddit.submissions:
                for comment in submission.comments:
                    text = comment.text
                    text = text.replace("\t", " ").replace("\n", " ")
                    
                    m = re.split(r'[\.\?\!] \s*(?![^()]*\))', text)
                    
                    #print(m)

                    words = []

                    for sentence in m:
                        words += sentence.split(" ")

                    comment_word_count = Counter(words)

                    #print(text)

                    #i = 0
                    #for arg in topic.procon.pros + topic.procon.cons:
                    #    #print(i)
                    #    i += 1
                    #    #print(arg)

                    #i = 0
                    maxScore1 = [0, "", "", ""]
                    maxScore2 = [0, "", "", ""]
                    for arg, awc in arg_word_counts.items():
                        #print(i)
                        #i += 1
                        matched_w_c = comment_word_count & awc
                        #print(matched_w_c)
                        score1 = sum(matched_w_c.values()) / len(arg.split(" "))
                        score2 = sum(matched_w_c.values()) / len(words)

                        #print(score1, score2)
                        if maxScore1[0] < score1:
                            maxScore1 = [score1, text, arg, matched_w_c]
                        if maxScore2[0] < score2:
                            maxScore2 = [score2, text, arg, matched_w_c]

                    threshold = 0.5

                    if maxScore1[0] > threshold or maxScore2[0] > threshold:
                        print("___")
                        print(text)
                    if maxScore1[0] > threshold:
                        print("Max Score 1:", maxScore1[0])
                        print(maxScore1[2])
                        print(maxScore1[3])

                    if maxScore2[0] > threshold:
                        print("Max Score 2:", maxScore2[0])
                        print(maxScore2[2])
                        print(maxScore2[3])

                        


          