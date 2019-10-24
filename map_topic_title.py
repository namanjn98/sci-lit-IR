# Extracting Topics using LDA on Titles

import pandas as pd
import pickle
from gensim.models import CoherenceModel
import nltk 
import numpy as np
import json
import os
import math
from nltk.corpus import stopwords
import gensim
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
import spacy
from spacy.lang.en import English
import pickle
from gensim import corpora

# Single column of texts
title_code_map = pd.read_csv('all_titles.csv')
####################################

# Preprocess texts
parser = English()
def tokenize(text):
    lda_tokens = []
    tokens = parser(text)
    for token in tokens:
        if token.orth_.isspace():
            continue
        else:
            lda_tokens.append(token.lower_)
    return lda_tokens

def get_lemma(word):
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma

en_stop = set(nltk.corpus.stopwords.words('english'))

def prepare_text_for_lda(text):
    tokens = tokenize(text)
    tokens = [token for token in tokens if len(token) > 4]
    tokens = [token for token in tokens if token not in en_stop]
    tokens = [get_lemma(token) for token in tokens]
    return tokens

####################################
get_text = title_code_map.keys()

text_data = []
for line in get_text:
    tokens = prepare_text_for_lda(unicode(line))
    text_data.append(tokens)

dictionary = corpora.Dictionary(text_data)
corpus = [dictionary.doc2bow(text) for text in text_data]

pickle.dump(corpus, open('corpus.pkl', 'wb'))
dictionary.save('dictionary.gensim')
####################################
# Training for 15 Topics
NUM_TOPICS = 15
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary)
ldamodel.save('lda-refresh-%d.gensim'%(NUM_TOPICS))

# Inferencing Model for a Topic for every Title
bucket = {}
for w,i in enumerate(corpus):
    list_ = ldamodel[i]
    for j in list_:
        if j[1] > 0.3:
            try:
                bucket[title_code_map[get_text[w]]].append(j[0])
            except:
                bucket[title_code_map[get_text[w]]] = [j[0]]

topics = ldamodel.print_topics(num_words=10)
for topic in topics:
    print(topic)
    print('\n')

# Saving
with open('topic-bucket.pickle', 'wb') as handle:
    pickle.dump(bucket, handle, protocol=pickle.HIGHEST_PROTOCOL)



