import re
import requests
import csv
import pandas as pd 

from sys import argv
from nltk.tokenize import word_tokenize


import re
alphabets= "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"

def split_into_sentences(text):
	text = " " + text + "  "
	text = text.replace("\n"," ")
	text = re.sub(prefixes,"\\1<prd>",text)
	text = re.sub(websites,"<prd>\\1",text)
	if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
	text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
	text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
	text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
	text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
	text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
	text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
	text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
	if "”" in text: text = text.replace(".”","”.")
	if "\"" in text: text = text.replace(".\"","\".")
	if "!" in text: text = text.replace("!\"","\"!")
	if "?" in text: text = text.replace("?\"","\"?")
	text = text.replace(".",".<stop>")
	text = text.replace("?","?<stop>")
	text = text.replace("!","!<stop>")
	text = text.replace("<prd>",".")
	sentences = text.split("<stop>")
	sentences = sentences[:-1]
	sentences = [s.strip() for s in sentences]
	return sentences

def makeList (arguments): 
	outList =[]
	header3 = False 
	header4 = False 
	flag = False  
	
	for i in range(len(arguments)):
		token = word_tokenize(arguments[i])
		
		sentenceHeader3 = ''
		sentenceHeader4 = ''
		text = ''
		
		for word in token:  
			if (word == '<'): 
				flag = True

			
			if (flag and word == 'h3'):
				header3 = True 
			if (flag and word == '/h3'): 
				header3 = False 
				
			if (flag and word == 'h4'):
				header4 = True 
			if (flag and word == '/h4'): 
				header4 = False 
					
			
			
			if (header3 and not flag): 
				sentenceHeader3 +=word+' '
			if (header4 and not flag): 
				sentenceHeader4 += word+' '
			if (not header3 and not header4 and not flag): 
				text += word+' '
			
			if(word =='>'): 
				flag = False 

		#print(sentenceHeader3)
		#print('______') 
		#print (split_into_sentences(sentenceHeader4))
		#print('#########')
		#print(split_into_sentences(text))
		outList.append(sentenceHeader4+text)
		
	return outList 
	
	

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
proList = makeList(pros)
print(proList[0])

cons = retrieveCons(argv[1])
conList = makeList(cons)
print(conList[0])
