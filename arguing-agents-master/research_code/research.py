from topic import Topic

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


        