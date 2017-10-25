"""
This script takes bow representation of our texts and stores it into a text document in order to ease the load on the database
We also store the text labels on another list in order to retrieve them for further processing
"""
import mongoConnection
import pickle

mongoCo = mongoConnection.connectToMongo(ignore_unicode_error=True)
mongoDb = mongoCo.tensor_exp
mongoColl = mongoDb.news_aggregator

# Loading documents from the database
documentList = list(mongoColl.aggregate([
    {"$match": {"title_doc2bow": {"$exists": True}}},
    {"$project": {"title_doc2bow": 1, "cat_integer": 1}}
]))

if len(documentList) == 0:
    print("Nothing to do in here")
    exit()
else:
    print("Processing " + str(len(documentList)) + " documents\n")

# Creating an empty list for our corpus title vectors
corpus_title = []
labels = []

corpus_body = []

# Processing documents
for index, doc in enumerate(documentList, start=1):
    if index % 1000 == 0:
        print("\n##### Processing batch number " + str(index) + " #####\n")

    try:
        body_bow = doc["body_doc2bow"]
        body_bow_list = [words for words in body_bow]
        corpus_body.append(body_bow_list)
    except:
        pass
    finally:
        # Getting the bow representation from mongodb into a list and saving it on the disk
        title_bow = doc["title_doc2bow"]
        title_bow_list = [words for words in title_bow]
        corpus_title.append(title_bow_list)
        labels.append(doc["cat_integer"])

with open("lists/title/bow.txt", "wb") as fp:
    pickle.dump(corpus_title, fp)

with open("lists/title/labels.txt", "wb") as fp:
    pickle.dump(labels, fp)

mongoConnection.closeMongo(mongoCo)