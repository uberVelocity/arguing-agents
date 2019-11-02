from reddit import Reddit
from procon import Procon

from comparison_methods import compare_word_counts, compare_only_noun_synsets, compare_noun_verb_synsets, dandelion

similarity_matrix_algorithms = {'words': compare_word_counts, 'noun_synsets': compare_only_noun_synsets, 'n_v_adj_adv_synsets': compare_noun_verb_synsets, 'dandelion': dandelion}

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

        self.similarity_matrices = {}

        for name, similarity_matrix_algorithm in similarity_matrix_algorithms.items():
            self.similarity_matrices[name] = similarity_matrix_algorithm.match([comment.text for comment in self.getAllComments()], self.getPros(), self.getCons())

        self.comment_rank_pros, self.comment_rank_cons = dandelion.match([comment.text for comment in self.getAllComments()], self.getPros(), self.getCons())
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