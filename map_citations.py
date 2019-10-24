# Identifying Paper from Refeences

# Example,

# Reference
# Fuchun Peng and Andrew McCallum. 2004. Accurate information extraction 
# from research papers using conditional random fields. 
# In Daniel Marcu Susan Dumais and Salim Roukos, editors, HLT-NAACL
# 2004: Main Proceedings, pages 329–336, Boston,
# Massachusetts, USA, May 2 - May 7. Association
# for Computational Linguistics.

# Retrieving Information to map 
# ACL_ID - N04-1042
# Title - Accurate information extraction from research papers using conditional random fields

# Exact Paper Title matching after extracting Titles using Regex does not work.

import pandas as pd
import string
from nltk.probability import FreqDist, MLEProbDist
import pickle
import numpy as np
import time
import json
import os
import sys
import nltk
import re
from difflib import SequenceMatcher
import xmltodict
import sys

a = sys.argv[1]
b = sys.argv[2]
###################################
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def compare(i, j):
    if similar(tak, j) > 0.8:
        return 1
    else:
        return 0

def get_year(code):
    code_ = int(code[1:3])
    if code_ > 21:
        year = 1900 + code_
    else:
        year = 2000 + code_
    return year

####################################
# List of all (ACL_ID, Title) tuples which are taken from ACL Website
with open('SciBase/Paper_Meta_Data.pickle', 'rb') as f:
    x = pickle.load(f)

title_code_map = {}
for i in x:
    try:
        title_code_map[x[i]['Title']] = i
    except:
        print i

###################################
# List of all Citations/References which were identified by OCR
df = pd.read_csv('all_citations.csv')

df_2013 = df[df['Year'] > 2013].reset_index(drop=True)

# Removing using obvious Non-ACL Keywords
code = []
for i in df_2013['Citation']:
    work = ''.join(i.lower().split('- '))
    
    if len(work) < 20:
        code.append(i)
    elif 'journal' in work:
        code.append(i)
    elif 'nips' in work:
        code.append(i)
    elif 'aaai' in work:
        code.append(i)
    elif 'lrec' in work:
        code.append(i)
    elif 'springer' in work:
        code.append(i)
    elif 'text analysis conference' in work:
        code.append(i)
    elif 'j. mach. learn. res.' in work:
        code.append(i)
    elif 'arxiv' in work:
        code.append(i)
    elif 'iclr' in work:
        code.append(i)
    elif 'cvpr' in work:
        code.append(i)
    elif 'iccv' in work:
        code.append(i)
    elif 'icml' in work:
        code.append(i)
    elif 'neurocomputing' in work:
        code.append(i)
    elif 'www' in work:
        code.append(i)
    elif 'mit press' in work:
        code.append(i)
    elif 'ieee' in work:
        code.append(i)
    elif 'neural information processing system' in work:
        code.append(i)
    elif 'corr abs' in work:
        code.append(i)
    elif 'interspeech' in work:
        code.append(i)
    elif 'natural language engineering' in work:
        code.append(i)
    elif 'iwpt ' in work:
        code.append(i)
    elif 'john wiley and sons' in work:
        code.append(i)
    elif 'european language resources association' in work:
        code.append(i)
    elif 'master thesis' in work:
        code.append(i)
    elif 'neural computation' in work:
        code.append(i)
    elif 'university' in work:
        code.append(i)
    elif 'slpat' in work:
        code.append(i)
    elif 'asru' in work:
        code.append(i)
    elif 'sigkdd' in work:
        code.append(i)
    elif 'ialp' in work:
        code.append(i)
    elif 'ACM' in i:
        code.append(i)
    elif 'ICASSP' in i:
        code.append(i)
    elif 'citeseer' in work:
        code.append(i)

df_2013_filtered = df_2013[~df_2013['Citation'].isin(code)]
df_code_paper = pd.DataFrame([title_code_map.keys(), title_code_map.values(), [get_year(i) for i in title_code_map.values()]]).T
df_code_paper.columns = ['Title', 'ID', 'Year']

list_papers = title_code_map.keys()    


# Mapping Loop
main = []

count = 0 
start = time.time()
for i in df_2013_filtered['Citation'][a:b]:
	try:
		count += 1
		flg = 0

		row = df_2013_filtered[df_2013_filtered['Citation'] == i]
		list_title = list(df_code_paper[df_code_paper['Year'] < int(row['Year'][:1])+1]['Title'])
		process_list_title = []

		t = re.findall('\d\)*\.*.*\.', i)
		q = ' '.join(t[0].split(' ')[1:])
		tak = re.findall('[^\.]*\.', q)[0][:-1]

		h = 1
		for k in list_title:
		    try:
		        you = tak.split(' ')
		        if (you[0] in k) or (you[1] in k):
		            process_list_title.append(k)
		    except:
		        h = 0
		        print tak
		        break
		        
		if h == 0:
		    continue

		for j in process_list_title:
		    if compare(tak,j) == 1:
		        flg = 1
		        paper = title_code_map[j]
		        text = j
		        break

		if flg == 1:
		    for o in range(row.shape[0]):
		        main.append([str(row.iloc[o]['ID']), paper, tak, text])

		if count%1000 == 0: 
			print count, time.time() - start
	except:
		continue

pd.DataFrame(main).to_csv('%d_%d_cit_title.csv'%(a,b))
