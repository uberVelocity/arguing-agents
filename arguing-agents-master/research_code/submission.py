class Submission:
    def __init__(self, title, comments = []):
        self.title = title
        self.comments = comments
    
    def addComment(self, comment):
        self.comments.append(comment)