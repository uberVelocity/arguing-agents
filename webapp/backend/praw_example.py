import praw

from praw.models import MoreComments

class Submission:
    def __init__(self, title, comments = []):
        self.title = title
        self.comments = comments
    
    def addComment(self, comment):
        self.comments.append(comment)

class Comment:
    def __init__(self, body, depth, author, author_delta):
        self.body = body
        self.depth = depth
        self.author = author
        self.author_delta = author_delta

def parseDeltaFlair(flair):
    if flair == None or flair == '∞∆':
        return 0
    return int(flair[:-1])

def retrieveComments(submission, praw_comment_forest, depth = 0):
    for praw_comment in list(praw_comment_forest):
        if isinstance(praw_comment, MoreComments):
            continue
        comment = Comment(praw_comment.body, depth, praw_comment.author, parseDeltaFlair(praw_comment.author_flair_text))
        submission.addComment(comment)

        retrieveComments(submission, praw_comment.replies, depth + 1)

def parseSubmission(praw_submission):
    submission = Submission(praw_submission.title)
    retrieveComments(submission, praw_submission.comments)
    return submission

reddit = praw.Reddit(client_id='Vyw-20ZFtH4msA',
                    client_secret='-vZkEG8s6qlRvbTcuGxmJOnpAds',
                    user_agent='ubuntu:arguing-agents:v1 (by /u/HolzmindenScherfede)'
                    )

for subm in reddit.subreddit('ChangeMyView').hot(limit=10):
    submission = parseSubmission(subm)
    print(submission.title)
    for comment in submission.comments:
        print(comment.author, comment.depth, comment.author_delta)
    
exit(0)
subm = list(reddit.subreddit('ChangeMyView').hot(limit=1))[0]
print(subm.title)
for c in list(subm.comments):
    print(c.author_flair_text)
#    for nc in c.replies:
#        print(nc.author)

submission = parseSubmission(subm)
print(submission.comments)
for comment in submission.comments:
    print(comment.author, comment.depth, comment.author_delta)