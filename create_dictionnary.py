### Creating a dictionnary with pre-processed texts ###
### The dictionnary is basically a map from words to integers ###
import mongoConnection
from pathlib import Path
import gensim

# Checking if a dictionnary already exists or not
my_file_title = Path("dict/title/title.dict")
my_file_body = Path("dict/body/body.dict")

if not(my_file_body.exists()):
    print("Do not exist")
    gensim.corpora.Dictionary().save(str(my_file_body))
if not(my_file_title.exists()):
    gensim.corpora.Dictionary().save(str(my_file_title))

i = 0

while True:
    # Loading dictionnaries from the disk
    dict_title = gensim.corpora.Dictionary()
    dict_title = dict_title.load(str(my_file_title))
    dict_body = gensim.corpora.Dictionary()
    dict_body = dict_body.load(str(my_file_body))

    i += 1
    print("\n##### Processing batch number " + str(i) + " #####\n")
    mongoCo = mongoConnection.connectToMongo(ignore_unicode_error=True)
    mongoDb = mongoCo.tensor_exp
    mongoColl = mongoDb.news_aggregator

    documentList = list(mongoColl.aggregate([
        {"$match": {"used_in_dict": {"$exists": False}}},
        {"$match": {"sentences_from_words": {"$exists": True}}},
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
            print(dict_title)
            print(dict_body)
        doc_id = doc["_id"]

        title_sentences = doc["title_lemm_words"]
        try:
            body_sentences = doc["body_lemm_words"]
            dict_body.add_documents([body_sentences])
        except KeyError:
            # When the document has no body, we pass the exception in order to add the title to the dictionnary
            pass
        finally:
            # DO nothing
            dict_title.add_documents([title_sentences])
            mongoColl.update_one({"_id": doc_id}, {"$set": {'used_in_dict': True}})
    mongoConnection.closeMongo(mongoCo)
    dict_title.save(str(my_file_title))
    dict_body.save(str(my_file_body))
