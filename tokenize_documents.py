### This script is made to process our data in order to tokenize, lemmatize and stem words ###
### Preprocessing our data is a must-do in order to have good performance ###
test_sentence = """NLTK is a leading platform for building Python programs to work with human language data. It provides easy-to-use interfaces to over 50 corpora and lexical resources such as WordNet, along with a suite of text processing libraries for classification, tokenization, stemming, tagging, parsing, and semantic reasoning, wrappers for industrial-strength NLP libraries, and an active discussion forum.

Thanks to a hands-on guide introducing programming fundamentals alongside topics in computational linguistics, plus comprehensive API documentation, NLTK is suitable for linguists, engineers, students, educators, researchers, and industry users alike. NLTK is available for Windows, Mac OS X, and Linux. Best of all, NLTK is a free, open source, community-driven project.

NLTK has been called “a wonderful tool for teaching, and working in, computational linguistics using Python,” and “an amazing library to play with natural language.”"""

test_fr_sentence = """Il s'agit d'une première en France, se félicite Halte à l'Obsolescence Programmée (HOP). L'association
 née en 2015 et spécialisée dans la lutte contre l'obsolescence programmée - une technique imputée aux fabricants pour 
 réduire volontairement la durée de vie d'un produit et inciter le consommateur à acheter davantage - a déposé lundi une
  plainte auprès du Procureur de la République de Nanterre à l'encontre de plusieurs grandes marques d'imprimantes. 
  Les fabricants HP, Canon, Brother et en particulier Epson sont cités dans cette plainte pour obsolescence programmée 
  et tromperie, accusés par l'association de mettre en place des pratiques visant à «raccourcir délibérément la durée 
  de vie des imprimantes et des cartouches»."""

import nltk
from nltk.stem.snowball import EnglishStemmer as stemmer
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import FrenchStemmer as frstemmer

import mongoConnection

mongoCo = mongoConnection.connectToMongo(ignore_unicode_error=True)
tigerdb = mongoCo.tensor_exp
tigerDocs = tigerdb.news_aggregator

# Retrieving the documents we want to process
documentList = list(tigerDocs.aggregate([
    {"$match": {"body_words": {"$exists": False}}},
    {"$match": {"text_body": {"$exists": True}}},
    {"$limit": 50000}
],
    allowDiskUse=True))

if len(documentList) == 0:
    print("Nothing to do in here")
    exit()
else:
    print("Processing " + str(len(documentList)) + " documents\n")

wnl = WordNetLemmatizer()
list_len = len(documentList)
process_length = int(list_len/20)

for index, doc in enumerate(documentList, start=1):
    if index % process_length == 0:
        print("Processing document n°" + str(index) + "/" + str(list_len))
    doc_id = doc["_id"]

    # Triple pre-processing - we are going to store those three fields in order to be able to process it again
    # If we wanna change it
    body_words_list = word_tokenize(doc["title"])
    body_stemmed_word = list(map(lambda word: stemmer().stem(word), body_words_list))
    body_lemm_words = list(map(lambda word: wnl.lemmatize(word), body_stemmed_word))

    tigerDocs.update_one({"_id": doc_id}, {"$set": {'body_words': body_words_list,
                                                    'body_stemmed_words': body_stemmed_word,
                                                    'body_lemm_words': body_lemm_words}})

# The above code was an experiment in French
"""
test_fr_list = word_tokenize(test_fr_sentence)
test_fr_stemmed = [frstemmer().stem(words) for words in test_fr_list]
test_fr_lemm = [wnl.lemmatize(words) for words in test_fr_stemmed]

print(test_fr_list)
print(test_fr_stemmed)
print(test_fr_lemm)
"""
