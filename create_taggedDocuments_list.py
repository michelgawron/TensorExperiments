"""
Create a list of TaggedDocuments (gensim representation of documents) before training doc2vec corpus
This ensures that we have a consistent representation of our documents, and helps us get right results
This script also stores a dictionary of labels
"""
import pickle

from gensim.models.doc2vec import TaggedDocument

# Opening sentences, labels, and label dictionary file
with open("lists/title/list_tokenized_docs.txt", "rb") as tokenized_docs, \
        open("lists/title/labels.txt", "rb") as labels, \
        open("lists/title/label_dict.pkl", "wb") as label_dict_file, \
        open("lists/title/list_tagged_documents.txt", "wb") as tagged_docs_file:
    print("Loading files")
    # Getting documents and labels from files
    documents = pickle.load(tokenized_docs)
    labels = pickle.load(labels)

    print("Creating empty list and dictionary and filling it")
    # Create a list of tagged documents and a dictionary of labels associated to each
    labeled_sentences = []
    label_dict = {}

    step_5percent = len(documents) // 20

    # We iterate over both labels and documents lists in order to create both sentences list and labels dictionary
    # Creating and appending vectors of [['words', 'from', 'corpus'], ['labels']]
    for index, (single_label, sentences) in enumerate(zip(labels, documents)):
        if index % step_5percent == 0:
            print("{}% achieved".format(5 * index / step_5percent))
        labeled_sentences.append(TaggedDocument(sentences, [index]))
        label_dict[index] = single_label

    print("Saving both")
    # Saving documents list and label dictionary
    pickle.dump(labeled_sentences, tagged_docs_file)
    pickle.dump(label_dict, label_dict_file)
