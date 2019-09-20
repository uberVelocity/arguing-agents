import praw

class Reddit:
    def __init__(self, reddit_settings):
        if 'mode' not in reddit_settings:
            print("Reddit: provide mode")
            exit(-1002)
        
        mode = reddit_settings['mode']

        self.reddit = praw.Reddit(client_id='Vyw-20ZFtH4msA',
                    client_secret='-vZkEG8s6qlRvbTcuGxmJOnpAds',
                    user_agent='ubuntu:arguing-agents:v1 (by /u/HolzmindenScherfede)'
                    )
        
        if mode == 'find':
            if 'topic' in reddit_settings:
                topic = reddit_settings['topic']
            else:
                print("Reddit: provide topic")
                exit(-1003)

            if 'amount' in reddit_settings:   
                amount = reddit_settings['amount']
            else:
                amount = 10

            if 'sortby' in reddit_settings:
                sortby = reddit_settings['sortby']
            else:
                sortby = 'hot'

            self.submissions = list(self.reddit.subreddit('ChangeMyView').search(topic, sortby))[:amount]

reddit = Reddit({'mode': 'find', 'topic': 'gun control', 'amount': 100, 'sortby': 'new'})

for s in reddit.submissions:
    print(s.title)

            
