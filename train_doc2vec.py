"""
Training a doc2vec model following those steps :
1/ Appending a label representing the category of a document to each title
"""
import logging
import pickle
from gensim import utils
import gensim
from gensim.models.doc2vec import TaggedDocument
from gensim.models import Doc2Vec
from sklearn.utils import shuffle

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

assert gensim.models.doc2vec.FAST_VERSION > -1, "This will be painfully slow otherwise"

# Opening sentences and labels lists
with open("lists/title/list_tagged_documents.txt", "rb") as tagged_docs:
    # Loading lists
    labeled_sentences = pickle.load(tagged_docs)
    print(labeled_sentences[0])
    print("Len : {}".format(len(labeled_sentences)))

    for i in [10, 20, 30, 50, 100, 200, 300, 400]:
        # Creating model, and feeding it with vocabulary
        model = Doc2Vec(size=i, window=10, workers=20)
        model.build_vocab(labeled_sentences)

        # Training the model with 25 steps
        for epoch in range(25):
            labeled_sentences = shuffle(labeled_sentences)
            model.train(labeled_sentences, total_examples=model.corpus_count, epochs=model.iter)
            model.save("doc2vec/model_{}.d2v".format(i))
