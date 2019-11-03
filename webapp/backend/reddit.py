import praw
from submission import Submission

class Reddit:
    def __init__(self, reddit_settings):
        if 'mode' not in reddit_settings:
            print("Reddit: __init__: Mode not provided. Initializing it to 'find'.")
        
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
                amount = 2

            if 'sortby' in reddit_settings:
                sortby = reddit_settings['sortby']
            else:
                sortby = 'hot'

            praw_submissions = list(self.reddit.subreddit('ChangeMyView').search(topic, sortby))[:amount]

            self.submissions = []

            for praw_submission in praw_submissions:
                submission = Submission(praw_submission)
                self.submissions.append(submission)
        elif mode == 'url':
            if 'submission_urls' not in reddit_settings:
                print('Reddit: provide submission_urls!')
                exit(-12031)
            
            submission_urls = reddit_settings['submission_urls']

            self.submissions = [] 

            for submission_url in submission_urls:
                submission = Submission(praw.models.Submission(self.reddit, url=submission_url))
                self.submissions.append(submission)

    def to_dict(self):
        dic = {}
        dic['submissions'] = []
        for submission in self.submissions:
            dic['submissions'].append(submission.to_dict())
        return dic
            
    def getAllComments(self):
        return [comment for submission in self.submissions for comment in submission.comments]