import re
import requests

from sys import argv

def retrieveArguments(url, isPro):
    if isPro:
        arg_type = "pro"
    else:
        arg_type = "con"

    if 'answers' in url:
        regex = '<div class="newblue-' + arg_type + '-quote-box">(.*?)</div>\n<br />\n<br />\n</div><br />'
    elif 'resource' in url:
        regex = '<td id="newblue-' + arg_type + '.*?>\n<div class="newblue-top-' + arg_type + '-quote-box">(.*?)</td>'
    else:
        regex = '<blockquote .*?argument-type-' + arg_type + '.*?>(.*?)</blockquote>'

    web_page_string = requests.get(url).text
    arguments = re.findall(regex, web_page_string, flags=re.DOTALL)

    return arguments

def retrievePros(url):
    return retrieveArguments(url, True)

def retrieveCons(url):
    return retrieveArguments(url, False)

pros = retrievePros(argv[1])

for i in range(len(pros)):
    print("___Pro Argument", i, "___\n", pros[i], "\n")

cons = retrieveCons(argv[1])

for i in range(len(cons)):
    print("___Con Argument", i, "___\n", cons[i], "\n")