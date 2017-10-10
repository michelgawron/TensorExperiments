### Creating a dictionnary with pre-processed texts ###
### The dictionnary is basically a map from words to integers ###
import mongoConnection
from pathlib import Path
import gensim

# Checking if a dictionnary already exists or not
my_file_title = Path("dict/title/new_title.dict")
my_file_body = Path("dict/body/new_body.dict")

# If dictionnaries do not exist, we are going to create and save them on the disk
if not(my_file_body.exists()):
    print("Do not exist")
    gensim.corpora.Dictionary().save(str(my_file_body))
if not(my_file_title.exists()):
    gensim.corpora.Dictionary().save(str(my_file_title))

i = 0

while True:
    # Loading dictionnaries from the disk as they exist now
    dict_title = gensim.corpora.Dictionary()
    dict_title = dict_title.load(str(my_file_title))
    dict_body = gensim.corpora.Dictionary()
    dict_body = dict_body.load(str(my_file_body))

    i += 1
    print("\n##### Processing batch number " + str(i) + " #####\n")
    mongoCo = mongoConnection.connectToMongo(ignore_unicode_error=True)
    mongoDb = mongoCo.tensor_exp
    mongoColl = mongoDb.news_aggregator

    # Loading documents from the database
    documentList = list(mongoColl.aggregate([
        {"$match": {"used_in_dict": {"$exists": False}}},
        {"$match": {"title_normalized": {"$exists": True}}},
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
            print(dict_title)
            print(dict_body)
        doc_id = doc["_id"]

        # Getting title sentences
        title_sentences = doc["title_normalized"]
        try:
            # Trying to get body sentences (if the field exists in the database) and adding it
            body_sentences = doc["body_normalized"]
            dict_body.add_documents([body_sentences])
        except KeyError:
            # When the document has no body, we pass the exception in order to add the title to the dictionnary
            pass
        finally:
            dict_title.add_documents([title_sentences])
            # Updating mongodb
            mongoColl.update_one({"_id": doc_id}, {"$set": {'used_in_dict': True}})
    mongoConnection.closeMongo(mongoCo)
    # Saving dictionnaries
    dict_title.save(str(my_file_title))
    dict_body.save(str(my_file_body))
