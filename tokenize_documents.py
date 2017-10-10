### This script is made to process our data in order to tokenize, lemmatize and stem words ###
### Preprocessing our data is a must-do in order to have good performance ###
test_sentence = """NLTK is a leading platform for building Python programs to work with human language data. It provides easy-to-use interfaces to over 50 corpora and lexical resources such as WordNet, along with a suite of text processing libraries for classification, tokenization, stemming, tagging, parsing, and semantic reasoning, wrappers for industrial-strength NLP libraries, and an active discussion forum.

Thanks to a hands-on guide introducing programming fundamentals alongside topics in computational linguistics, plus comprehensive API documentation, NLTK is suitable for linguists, engineers, students, educators, researchers, and industry users alike. NLTK is available for Windows, Mac OS X, and Linux. Best of all, NLTK is a free, open source, community-driven project.

NLTK has been called “a wonderful tool for teaching, and working in, computational linguistics using Python,” and “an amazing library to play with natural language.
This does provide something very cool. I did something. I am doing something. I do something. I don't have any ideas. I don t surprise
I dont” Hey you'are"""

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
from nltk.corpus import stopwords

import mongoConnection
import string

while True:
    mongoCo = mongoConnection.connectToMongo(ignore_unicode_error=True)
    tigerdb = mongoCo.tensor_exp
    tigerDocs = tigerdb.news_aggregator

    # Retrieving the documents we want to process
    documentList = list(tigerDocs.aggregate([
        {"$match": {"body_normalized": {"$exists": False}}},
        {"$match": {"text_body": {"$exists": True}}},
        {"$limit": 1000}
    ],
        allowDiskUse=True))

    if len(documentList) == 0:
        print("Nothing to do in here")
        exit()
    else:
        print("Processing " + str(len(documentList)) + " documents\n")

    # Initializing variables - WordNet Lemmatizer, downloading english stop words, getting list length, and batch size
    wnl = WordNetLemmatizer()
    nltk.download('stopwords')
    list_len = len(documentList)
    process_length = int(list_len/20)
    s = stopwords.words("english")

    # Punctuation we want to remove that is not in string.punctuation
    my_list_punctuation = "”“'\n\t\r" + string.punctuation



    # Processing documents
    for index, doc in enumerate(documentList, start=1):
        # Below statement only for output purpose
        if index % process_length == 0:
            print("Processing document n°" + str(index) + "/" + str(list_len))

        # Getting doc id and title/body
        doc_id = doc["_id"]
        basic_sentence = doc["text_body"]
        basic_sentence_without_punct = basic_sentence

        # Replacing punctuation
        for char in my_list_punctuation:
            basic_sentence_without_punct = basic_sentence_without_punct.replace(char, " ")

        # Tokenizing, stemming and lemmatizing sentence. After tokenizing, we remove the most common words (the, a, etc)
        body_words_list = word_tokenize(basic_sentence_without_punct)
        sentence_without_words = list(filter(lambda word: not word in s, body_words_list))
        body_stemmed_word = list(map(lambda word: stemmer().stem(word), sentence_without_words))
        body_lemm_words = list(map(lambda word: wnl.lemmatize(word), body_stemmed_word))

        # Removing most common words a second time after data processing
        final_sentence = list(filter(lambda word: not word in s, body_lemm_words))

        # Updating the document with the final sentence
        tigerDocs.update_one({"_id": doc_id}, {"$set": {'body_normalized': final_sentence}})
    mongoConnection.closeMongo(mongoCo)


"""
# The above code was an experiment in French
print(string.punctuation)

s = stopwords.words("english")

my_list = ["'"]
test_sentence_replace = test_sentence
for char in my_list:
    test_sentence_replace = test_sentence_replace.replace(char, " ")
test_fr_list = word_tokenize(test_sentence_replace)
test_sentence_without_words = list(filter(lambda word: not word in s, test_fr_list))
test_fr_stemmed = [stemmer().stem(words) for words in test_sentence_without_words]
test_fr_lemm = [wnl.lemmatize(words) for words in test_fr_stemmed]
test_final_sentence = []
personnal_dictionnary = "”“"
for words in test_fr_lemm:
    if words not in string.punctuation and words not in personnal_dictionnary:
        test_final_sentence.append(words)

test_final_sentence_filtered = list(filter(lambda word: not word in s, test_final_sentence))

print(test_fr_list)
print(test_fr_stemmed)
print(test_fr_lemm)
print(test_final_sentence)
print(test_final_sentence_filtered)
print(len(test_sentence.split(" ")))
print(len(test_final_sentence_filtered))
"""
