"""
Create a tfidf model from our title corpus
"""

import pickle
import gensim

with open("lists/title/bow.txt", "rb") as fp:
    # Load the list of bag of words for our corpus
    title_bow = pickle.load(fp)
    print("Loaded, going through tfidf constructor")

    # Training tfidf model
    tfidf = gensim.models.TfidfModel(title_bow)
    print(tfidf)
    print("Saving tfidf model")
    tfidf.save('tfidf/model.tfidf')
    print("Applying tfidf model to our corpus")

    # Applying it on our corpus
    corpus_tfidf = tfidf[title_bow]
    print(len(corpus_tfidf))
    print("Saving the tfidf representation of our corpus")

    # Saving the tfidf corpus
    gensim.corpora.MmCorpus.serialize('tfidf/corpus_tfidf.mm', corpus_tfidf)