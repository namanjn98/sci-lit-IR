# Basic Algorithm to Get Similar Papers for a Given Paper

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import operator
from sklearn.decomposition import PCA
import json
#####################################
# Get Top 5 Papers
def get_5(vec, X_vec):
    
    list_df = {}
    k = 0
    for i,w in enumerate(X_vec):

        list_df[i] = np.dot(w, vec)   

        if list_df[i] == 1:
            k += 1
        if k == 5:
            break

    return sorted(list_df.items(), key=operator.itemgetter(1))[-5:]
######################################
# Format
# Paper_ID  ->  Category_1_List          Category_2_List       ...
# C14-4955  ->  ['English', 'French']    ['NMT', 'Sentiment']  ...

df = pd.read_csv('topics.csv')
list_df = np.array(df.values.tolist())

# Generating a list of topics from Pandas structure for each paper
# C14-4955 -> ['English', 'French', 'NMT', 'Sentiment']
main = []
for i in list_df:
    new = []
    o = 0
    string = []
    
    for j in i:            
        res = j.strip('][').split(', ')
        res = [str(k.replace("'", "")) for k in res]
        res = [k.strip().replace(" ","_") for k in res]
        
        if o == 0:
            o += 1
            new.append(res[0])
        
        else:
            string += res
    
    new_string = []
    for j in string:
        if 'no_topic' != j:
            new_string.append(j)
        
    main.append([' '.join(new_string)] + new)

df = pd.DataFrame(main)

# Get One-Hot Encoding over all Topics
# C14-4955 -> [0,0,0,0,1,1,1,1,0,0] 
# Here, ['English', 'French', 'NMT', 'Sentiment'] out of total pool of topics (10 in this case)

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(list(df[0]))

# Reducing Dimensions for Quicker Computation
pca = PCA(n_components=2)
principalComponents = pca.fit_transform(X)

# Getting Top 5 Most similar paper to given paper
# Similar == Cosine Similarity in Euclidean Plane
dict_df = {}
for i, w in enumerate(principalComponents):
    dict_df[i] = get_5(principalComponents[i], principalComponents)
    if i%1000 == 0:
        print i

new_df = {}
for i in dict_df:
    new_df[df.iloc[i][1]] = [df.iloc[j[0]][1] for j in dict_df[i]]

with open('for_similar_papers.json', 'w') as f:
    json.dump(new_df, f, ensure_ascii=False, indent=4)

# Can be extended to Similar Authors
# Add One-Hot Encoding Vectors of all the papers for that particular author
# Run the comparison 
# Get Similar Authors
