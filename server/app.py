from flask import Flask, request
from waitress import serve
import pickle
import sklearn
import spacy
import numpy as np
app = Flask(__name__)


@app.route('/classify',  methods=['POST'])
def classify():
   # print(request.json)
    doc = nlp(request.json['tweet'])

  #  tokens = list(filter(is_valid, doc))
    lemmas = set([token.lemma for token in doc])

    array = np.zeros(shape=(1, len(feature_index)))

    for lemma in lemmas:
        try:
            # print(features_index[lemma])
            array[0, feature_index[lemma]] = 1
        except:
            pass


    X = svd.transform(array)

    prediction = clf.predict(X)
    if prediction[0] == 1:
        return (
            {"author": "Donny"}
            )

    else: 
        return (
            {"author": "Mike"}
            )



if __name__ == '__main__':
    nlp = spacy.load('en_core_web_sm')

    clf = pickle.load(open('./saved_objects/svc.bin', 'rb'))
    svd = pickle.load(open('./saved_objects/svd.bin', 'rb'))
    feature_index = pickle.load(open('./saved_objects/feature_index.bin', 'rb'))
    serve(app, listen='*:5000')

