import pickle
import gensim
import pandas as pd
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)




for i in [4, 8, 16, 32, 64, 128, 256]:
    print("Loading tfidf corpus")
    # Loading tfidf corpus from disk
    tfidf_corpus = gensim.corpora.MmCorpus('tfidf/corpus_tfidf.mm')

    print("Creating LSI model for {} features".format(i))
    # Creating a LSI model fitting this corpus
    lsi = gensim.models.LsiModel(tfidf_corpus, i)

    print("Saving model")
    lsi.save("lsi/model_{}.lsi".format(i))

    # Creating LSI representation for our vectors
    with open("lists/title/labels.txt", "rb") as fp:
        print("Creating and saving vectors")
        list_labels = pickle.load(fp)
        vecs_tuples = lsi[tfidf_corpus]
        doc_vec = [[tup[1] for tup in vec_tuple] for vec_tuple in vecs_tuples]
        doc_vec = pd.DataFrame(doc_vec)
        doc_vec.insert(0, 'label', list_labels)
        doc_vec.to_csv('csv_vectors/docvec_{}.csv'.format(i), index=False)