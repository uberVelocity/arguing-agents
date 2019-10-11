from topic import Topic

import re
from collections import Counter
from nltk.corpus import wordnet as wn
from nltk.corpus.reader import NOUN

import operator

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

    def compareWordCounts2(self):
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

    def prepareText(self, text):
        text = text.replace("\t", " ").replace("\n", " ")
        text = re.sub(r' +', ' ', text)
        text = text.strip(' ')

        return text

    def getSentences(self, text):
        sentences = []

        parts = re.split(r'([\.\?\!]) \s*(?![^()]*\))', text)

        for i in range(len(parts))[::2]:
            sentence = parts[i]

            if i + 1 < len(parts):
                sentence += parts[i + 1]

            sentence = sentence.strip()

            if sentence == "":
                continue

        return sentences

#    def getDataPoints(self):
#        for topic in self.topics:
#            arg_data_points = {}
#            for arg in topic.procon.pros + topic.procon.cons:
#                arg_words = 

    def getWords(self, text):
        text = self.prepareText(text)
        return [word.strip(' ,.-!') for word in text.split(' ')]

    def getSynsets(self, text):
        text = self.prepareText(text)
        words = self.getWords(text)

        synsets = []

        for word in words:
            #print(word)
            word_synsets = wn.synsets(word, NOUN)

            if word_synsets == []:
                morpied_word = wn.morphy(word, NOUN)

                while morpied_word != None:
                    word_synsets += wn.synsets(morphied_word, NOUN)
                    morphied_word = wn.morphy(word, NOUN)

            synsets += word_synsets

        return synsets

    def matchCommentToArgument(self, comment_text, argument_counts):
        comment_synsets = self.getSynsets(comment_text)
        c_synset_counts = Counter(comment_synsets)

        selected_comment_idx = 0
        selected_comment_score = 0
        for i in range(len(argument_counts)):
            a_c = argument_counts[i]

            shared_synset_counts = a_c & c_synset_counts
            score = sum(shared_synset_counts.values()) / max(sum(a_c.values()), sum(c_synset_counts.values()))

            if score > selected_comment_score:
                selected_comment_idx = i
                selected_comment_score = score

        return selected_comment_idx, score, shared_synset_counts

    def matchCommentsAndArguments(self, argument_texts, comment_texts):
        matches = []

        argument_synset_counts = {}

        for argument in argument_texts:
            argument_synset_counts[argument] = Counter(self.getSynsets(argument))

        for comment in comment_texts:
            matched_argument_idx, score, shared_synset_counts = self.matchCommentToArgument(comment, list(argument_synset_counts.values()))
            matched_argument = list(argument_synset_counts.keys())[matched_argument_idx]

            #print("_")
            #print(comment)
            #print(matched_argument)

            matches.append((comment, matched_argument, score, shared_synset_counts))
        
        return matches

    def compareWordCounts(self):
        for topic in self.topics:
            argument_texts = topic.procon.pros + topic.procon.cons

            all_comments = []

            for submission in topic.reddit.submissions:
                all_comments += [comment for comment in submission.comments]

            comment_texts = [comment.text for comment in all_comments]
            print(comment_texts)

            matches = self.matchCommentsAndArguments(argument_texts, comment_texts)

            matches.sort(key = operator.itemgetter(2))

            for comment, argument, score, shared_synset_counts in matches:
                print("_")
                print(comment)
                print(argument)
                print("Score:", score)
                print(shared_synset_counts)
                print("\n")
            
    
    def compareWordCounts3(self):
        for topic in self.topics:
            arg_word_counts = {}
            for arg in topic.procon.pros + topic.procon.cons:
                arg_word_counts[arg] = Counter(arg.split(" "))

            for submission in topic.reddit.submissions:
                for comment in submission.comments:
                    text = comment.text
                    text = text.replace("\t", " ").replace("\n", " ")
                    text = re.sub(r' +', ' ', text)
                    text = text.strip()
                    
                    m = re.split(r'[\.\?\!] \s*(?![^()]*\))', text)
                    
                    meanings = []

                    for sentence in m:
                        words = sentence.split(" ")
                        for word in words:
                            print(word)
                            synsets = wn.synsets(word, NOUN)
                            #print(synsets)
                            if synsets == []:
                                word = wn.morphy(word, NOUN)
                                #print(word)
                                if word:
                                    synsets = wn.synsets(word, NOUN)
                            for synset in synsets:
                                print(synset.name())
                                meanings.append(synset.name())

                    comment_word_count = Counter(words)

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


          