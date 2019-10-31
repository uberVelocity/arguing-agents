from reddit import Reddit
from procon import Procon

from comparison_methods import compare_only_noun_synsets

class Topic:
    def __init__(self, topic_settings):
        if 'topic-name' not in topic_settings:
            print("Topic: Provide a topic name")
            exit(-12312)
        
        self.topic_name = topic_settings['topic-name']

        if 'procon' not in topic_settings:
            print('Topic: Provide procon settings')
            exit(-124)

        procon_settings = topic_settings['procon']

        if 'reddit' not in topic_settings:
            print('Topic: Provide reddit settings')
            exit(-3324)

        reddit_settings = topic_settings['reddit']
        
        procon_settings['topic'] = self.topic_name
        reddit_settings['topic'] = self.topic_name

        self.procon = Procon(procon_settings)
        self.reddit = Reddit(reddit_settings)

        self.comment_rank_pros, self.comment_rank_cons = compare_only_noun_synsets.match(self.getPros(), self.getCons(), [comment.text for comment in self.getAllComments()])
        print(self.comment_rank_pros)
        print(self.comment_rank_cons)

    def getAllComments(self):
        return self.reddit.getAllComments()

    def getPros(self):
        return self.procon.pros

    def getCons(self):
        return self.procon.cons

#topic = Topic({'topic-name': 'medical marijuana', 'procon': {'mode': 'find'}, 'reddit': {'mode': 'find'}})
#print(topic.procon.background)