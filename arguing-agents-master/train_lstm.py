# Arguing agents start again
import pandas as pd
import numpy as np
#import seaborn as sns # unused, consider removing
#import matplotlib.pyplot as plt # unused, consider removing
import os,csv, time
import spacy # has pos tagger, word vector stuff and a bunch of other tools, very fast as well
from keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
import json
from tqdm import tqdm
# a debugging import
#from pprint import pprint

top_path = 'Corpora/complete/'
path_to_data = os.getcwd() + '/' + top_path

global_timer = time.time()

files = os.listdir(path_to_data)
files = list(filter(lambda k: '.tsv' in k,files)) # keep only tsv files
#files = files[:1] # only the first file so that tests don't take hours

temp_frames = []
df = pd.DataFrame()
for file in files:
	print("Reading {}".format(file))
	temp_df = pd.read_csv(path_to_data+file,delimiter='	',quoting=csv.QUOTE_NONE) # using tab delimiter (it may look like a space, but its a tab (probably))
	# note on the 'quoting=csv.QUOTE_NONE': its there because in one of the files (school_uniforms.tsv) there's at least one entry that looks to the parser like an end of file character inside a string
	temp_frames.append(temp_df)

df = pd.concat(temp_frames,ignore_index=True)

# adding simpler labels
def labeling(row):
	if row['annotation'] == 'NoArgument':
		return 0
	elif row['annotation'] in ['Argument_against','Argument_for']:
		return 1
# apply labels
df['label'] = df.apply(lambda row: labeling(row),axis=1)

### Once we have the data, time to initialize the spacy parser
l_model = 'en_core_web_lg'
print("Loading model {}".format(l_model))
start_time = time.time()
nlp = spacy.load(l_model) # this is the large sized model that also supports word vectors (for some reason loads faster than medium size model)
print("Done. Loading took {} seconds".format((time.time()-start_time)))


vectors = []
raw_sentences = df['sentence'].tolist()
labels = df['label'].tolist()
processed_sentences = []
max_len = 100

num_over_limit = 0

print("Processing sentences using spaCy")
for s in tqdm(range(len(raw_sentences))): # len(raw_sentences) goes here normally
	processed = nlp(raw_sentences[s])
	processed_sentences.append(processed)
	temp_vectors = []
	#temp_max = 0
	for word in processed:
		if(not word.pos_ in ['PUNCT','SYM','X']): # not word.is_stop and 
			temp_vectors.append(word.lex_id)
			#temp_max += 1
	if(len(temp_vectors) > max_len):
		temp_vectors = temp_vectors[:max_len] # if sequence is longer, simply truncate it (should not be needed, but ok)
		num_over_limit += 1
	vectors.append(temp_vectors)
	#if(temp_max > max_len):
	#	max_len = temp_max

print("Number of sentences found to be over max length of {} is {}".format(max_len,num_over_limit))


### model
# Imports (not sure how wise it is to do those here instead of at the top)
from keras.models import Sequential
from keras.layers import (Embedding, Activation, LSTM, Dense,Dropout)
from keras.utils import to_categorical
# set backend
os.environ['KERAS_BACKEND']='tensorflow'

# some variables we're going to need for the model
vocab_len = len(nlp.vocab.vectors.data) # just in case
vector_len = 300
batch_size = 32

print("Maximum sequence length = {}".format(max_len))

# last bit of pre-processing
print("Padding vectors")
padded_vectors = pad_sequences(vectors,maxlen=max_len,padding='pre')
print("Splitting data")
labels = to_categorical(labels)
X_train, X_test, Y_train, Y_test = train_test_split(padded_vectors,labels,test_size=0.2,random_state=42) # try a split that may not overfit?
print("Size of training data: {}".format(len(X_train)))

# initialize model
print("Initializing Keras Model")
model = Sequential()
model.add(Embedding(vocab_len,300,weights=[nlp.vocab.vectors.data],input_length=max_len,trainable=False))
#model.add(Dropout(0.4))
model.add(LSTM(max_len,dropout=0.2,recurrent_dropout=0.2,use_bias=True))
model.add(Dense(2,activation='softmax'))
model.compile(loss = 'categorical_crossentropy', optimizer='adam',metrics = ['accuracy'])
print(model.summary())
# train the model
print("Training model")
model_timing = time.time()
model.fit(X_train, Y_train, batch_size =batch_size, epochs = 30,  verbose = 2)
print("Model Trained. Time elapsed: {}".format(time.time()-model_timing))

# score model
score,acc = model.evaluate(X_test, Y_test, verbose = 2, batch_size = batch_size)
print('Test accuracy: {}\nModel Score: {}'.format(acc,score))

# Save model to disk
def save_model(model):
	model_save = 'model_best'
	print("Converting model to json")
	model_json = model.to_json()
	print("Saving model to {}".format(model_save))
	with open(model_save+'.json','w+') as json_file:
		json_file.write(model_json)
	print("Saving model weights")
	model.save_weights(model_save+'.weights')

save_model(model)


print("Done.")
print("Total time elapsed: {}s".format((time.time()-global_timer)))


