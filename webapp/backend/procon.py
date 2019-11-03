import dryscrape
import re
import requests

from sys import argv

class Procon:
	def __init__(self, settings = {}):
		if settings == {}:
			print("Procon: __init__: No settings given. Creating empty object.")
			return

		if 'mode' not in settings:
			print("Procon: __init__: Mode not provided. Initializing it to 'find'.")
			settings['mode'] = 'find'
			
		mode = settings['mode']

		if mode == 'find':
			topic = settings['topic']
			self.find(topic)
			self.load()
		elif mode == 'url':
			self.background_url = settings['background_url']
			self.argument_url = settings['argument_url']
			self.load()
		elif mode == 'given':
			if 'background' in settings:
				self.background = settings['background']
			else:
				self.background = ''

			if 'pros' in settings:
				self.pros = settings['pros']
			else:
				self.pros = []

			if 'cons' in settings:
				self.cons = settings['cons']
			else:
				self.cons = []
		else:
			print("Procon: Unsupported mode!")
			exit(-1230)

	def to_dict(self):
		dic = {}
		dic['background'] = self.background
		dic['pros'] = self.pros
		dic['cons'] = self.cons
		return dic

	def from_dict(self, dic):
		self.background = dic['background']
		self.pros = dic['pros']
		self.cons = dic['cons']

	def load(self):
		self.background = self.retrieveBackground()
		self.pros = self.retrievePros()
		self.cons = self.retrieveCons()

	def find(self, string):
		url = "https://duckduckgo.com/?q=procon.org"

		for word in string.split(" "):
			url += "+" + word
		
		url += "&t=h_&ia=web"

		session = dryscrape.Session()
		session.visit(url)
		website_string = session.body()

		#search_results = re.findall('<a class="result__a" rel="noopener" href="(.*?)">', website_string, flags=re.DOTALL)
		search_results = re.findall(r'"([^"<>?]*?procon\.org[^ ]*?)"', website_string, flags=re.DOTALL)
		for s in search_results:
			print(s)
		
		base_url = search_results[0]
		if not base_url.startswith("https://"):
			base_url = "https://" + base_url
		# print("______\n", base_url, "\n_____")
		# exit(0)
		
		links = re.findall("<a.*?newblue-get-started-(.*?)'", requests.get(base_url).text)

		self.background_url = base_url

		if links != []:
			self.argument_url = base_url + links[1]
		else:
			self.argument_url = base_url

		
		
	def retrieveBackground(self):
		url = self.background_url
		web_page_string = requests.get(url).text
		backgrounds = re.findall('<div style="display:block;">(.*?)</div>', web_page_string, flags=re.DOTALL)

		if backgrounds == []:
			backgrounds = re.findall('<div class="entry-content">(.*?)<h3 class="top-pca">', web_page_string, flags = re.DOTALL)

		if backgrounds == []:
			background = ""
		else:
			background = backgrounds[0]
			
		return self.clean_str(background)

	def clean_str(self, string):
		cleaned_str = re.sub(r"<.*?>", " ", string)
		cleaned_str = re.sub(r"\[.*?\]", " ", cleaned_str)
		cleaned_str = re.sub(r"&.*?\;", " ", cleaned_str)
		cleaned_str = re.sub(r" +", " ", cleaned_str)
		cleaned_str = re.sub(r"\n+", "\n", cleaned_str)
		cleaned_str.strip()
		return cleaned_str
		

	def retrieveArguments(self, url, isPro):
		if isPro:
			arg_type = "pro"
		else:
			arg_type = "con"

		if 'answers' in url:
			regex = '<div class="newblue-' + arg_type + '-quote-box">(.*?)</div>\n<br />\n<br />\n</div><br />'
		elif 'resource' in url:
			regex = '<td id="newblue-' + arg_type + '.*?>\n<div class="newblue-top-' + arg_type + '-quote-box">(.*?)</td>'
		else:
			regex = '<blockquote .*?argument-type-' + arg_type + '.*?>.*?<h3>.*?</h3>(.*?)</blockquote>'

		web_page_string = requests.get(url).text
		arguments = re.findall(regex, web_page_string, flags=re.DOTALL)

		cleaned_arguments = []

		for arg in arguments:
			cleaned_arg = self.clean_str(arg)
			cleaned_arguments.append(cleaned_arg)

		return cleaned_arguments

	def retrievePros(self):
		return self.retrieveArguments(self.argument_url, True)

	def retrieveCons(self):
		return self.retrieveArguments(self.argument_url, False)

#pros = retrievePros(argv[1])

#for i in range(len(pros)):
	##print("___Pro Argument", i, "___\n", pros[i], "\n")

#cons = retrieveCons(argv[1])

#for i in range(len(cons)):
	#print("___Con Argument", i, "___\n", cons[i], "\n")

#bacs = retrieveBackground(argv[1])

#print(bacs)
#for i in range(len(bacs)):
#	#print("___Background", i, "___\n", bacs[i], "\n")


#pc = Procon({'mode': 'find', 'topic': argv[1]})

#for i in range(len(pc.pros)):
#	print("___Pro Argument", i, "___\n", pc.pros[i], "\n")

#for i in range(len(pc.cons)):
#	print("___Con Argument", i, "___\n", pc.cons[i], "\n")

#print(pc.background)
#print(pc.background_url)
#print(pc.argument_url)
#print(pc.pros)

#pc.find("medical marijuana")