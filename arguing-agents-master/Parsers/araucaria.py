# This is being reworked into something else.
# Starting from scratch I guess...
# Also this implementation is going to work using spacy instead

import os, json
import pandas as pd # tentative, may use may not

class DataSet():
	'''
	Reads a dataset into a series of sentences, these don't have labels yet
	'''
	def __init__(self):
		self.data = []


	def fromTSV(self):
		