"""
This script takes bow representation of our texts and stores it into a text document in order to ease the load on the database
"""
import mongoConnection
import pickle

i = 0

corpus_body = []

"""
Processing collection while there are documents to process
"""
while True:
    i += 1
    print("\n##### Processing batch number " + str(i) + " #####\n")

    mongoCo = mongoConnection.connectToMongo(ignore_unicode_error=True)
    mongoDb = mongoCo.tensor_exp
    mongoColl = mongoDb.news_aggregator

    # Loading documents from the database
    documentList = list(mongoColl.aggregate([
        {"$match": {"body_doc2bow": {"$exists": True}}},
        {"$match": {"used_in_clean_list": {"$exists": False}}},
        {"$project": {"body_doc2bow": 1}},
        {"$limit": 10000}
    ]))

    # If there's nothing to do, leaving
    if len(documentList) == 0:
        print("Nothing to do in here")
        exit()
    else:
        print("Processing " + str(len(documentList)) + " documents\n")

    # Opening the list file in update mode
    print("Corpus body length : " + str(len(corpus_body)))

    # Processing documents
    for index, doc in enumerate(documentList, start=1):
        if index % 1000 == 0:
            print("\n##### Processing doc number " + str(index) + " #####\n")

        doc_id = doc["_id"]

        # Appending new elements to the list
        try:
            body_bow = doc["body_doc2bow"]
            body_bow_list = [words for words in body_bow]
            corpus_body.append(body_bow_list)
            mongoColl.update_one({"_id": doc_id}, {"$set": {'used_in_clean_list': True}})
        except:
            pass
        """finally:
            title_bow = doc["title_doc2bow"]
            title_bow_list = [words for words in title_bow]
            corpus_title.append(title_bow_list)"""
        # Saving the list
    mongoConnection.closeMongo(mongoCo)
    with open("lists/body/bow.txt", "wb") as fp:
        pickle.dump(corpus_body, fp)