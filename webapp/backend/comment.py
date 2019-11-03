import praw
import re

class Comment:
    def __init__(self, praw_comment = None, depth = 0):
        if praw_comment == None:
            print("Comment: __init__: No praw comment given. Creating empty object.")
            return

        self.src = praw_comment

        self.text = praw_comment.body
        self.depth = depth
        self.author = praw_comment.author
        print(self.author, praw_comment.author_flair_text)
        self.author_delta = self.parseDeltaFlair(praw_comment.author_flair_text)

    def to_dict(self):
        dic = {}

        dic['src'] = self.src.id
        dic['text'] = self.text
        dic['depth'] = self.text

        if self.author == None:
            dic['author'] = ''
        else:
            dic['author'] = self.author.name

        dic['author_delta'] = self.author_delta

        return dic

    def from_dict(self, dic, reddit):
        self.src = praw.models.Comment(reddit, id = dic['src'])
        self.text = dic['text']
        self.depth = dic['depth']

        if dic['author'] == '':
            self.author = None
        else:
            self.author = praw.models.Redditor(reddit, dic['author'])

        self.author_delta = dic['author_delta']
        
        
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