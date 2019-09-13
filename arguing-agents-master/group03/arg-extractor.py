import praw
from praw.models import MoreComments
from pass import PASS
# Initialize reddit instance
reddit = praw.Reddit(client_id='vsf_RaO1Y0ddLA',
                     client_secret='AKNm3rM3zJ6m6lWdxJwE6u6Z7qM',
                     password=PASS,
                     user_agent='argument-extracthor',
                     username='ubervelocity')

# Initialize subreddit 'changemyview' instance
change_my_view = reddit.subreddit('changemyview')

# Loop through all submissions and output in the following order:
# top-level comments, secondary-level comments, third-level comments etc.
for submission in reddit.subreddit('changemyview').hot(limit=10):
    for comment in submission.comments.list():
        if isinstance(comment, MoreComments):
            continue
        print(comment.body)