#Keywrod-Based Topic Extraction

import numpy as np
import pandas as pd
import nltk
import re
import pickle
from difflib import SequenceMatcher


# Linguistic Target of Study
TOS = '''Discourse
Pragmatics
Lexical semantics
Distributional semantics
Embeddings
Formal semantics
Propositional semantics
Event semantics
Extra-propositional semantics
Grounded semantics
Ontologies
Syntax
Morphology
Phonology
Phonetics
Prosody
Gesture
Code mixing
code switching
Multilingualism
Sociolinguistic variation
Language change
Typology
Neurolinguistics
cognitive linguistics
psycholinguistics'''


# Application Task: What do you work on?
app = '''Language understanding
Corpus development
corpus annotation
Language identification
Morphological analysis
Tagging
Chunking
Syntactic parsing
Semantic parsing
Discourse parsing
Word sense disambiguation
Named entity recognition
Textual entailment
Semantic similarity
Information extraction
Information retrieval
Relation extraction
Sentiment analysis
Emotion detection
Event detection
Time normalization
Question answering
Knowledge acquisition
Coreference resolution
Dialog structure
Conversation analysis
Language generation
Summarization
machine translation
Paraphrasing
Text simplification
Determining discourse relations
text organization
argumentation mining
Dialogue and interactive systems
Image description generation
video description generation
Belief analysis
factuality analysis
modality analysis
irrealis analysis
ASR
spoken language processing
OCR
Word segmentation
Text categorization
Spelling correction
Text quality prediction
Style analysis
Predicting speaker characteristics
Authorship attribution
Native language identification
Lexicon and paraphrase induction
Mathematical models
Biomedical
social science
Ethics
Multimodal systems
Modeling human language processing
computational psycholinguistics
Modeling human language acquisition'''

# Approaches: How are you working on it? 
approach = '''multilingual resources
Modeling linguistic knowledge 
Algorithm development 
Data analysis 
User evaluation
Crowd sourcing
human computation
Topic modeling
Deep learning
Bayesian model
Kernel method
Structured prediction
Generative model
Discriminative model
Graphical model
Representation learning
Semi-supervised learning
Unsupervised learning'''


# Your data: Languages *
data = '''Multilingual
Chinese
Indian
Arabic
Hebrew
Semitic
Low-Resource Languages
Signed Languages
Child language'''

# Your data: Genres *
data_genre = '''scientific literature
Literary text
News
Encyclopedia
Biographies
Written dialog 
Chat 
Social media
Non-private unedited text 
Twitter
blogs
Spoken dialog
Child-directed speech
child language
Other spoken genres
human-computer interaction 
query logs
Biomedical texts
Non-biomedical scholarly texts
Legal documents 
legal opinions
Clinical notes
Web crawl'''

import xmltodict

# Format
# Paper_ID    Full_Text       Abstract
# C14-5995    We propose...   We propose...
d = pd.read_csv('PaperCode_Fulltext_Abstract.csv')

TOS = TOS.lower().split('\n')
data_genre = data_genre.lower().split('\n')
data = data.lower().split('\n')
approach = approach.lower().split('\n')
app = app.lower().split('\n')

category = d[['0','1']].dropna().reset_index(drop=True)

# Func Matches Keywords
def func(temp, TOS, i):
    c = 0
    temp_2 = []
    for j in TOS:
        if j in i:
            temp_2.append(j)
            c = 1
    
    if c == 0:
        temp.append('no_topic')
    else:
        temp.append(temp_2)
    
    return temp
        
tags = []
k = 0
for num in range(category.shape[0]):
    i = category.iloc[num]['1'].lower()
    temp = [category.iloc[num]['0']]
    temp = func(temp, TOS, i)
    temp = func(temp, app, i)
    temp = func(temp, approach, i)    
    temp = func(temp, data, i)
    temp = func(temp, data_genre, i)
    tags.append(temp)
    
    k += 1 
    if k%1000 == 0:
        print(k)

f = pd.DataFrame(tags, columns=['code','linguistic', 'task', 'approach', 'languages', 'dataset_type'])
f = f[(f['linguistic'] != 'no_topic')|(f['task'] != 'no_topic')|(f['approach'] != 'no_topic')|(f['languages'] != 'no_topic')|(f['dataset_type'] != 'no_topic')]
f.to_csv('topics.csv', index=False)

