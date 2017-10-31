import pickle

import mongoConnection

# Batch counter
i = 0

list_titles = []

while True:
    i += 1
    print("\n##### Processing batch number " + str(i) + " #####\n")
    mongoCo = mongoConnection.connectToMongo(ignore_unicode_error=True)
    mongoDb = mongoCo.tensor_exp
    mongoColl = mongoDb.news_aggregator

    # Loading documents from the database
    documentList = list(mongoColl.aggregate([
        {"$match": {"clean_title": {"$exists": True}}},
        {"$match": {"clean_title_in_list": {"$exists": False}}},
        {"$limit": 10000}
    ]))

    # Exit statement
    if len(documentList) == 0:
        print("Nothing to do here")
        break
    else:
        print("Processing " + str(len(documentList)) + " documents")

    # Length variables initializing
    list_len = len(documentList)
    process_length = int(list_len / 20)

    # Processing documents
    for index, doc in enumerate(documentList, start=1):
        # Progress statement
        if index % process_length == 0:
            print("Processing document n°" + str(index) + "/" + str(list_len))

        # Getting fields that we need to process
        doc_id = doc["_id"]
        words_list = doc["clean_title"]
        list_titles.append(words_list)
        mongoColl.update_one({"_id": doc_id}, {"$set": {'clean_title_in_list': True}})

    mongoConnection.closeMongo(mongoCo)

with open("lists/title/list_tokenized_docs.txt", "wb") as fp:
    pickle.dump(list_titles, fp)
