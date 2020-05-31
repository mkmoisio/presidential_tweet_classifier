import json
import spacy
from spacy.tokens import DocBin
import numpy as np
import pickle

nlp = spacy.load('en_core_web_sm')

path_raw = './data/raw/%s.txt'
path_clean = './data/clean/%s.txt'
path_proc = './data/processed/%s.bin'

usernames = ['MikeBloomberg', 'realDonaldTrump']

def spacy_process(tweets):
    doc_bin = DocBin(attrs=["LEMMA", "POS", "TAG", "IS_ALPHA", "IS_STOP", "ENT_IOB", "ENT_TYPE"], store_user_data=True)
    docs = []
    for x in tweets:
        doc = nlp(x['msg'])
        doc_bin.add(doc)
        docs.append(doc)
    return doc_bin, docs

def clean(tweets, min_len = 100):
    tweets = map(lambda x: {'user': x[2], 'msg': x[4]}, tweets)
    tweets = list(filter(lambda x: len(x['msg']) >= min_len, tweets))
    return tweets

def get_cleaned_tweets(username):
    path_raw_username = path_raw % username
    path_clean_username = path_clean % username

    # test if cleaned data exists, if not, create it

    try:
        with open(path_clean_username, mode='r') as f:
            tweets = [json.loads(f)]
    except:
        with open(path_raw_username, mode='r') as f:
            tweets = clean([json.loads(x) for x in f])
           
        with open(path_clean_username, mode='w') as f:
            f.write(json.dumps(tweets, ensure_ascii=False, indent=2))

    return tweets

def get_processed_tweets(username):
    path_proc_username = path_proc % username

    try:
        with open(path_proc_username, mode='rb') as f:
            doc_bin = DocBin().from_bytes(f.read())
        nlp = spacy.blank("en")
        docs = list(doc_bin.get_docs(nlp.vocab))    

    except:
        tweets = get_cleaned_tweets(username)
        doc_bin, docs = spacy_process(tweets)
        with open(path_proc_username, mode='wb') as f:
            f.write(doc_bin.to_bytes())
    return docs


from collections import defaultdict

is_valid = lambda x: x.is_alpha and not x.is_stop


def lemma2index(docs):
    index = {}
    all_tokens = [doc for sb in docs for doc in sb]
    
    all_tokens = list(filter(is_valid, all_tokens))
    #print(len(all_tokens))
    lemmas = set([token.lemma for token in all_tokens])
    for i, v in enumerate(lemmas):
        index[v] = i
    #print(len(index))
    return index

def construct_matrix(docs, feature_index):
    array = np.zeros(shape = (len(docs), len(feature_index)))

    sample_idx = 0
    for doc in docs:
       # tokens = list(filter(is_valid, doc))
        lemmas = set([token.lemma for token in doc])
        for lemma in lemmas:
            try:
                #print(features_index[lemma])
                array[sample_idx, feature_index[lemma]] = 1
            except:
                pass
        sample_idx += 1

    return array        


docs = get_processed_tweets('MikeBloomberg')[0:8000]
docs.extend(get_processed_tweets('realDonaldTrump')[0:8000])

index = lemma2index(docs)
array = construct_matrix(docs, index)

from sklearn.decomposition import TruncatedSVD
svd = TruncatedSVD(n_components=100, n_iter= 15, random_state=42)
X = svd.fit_transform(array)
y = np.concatenate((np.zeros(shape = (8000, )), np.ones(shape = (8000, ))))

from sklearn.svm import SVC
clf = SVC(gamma='auto')
clf.fit(X, y)

bloombergs = get_processed_tweets('MikeBloomberg')[8000:9000]
print('---- test phase -----')
bloom_array = construct_matrix(bloombergs, index)
X_test = svd.transform(bloom_array)
results = clf.predict(X_test)
print(np.sum(results))
print('Percentage of Mikes\'s tweets classified as Mikes\'s (' + str(len(results))+ ' samples):', ((len(results) - np.sum(results)) * 100 / len(results)), '%')

trumps = get_processed_tweets('realDonaldTrump')[8000:9000]
trump_array = construct_matrix(trumps, index)
X_test = svd.transform(trump_array)
results = clf.predict(X_test)
print('Percentage of Donny\'s tweets classified as Donny\'s (' + str(len(results)) + ' samples):', np.sum(results) * 100 / len(results), '%')

pickle.dump(clf, open('svc', mode = 'wb'))
pickle.dump(svd, open('svd', mode = 'wb'))
pickle.dump(index, open('feature_index', mode = 'wb'))    