from reddit import Reddit
from procon import Procon

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

#topic = Topic({'topic-name': 'medical marijuana', 'procon': {'mode': 'find'}, 'reddit': {'mode': 'find'}})
#print(topic.procon.background)