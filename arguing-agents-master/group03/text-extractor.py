import re
import urllib.request
from bs4 import BeautifulSoup
    
html = urllib.request.urlopen('https://gun-control.procon.org/')
soup = BeautifulSoup(html)
data = soup.findAll(text=True)
    
def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True
    
result = filter(visible, data)
    
print list(result)