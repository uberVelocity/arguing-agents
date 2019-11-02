from reddit import Reddit
from procon import Procon

from comparison_methods import compare_word_counts, compare_only_noun_synsets, compare_noun_verb_synsets, dandelion, new

similarity_matrix_algorithms = {'words': compare_word_counts, 'noun_synsets': compare_only_noun_synsets, 'n_v_adj_adv_synsets': compare_noun_verb_synsets, 'new': new}  # 'dandelion': dandelion, 'new': new}

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

        # self.comment_rank_pros, self.comment_rank_cons = dandelion.match([comment.text for comment in self.getAllComments()], self.getPros(), self.getCons())
        # print(self.comment_rank_pros)
        # print(self.comment_rank_cons)

    def getSimilarityMatrices(self, similarity_matrix_algorithm):
        similarity_matrix_pro, similarity_matrix_con = self.similarity_matrices[similarity_matrix_algorithm]
        return similarity_matrix_pro, similarity_matrix_con

    def getSimilarityMatrix(self, similarity_matrix_algorithm, polarity):
        similarity_matrix_pro, similarity_matrix_con = self.getSimilarityMatrices(similarity_matrix_algorithm)

        if polarity == 'pro':
            return similarity_matrix_pro
        elif polarity == 'con':
            return similarity_matrix_con
        else:
            print("Topic: getSimilarityMatrix: Unknown polarity:", polarity)

    def getCommentRankings(self, similarity_matrix_algorithm, polarity):
        similarity_matrix = self.getSimilarityMatrix(similarity_matrix_algorithm, polarity)

        comment_rankings = []
        
        for similarity_vector_argument in similarity_matrix:
            comment_rankings.append(sorted(similarity_vector_argument, key = lambda tup: tup[0], reverse = True))

        return comment_rankings

    def transpose(self, matrix):
        transposed_matrix = [[] for _ in matrix[0]]

        for vector in matrix:
            for i in range(len(vector)):
                transposed_matrix[i].append(vector[i])

        return transposed_matrix

    def get_data_points_comment_score_author_delta(self, similarity_matrix_algorithm, aggregation = 'max'):
        data_points = {}

        similarity_matrix_pro, similarity_matrix_con = self.getSimilarityMatrices(similarity_matrix_algorithm)

        combined_matrix = similarity_matrix_pro + similarity_matrix_con

        transposed_combined_matrix = self.transpose(combined_matrix)

        for i in range(len(transposed_combined_matrix)):
            similarity_vector_comment = transposed_combined_matrix[i]
            scores = [score for score, idx in similarity_vector_comment]
            
            if aggregation == 'max':
                comment_score = max(scores)
            else:
                print("Topic: Get_data_points_comment_score_author_delta:", aggregation)
                exit(0)

            deltas_author = self.getAllComments()[i].author_delta

            if deltas_author not in data_points:
                data_points[deltas_author] = []

            data_points[deltas_author].append(comment_score)

            



    def getAllComments(self):
        return self.reddit.getAllComments()

    def getPros(self):
        return self.procon.pros

    def getCons(self):
        return self.procon.cons

#topic = Topic({'topic-name': 'medical marijuana', 'procon': {'mode': 'find'}, 'reddit': {'mode': 'find'}})
#print(topic.procon.background)