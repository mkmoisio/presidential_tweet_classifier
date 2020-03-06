import json
import spacy
from spacy.tokens import DocBin


nlp = spacy.load('en_core_web_sm')

usernames = ['MikeBloomberg']

def spacy_process(tweets):
    doc_bin = DocBin(attrs=["LEMMA", "ENT_IOB", "ENT_TYPE"], store_user_data=True)
    docs = []
    for x in tweets:
        doc = nlp(x['msg'])
        doc_bin.add(doc)
        docs.append(doc)
    return doc_bin, docs

for username in usernames:
    path_raw = './data/raw/' + username + '.txt'
    path_clean = './data/clean/' + username + '.txt'
    path_proc = './data/processed/' + username + '.bin'

    # test if cleaned data exists, if not, create it
    try:
        with open(path_clean, mode='r') as f:
            tweets = [json.loads(f)]
    except:
        min_len = 100
        with open(path_raw, mode='r') as f:
            tweets = map(lambda x: {'user': x[2], 'msg': x[4]}, [json.loads(x) for x in f])
            tweets = list(filter(lambda x: len(x['msg']) >= min_len, tweets))

        with open(path_clean, mode='w') as f:
            f.write(json.dumps(tweets, ensure_ascii=False, indent=2))

    try:
        with open(path_proc, mode='rb') as f:
            doc_bin = DocBin().from_bytes(f.read())
        nlp = spacy.blank("en")
        docs = list(doc_bin.get_docs(nlp.vocab))    

    except:
        doc_bin, docs = spacy_process(tweets)
        with open(path_proc, mode='wb') as f:
            f.write(doc_bin.to_bytes())

    print(docs[0])

doc = docs[0]        
print([(ent.text, ent.label_) for ent in doc.ents])

    




"""     print(x['msg'])
    for sent in doc.sents:
        for token in sent: 
            print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)
            print() """
#docs = [nlp(x['msg']) for x in tweets]

""" for sent in docs[0].sents:
    for token in sent: 
        print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)

doc = docs[0]        
print([(ent.text, ent.label_) for ent in doc.ents])
 """

""" 
('./data/processed/realDonaldTrump.txt', mode='w') as f:
    f.write(json.dumps(docs, ensure_ascii=False, indent=2)) """