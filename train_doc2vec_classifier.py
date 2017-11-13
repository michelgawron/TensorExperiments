"""
This script trains a basic classifier using the doc2vec corpus
"""

from gensim.models import Doc2Vec
import random
import numpy as np
import pandas as pd
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.utils import shuffle

# Model we choose to train the classifier
model_features = 100

print("Loading model...")
model = Doc2Vec.load("doc2vec/model_window100_{}.d2v".format(str(model_features)))
print(model.docvecs[0])
# Importing labels
with open("lists/title/label_dict.pkl", "rb") as doc_labels:
    print("Files opened !")
    # Loading full labels from the pickle file and splitting them in 2 sets
    doc_labels = pickle.load(doc_labels)
    doc_labels_train = [doc_labels[i] for i in range(350000)]
    doc_labels_test = [doc_labels[i] for i in range(350000, len(doc_labels), 1)]

    vectors_train = [model.docvecs[i] for i in range(350000)]
    vectors_test = [model.docvecs[i] for i in range(350000, len(doc_labels), 1)]

    print("Lists loaded")
    print("Vector test[0] : {}".format(vectors_test[0]))
    print("Vector train[0] : {}".format(vectors_train[0]))
    print("Label test[0] : {}".format(doc_labels_test[0]))
    print("Label train[0] : {}".format(doc_labels_train[0]))

    classifier = LogisticRegression()
    classifier.fit(vectors_train, doc_labels_train)
    print("Train score : {}".format(classifier.score(vectors_train, doc_labels_train)))
    print("Test score : {}".format(classifier.score(vectors_test, doc_labels_test)))
