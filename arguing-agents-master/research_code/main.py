import research
from sys import argv

if len(argv) < 2 or len(argv) > 3:
    print("Usage: python3 main.py [json file]")
    exit(-1)

research = Research(argv[1])
research.run()
