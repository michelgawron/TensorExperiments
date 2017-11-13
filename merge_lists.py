"""
This script merges the lists of bodies texts located in lists/bodies/tokenized_split.
The aim is to get a single file containing all texts in order to open it and feed it into gensim.
This script stores our documents in a single csv file - which seemes to perform significantly better than pickle on this use case.
"""
import csv
import pickle

for i in range(1, 26):
    print("\n##### Processing batch number " + str(i) + " #####\n")

    with open("lists/body/tokenized_split/list_tokenized_docs{}.txt".format(i), "rb") as fp:
        list_bodies = list(pickle.load(fp))
        list_bodies = [row for row in list_bodies if False not in [False for words in row if '\x00' in words]]
        fp.close()
        with open("lists/body/list_tokenized_docs.csv", "a+") as filecsv:
            print("Saving file number {}...".format(i))
            writer = csv.writer(filecsv)
            writer.writerows(list_bodies)
            filecsv.close()

print("End of script")
