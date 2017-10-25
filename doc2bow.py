"""
This program retrieves pre-processed text from our database, and converts it into bag of words representation
"""

import mongoConnection
from pathlib import Path
import gensim

my_file_title = Path("dict/title/clean_title.dict")
my_file_body = Path("dict/body/clean_body.dict")

i = 0

while True:
    # Loading dictionnaries from the disk as they exist now
    dict_title = gensim.corpora.Dictionary()
    dict_title = dict_title.load(str(my_file_title))
    dict_body = gensim.corpora.Dictionary()
    dict_body = dict_body.load(str(my_file_body))

    i += 1
    print("\n##### Processing batch number " + str(i) + " #####\n")

    # Getting database and collection - ignore_unicode_error set to True because of bad encoding due to scraping
    mongoCo = mongoConnection.connectToMongo(ignore_unicode_error=True)
    mongoDb = mongoCo.tensor_exp
    mongoColl = mongoDb.news_aggregator

    # Loading documents from the database
    documentList = list(mongoColl.aggregate([
        {"$match": {"title_doc2bow": {"$exists": False}}},
        {"$match": {"clean_title": {"$exists": True}}},
        {"$limit": 10000}
    ]))

    print("Loaded from mongodb")

    # Leaving if there's nothing to process
    if len(documentList) == 0:
        print("Nothing to do here")
        exit()
    else:
        print("Processing " + str(len(documentList)) + " documents")

    list_len = len(documentList)
    process_length = int(list_len / 20)

    # Processing documents
    for index, doc in enumerate(documentList, start=1):
        if index % process_length == 0:
            print("Processing document n°" + str(index) + "/" + str(list_len))
        doc_id = doc["_id"]

        # Getting title and body (if it exists) from a document, and converting them to bag of words representation
        try:
            doc_body = list(doc["clean_body"])
            body_bow = dict_body.doc2bow(doc_body)
            mongoColl.update_one({"_id": doc_id}, {"$set": {'body_doc2bow': body_bow}})
        except:
            pass
        finally:
            doc_title = list(doc["clean_title"])
            title_bow = dict_title.doc2bow(doc_title)
            mongoColl.update_one({"_id": doc_id}, {"$set": {'title_doc2bow': title_bow}})


    i += 1
    mongoConnection.closeMongo(mongoCo)