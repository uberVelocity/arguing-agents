import re

class Comment:
    def __init__(self, praw_comment, depth):
        self.src = praw_comment

        self.text = praw_comment.body
        self.depth = depth
        self.author = praw_comment.author
        print(self.author, praw_comment.author_flair_text)
        self.author_delta = self.parseDeltaFlair(praw_comment.author_flair_text)
        
        
    """ def __init__(self, body, depth, author, author_delta):
        self.body = body
        self.depth = depth
        self.author = author
        self.author_delta = author_delta """

    def parseDeltaFlair(self, author_flair_text):
        if author_flair_text == None or author_flair_text == '∞∆':
            return 0

        delta = re.findall(r'(\d+?)∆', author_flair_text)

        print(delta)

        if delta == []:
            return 0
        
        return int(delta[0])