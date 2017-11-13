import pickle
import json

j = 0

for i in range(1, 26):
    print("\n##### Processing batch number " + str(i) + " #####\n")

    with open("lists/body/tokenized_split/list_tokenized_docs{}.txt".format(i), "rb") as fp:
        list_bodies = list(pickle.load(fp))
        j += sum(sum([(1 if '\x00' in words else 0) for words in row]) for row in list_bodies)
        print(str(j))