### Aggregating our words together after pre-processing ###
### Thus we will be able to use it in word2vec or doc2vec ##
import mongoConnection

for i in range(48):
    print("\n##### Processing batch number " + str(i) + "/48 #####\n")
    mongoCo = mongoConnection.connectToMongo(ignore_unicode_error=True)
    mongoDb = mongoCo.tensor_exp
    mongoColl = mongoDb.news_aggregator

    documentList = list(mongoColl.aggregate([
        {"$match": {"body_lemm_words": {"$exists": True}}},
        {"$match": {"body_sentences_from_words": {"$exists": False}}},
        {"$limit": 10000}
    ]))

    if len(documentList) == 0:
        print("Nothing to do here")
        exit()
    else:
        print("Processing " + str(len(documentList)) + " documents")

    list_len = len(documentList)
    process_length = int(list_len / 20)

    for index, doc in enumerate(documentList, start=1):
        if index % process_length == 0:
            print("Processing document n°" + str(index) + "/" + str(list_len))
        doc_id = doc["_id"]

        words_list = doc["body_lemm_words"]
        words_to_sentence = ' '.join(words_list)

        mongoColl.update_one({"_id": doc_id}, {"$set": {'body_sentences_from_words': words_to_sentence}})
    mongoConnection.closeMongo(mongoCo)
