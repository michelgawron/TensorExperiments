"""
This script deletes words that appears less than five times in the whole corpus
"""
import mongoConnection
import pickle

"""
Create a dictionnary of rare words in order to get rid of them - throwing out garbage
"""
def createDictionnary(folder, empty_dict):
    with open("lists/" + folder + "/full_corpus.txt", "rb") as fp:
        list_of_words = pickle.load(fp)

        # Going through the list of words and keeping those which appear at least 5 times in the corpus
        for tuples in list_of_words:
            if tuples[1] > 5.0:
                empty_dict[tuples[0]] = "keep"
        fp.close()
        return empty_dict

my_dict_title = createDictionnary("title", {})
my_dict_body = createDictionnary("body", {})

# Batch counter
i = 0

while True:
    print("\n##### Processing batch number " + str(i) + " #####\n")
    mongoCo = mongoConnection.connectToMongo(ignore_unicode_error=True)
    mongoDb = mongoCo.tensor_exp
    mongoColl = mongoDb.news_aggregator

    # Loading documents from the database
    documentList = list(mongoColl.aggregate([
        {"$match": {"clean_title": {"$exists": False}}},
        {"$match": {"title_normalized": {"$exists": True}}},
        {"$limit": 10000}
    ]))

    # Exit statement
    if len(documentList) == 0:
        print("Nothing to do here")
        exit()
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
        words_list = doc["title_normalized"]

        # Try to process body field
        try:
            # Getting list of words for the body
            words_body_list = doc["body_normalized"]
            clean_words_body = []

            # For each word, checking if it is in the dict and appending the list if it is
            for single_word in words_body_list:
                if single_word in my_dict_body:
                    clean_words_body.append(single_word)

            # Updating mongodb
            mongoColl.update_one({"_id": doc_id}, {"$set": {'clean_body': clean_words_body}})
        except:
            # Pass if we cannot find it
            pass
        finally:
            clean_words = []

            # Going through the list of words, checking if it is in the dictionnary and appending if it is
            for single_word in words_list:
                if single_word in my_dict_title:
                    clean_words.append(single_word)

            # Updating mongodb
            mongoColl.update_one({"_id": doc_id}, {"$set": {'clean_title': clean_words}})

    i += 1
    mongoConnection.closeMongo(mongoCo)
