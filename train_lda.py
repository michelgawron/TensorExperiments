import pickle

import gensim
import pandas as pd
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)




for i in [256]:
    print("Loading tfidf corpus")
    # Loading tfidf corpus from disk
    tfidf_corpus = gensim.corpora.MmCorpus('tfidf/corpus_tfidf.mm')

    print("\n\n\n############ Creating LSI model for {} features ############\n\n\n".format(i))
    # Creating a LSI model fitting this corpus
    lda = gensim.models.LdaModel(corpus=tfidf_corpus, num_topics=i, passes=20)

    print("Saving model")
    lda.save("lda/model_{}.lda".format(i))

    # Creating LSI representation for ou vectors
    with open("lists/title/labels.txt", "rb") as fp:
        print("Creating and saving vectors")
        list_labels = pickle.load(fp)
        vecs_tuples = lda[tfidf_corpus]
        doc_vec = [[tup[1] for tup in vec_tuple] for vec_tuple in vecs_tuples]
        doc_vec = pd.DataFrame(doc_vec)
        doc_vec.insert(0, 'label', list_labels)
        doc_vec.to_csv('csv_vectors/docvec_lda_{}.csv'.format(i), index=False)
        fp.close()