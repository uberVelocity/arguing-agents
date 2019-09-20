from research import Research
from sys import argv
import json

if len(argv) < 2 or len(argv) > 3:
    print("Usage: python3 main.py [json file]")
    exit(-1)


f = open(argv[1])
json_str = f.read()
settings = json.loads(json_str)

research = Research(settings)
