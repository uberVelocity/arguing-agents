import praw
from comment import Comment

class Submission:
    def __init__(self, praw_submission):
        self.src = praw_submission
        
        print("-", praw_submission.title)
        self.retrieveComments()

    def retrieveComments(self):
        self.comments = []
        self.retrieveCommentsHelper(self.src.comments)

    def retrieveCommentsHelper(self, praw_comment_forest, depth = 0):
        for praw_comment in list(praw_comment_forest):
            if isinstance(praw_comment, praw.models.MoreComments):
                continue

            comment = Comment(praw_comment, depth)
            self.addComment(comment)

            self.retrieveCommentsHelper(praw_comment.replies, depth + 1)

    def addComment(self, comment):
        self.comments.append(comment)


    """ 
    def __init__(self, title, comments = []):
        self.title = title
        self.comments = comments

    def addComment(self, comment):
        self.comments.append(comment)
     """