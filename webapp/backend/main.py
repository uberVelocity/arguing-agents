from research import Research
from sys import argv
import json

from submission import Submission
from comment import Comment

if len(argv) < 2 or len(argv) > 3:
    print("Usage: python3 main.py [json file]")
    exit(-1)


f = open(argv[1])
json_str = f.read()
settings = json.loads(json_str)
f.close()

research = Research(settings)

for i in range(len(research.topics)):
    print("___Topic", i, "___")
    print(research.topics[i].procon.background)
    topic = research.topics[i]
    for j in range(len(research.topics[i].reddit.submissions)):
        print("\t___Submission", j, "____")
        submission = topic.reddit.submissions[j]

        if len(submission.comments) == 0:
            continue

        comment = submission.comments[0]

        print(comment.author, comment.author_delta)

